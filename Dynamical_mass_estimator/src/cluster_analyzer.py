"""
Dynamical Mass Estimator for Galaxy Clusters

This module provides functions to query SDSS DR16 data and estimate
the dynamical mass of galaxy clusters using velocity dispersion.
"""

import requests
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from astropy.constants import G, c


class ClusterAnalyzer:
    """
    A class to analyze galaxy cluster data and estimate dynamical mass.
    """
    
    def __init__(self, plot_dir="../plots", data_dir="../data"):
        """
        Initialize the analyzer with directories for saving plots and data.
        
        Parameters
        ----------
        plot_dir : str
            Directory to save plots
        data_dir : str
            Directory to save data
        """
        self.plot_dir = plot_dir
        self.data_dir = data_dir
        self.c_km_s = c.to('km/s').value
        self.G_si = G.value
        self.H_0 = 70 * 1000 / (3.086e22)  # Hubble constant in SI units (s^-1)
        self.q0 = -0.534  # Deceleration parameter
        self.c_m_s = c.value  # Speed of light in m/s
        
        # Create directories if they don't exist
        os.makedirs(self.plot_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Data storage
        self.raw_df = None
        self.averaged_df = None
        self.filtered_df = None
        self.cluster_redshift = None
        self.velocity_dispersion = None
        self.diameter_Mpc = None
        self.dynamical_mass_solar = None
        self.luminous_mass = None
        
    def query_sdss(self, ra, dec, radius_arcmin, save_filename="cluster_data.csv"):
        """
        Query SDSS DR16 SkyServer for galaxies around a given RA, DEC.

        Parameters
        ----------
        ra : float
            Right Ascension (degrees)
        dec : float
            Declination (degrees)
        radius_arcmin : float
            Search radius in arcminutes
        save_filename : str
            CSV filename to save results

        Returns
        -------
        pd.DataFrame or None
            DataFrame with query results, or None if query fails.
        """
        save_path = os.path.join(self.data_dir, save_filename)
        
        query = f"""
        SELECT
            s.objid,
            sz.ra AS ra,
            sz.dec AS dec,
            pz.z AS photoz,
            pz.zerr AS photozerr,
            sz.z AS specz,
            sz.zerr AS speczerr,
            b.distance AS proj_sep,
            s.modelMag_u AS umag,
            s.modelMagErr_u AS umagerr,
            s.modelMag_g AS gmag,
            s.modelMagErr_g AS gmagerr,
            s.modelMag_r AS rmag,
            s.modelMagErr_r AS rmagerr,
            s.type AS obj_type
        FROM BESTDR16..PhotoObjAll AS s
        JOIN dbo.fGetNearbyObjEq({ra}, {dec}, {radius_arcmin}) AS b
            ON b.objID = s.objID
        JOIN Photoz AS pz ON pz.objid = s.objid
        JOIN SpecObjAll AS sz ON sz.bestobjid = s.objid
        WHERE s.type = 3 AND sz.z > 0.05 AND sz.z < 0.20
        """

        url = "https://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
        params = {"cmd": query, "format": "csv"}

        print(f"📡 Querying SDSS SkyServer...\n   RA={ra}, DEC={dec}, Radius={radius_arcmin} arcmin")
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Query failed: {e}")
            return None

        # Clean CSV (remove comment lines)
        lines = [line for line in response.text.splitlines() if not line.startswith('#')]
        clean_text = "\n".join(lines)

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)

        print(f"✅ Data saved to: {save_path}")

        # Load into DataFrame
        try:
            df = pd.read_csv(save_path)
            self.raw_df = df
            print(f"ℹ️ {len(df)} rows loaded into DataFrame")
            return df
        except Exception as e:
            print(f"❌ Failed to load DataFrame: {e}")
            return None

    def average_by_objid(self):
        """
        Average the data by object ID.

        Returns
        -------
        pd.DataFrame
            Averaged DataFrame
        """
        if self.raw_df is None:
            raise ValueError("No raw data loaded. Call query_sdss first.")
        
        self.averaged_df = self.raw_df.groupby('objid').agg({
            'specz': 'mean',
            'ra': 'first',
            'dec': 'first',
            'proj_sep': 'first',
        }).reset_index()
        
        return self.averaged_df

    def filter_by_redshift(self, sigma=3):
        """
        Filter data by 3-sigma redshift limits.

        Parameters
        ----------
        sigma : float
            Number of standard deviations for outlier removal

        Returns
        -------
        tuple
            (filtered_df, z_min, z_max, mean_z, std_z)
        """
        if self.averaged_df is None:
            raise ValueError("No averaged data. Call average_by_objid first.")
        
        mean_specz = self.averaged_df['specz'].mean()
        std_specz = self.averaged_df['specz'].std()

        z_min = mean_specz - sigma * std_specz
        z_max = mean_specz + sigma * std_specz

        self.filtered_df = self.averaged_df[
            (self.averaged_df['specz'] >= z_min) & 
            (self.averaged_df['specz'] <= z_max)
        ].copy()

        print(f"Mean specz: {mean_specz:.5f}")
        print(f"Standard Deviation: {std_specz:.5f}")
        print(f"Redshift Range ({sigma}-sigma cut): [{z_min:.5f}, {z_max:.5f}]")
        print(f"Galaxies before filtering: {len(self.averaged_df)}")
        print(f"Galaxies after filtering: {len(self.filtered_df)}")

        return self.filtered_df, z_min, z_max, mean_specz, std_specz

    def calculate_velocity_dispersion(self, z_min, z_max):
        """
        Calculate velocity dispersion from redshift data.

        Parameters
        ----------
        z_min : float
            Minimum redshift after filtering
        z_max : float
            Maximum redshift after filtering

        Returns
        -------
        tuple
            (cluster_redshift, velocity_dispersion, filtered_df)
        """
        if self.raw_df is None:
            raise ValueError("No raw data loaded. Call query_sdss first.")
        
        # Use average redshift from filtered data
        filtered_temp = self.raw_df[
            (self.raw_df['specz'] >= z_min) & 
            (self.raw_df['specz'] <= z_max)
        ].copy()
        
        self.cluster_redshift = filtered_temp['specz'].mean()

        # Calculate velocities
        filtered_temp['velocity'] = self.c_km_s * (
            (1 + filtered_temp['specz'])**2 - (1 + self.cluster_redshift)**2
        ) / (
            (1 + filtered_temp['specz'])**2 + (1 + self.cluster_redshift)**2
        )

        self.velocity_dispersion = filtered_temp['velocity'].std()
        self.filtered_df = filtered_temp

        print(f"Mean Cluster Redshift: {self.cluster_redshift:.5f}")
        print(f"Velocity Dispersion (σ): {self.velocity_dispersion:.2f} km/s")

        return self.cluster_redshift, self.velocity_dispersion, filtered_temp

    def calculate_diameter(self):
        """
        Calculate the physical diameter of the cluster.

        Returns
        -------
        float
            Diameter in Megaparsecs
        """
        if self.filtered_df is None or self.cluster_redshift is None:
            raise ValueError("Filtered data or cluster redshift not available.")

        z_cluster = self.cluster_redshift

        # Co-moving distance
        r = (self.c_m_s * z_cluster / self.H_0) * (
            1 - (z_cluster / 2) * (1 + self.q0)
        )

        # Angular diameter distance
        D_A = r / (1 + z_cluster)

        # Maximum angular separation
        theta_arcmin = self.filtered_df['proj_sep'].max()
        theta_rad = (theta_arcmin / 60) * (np.pi / 180)

        # Physical diameter
        diameter = D_A * theta_rad
        self.diameter_Mpc = diameter / 3.086e22

        print(f"Diameter: {self.diameter_Mpc:.3f} Mpc")

        return self.diameter_Mpc

    def calculate_dynamical_mass(self):
        """
        Calculate the dynamical mass using the virial theorem.

        Returns
        -------
        float
            Dynamical mass in solar masses
        """
        if (self.velocity_dispersion is None or 
            self.diameter_Mpc is None):
            raise ValueError("Required parameters not calculated.")

        sigma_m_s = self.velocity_dispersion * 1000  # km/s to m/s
        
        # Cluster radius in meters (half the diameter in Mpc)
        diameter_m = self.diameter_Mpc * 3.086e22
        R = diameter_m / 2

        # Dynamical mass in kg
        M_dyn_kg = (3 * sigma_m_s**2 * R) / self.G_si

        # Convert to solar masses
        self.dynamical_mass_solar = M_dyn_kg / 1.989e30

        print(f"Dynamical Mass: {self.dynamical_mass_solar:.3e} solar masses")

        return self.dynamical_mass_solar

    def calculate_luminous_mass(self, stellar_mass_per_galaxy=1e11):
        """
        Estimate the total luminous (stellar) mass.

        Parameters
        ----------
        stellar_mass_per_galaxy : float
            Assumed stellar mass per galaxy in solar masses

        Returns
        -------
        tuple
            (luminous_mass, dark_matter_ratio)
        """
        if self.filtered_df is None:
            raise ValueError("Filtered data not available.")

        N_galaxies = len(self.filtered_df)
        self.luminous_mass = N_galaxies * stellar_mass_per_galaxy

        if self.dynamical_mass_solar is None:
            raise ValueError("Dynamical mass not calculated yet.")

        dark_matter_ratio = self.dynamical_mass_solar / self.luminous_mass

        print(f"Number of Galaxies: {N_galaxies}")
        print(f"Estimated Luminous Mass: {self.luminous_mass:.2e} solar masses")
        print(f"Dark Matter Factor: {dark_matter_ratio:.2f}x")

        return self.luminous_mass, dark_matter_ratio

    def save_plot(self, fig=None, filename="plot.png", dpi=150):
        """
        Save a Matplotlib figure to the plot directory.

        Parameters
        ----------
        fig : matplotlib.figure.Figure, optional
            Figure to save. If None, uses current active figure.
        filename : str
            File name (including extension)
        dpi : int
            Resolution in dots per inch
        """
        os.makedirs(self.plot_dir, exist_ok=True)
        fig = fig or plt.gcf()
        path = os.path.join(self.plot_dir, filename)
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        print(f"Plot saved to {path}")

    def plot_redshift_histogram(self, save=True):
        """Plot histogram of spectroscopic redshift."""
        if self.average_df is None:
            raise ValueError("No averaged data available.")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(self.averaged_df['specz'], bins=90, color='skyblue', edgecolor='black')
        ax.set_title("Distribution of Spectroscopic Redshift")
        ax.set_xlabel("Spectroscopic Redshift (specz)")
        ax.set_ylabel("Number of Galaxies")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        if save:
            self.save_plot(fig, "spectroscopic_redshift_histogram.png")
        return fig

    def plot_velocity_distribution(self, save=True):
        """Plot histogram of velocity distribution."""
        if self.filtered_df is None:
            raise ValueError("No filtered data available.")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(self.filtered_df['velocity'], bins=50, color='orchid', edgecolor='black')
        ax.set_title("Velocity Distribution of Cluster Galaxies")
        ax.set_xlabel("Velocity (km/s)")
        ax.set_ylabel("Number of Galaxies")
        ax.grid(True, linestyle='--', alpha=0.7)
        
        if save:
            self.save_plot(fig, "velocity_distribution.png")
        return fig

    def plot_mass_comparison(self, save=True):
        """Plot comparison of luminous vs dynamical mass."""
        if self.luminous_mass is None or self.dynamical_mass_solar is None:
            raise ValueError("Masses not calculated yet.")
        
        fig, ax = plt.subplots(figsize=(8, 5))
        masses = [self.luminous_mass, self.dynamical_mass_solar]
        labels = ['Luminous Mass (Stars)', 'Dynamical Mass (Total)']
        
        ax.bar(labels, masses, color=['skyblue', 'orange'], edgecolor='black')
        ax.set_yscale('log')
        ax.set_ylabel("Mass (Solar Masses)")
        ax.set_title("Comparison of Luminous Mass vs Dynamical Mass")
        ax.grid(True, which="both", ls="--", linewidth=0.5, alpha=0.7)
        
        if save:
            self.save_plot(fig, "mass_comparison.png")
        return fig

    def run_full_analysis(self, ra, dec, radius_arcmin, stellar_mass=1e11):
        """
        Run complete analysis pipeline.

        Parameters
        ----------
        ra : float
            Right Ascension (degrees)
        dec : float
            Declination (degrees)
        radius_arcmin : float
            Search radius in arcminutes
        stellar_mass : float
            Assumed stellar mass per galaxy

        Returns
        -------
        dict
            Dictionary with all calculated results
        """
        print("\n" + "="*60)
        print("Starting Full Analysis Pipeline")
        print("="*60 + "\n")

        # Step 1: Query SDSS
        print("Step 1: Querying SDSS...")
        self.query_sdss(ra, dec, radius_arcmin)
        
        # Step 2: Average by object ID
        print("\nStep 2: Averaging by object ID...")
        self.average_by_objid()
        
        # Step 3: Filter by redshift
        print("\nStep 3: Filtering by redshift...")
        filtered_df, z_min, z_max, mean_z, std_z = self.filter_by_redshift()
        
        # Step 4: Calculate velocity dispersion
        print("\nStep 4: Calculating velocity dispersion...")
        self.calculate_velocity_dispersion(z_min, z_max)
        
        # Step 5: Calculate diameter
        print("\nStep 5: Calculating cluster diameter...")
        self.calculate_diameter()
        
        # Step 6: Calculate dynamical mass
        print("\nStep 6: Calculating dynamical mass...")
        self.calculate_dynamical_mass()
        
        # Step 7: Calculate luminous mass
        print("\nStep 7: Calculating luminous mass...")
        self.calculate_luminous_mass(stellar_mass)
        
        print("\n" + "="*60)
        print("Analysis Complete!")
        print("="*60 + "\n")

        return {
            'cluster_redshift': self.cluster_redshift,
            'velocity_dispersion': self.velocity_dispersion,
            'diameter_Mpc': self.diameter_Mpc,
            'dynamical_mass': self.dynamical_mass_solar,
            'luminous_mass': self.luminous_mass,
            'dark_matter_ratio': self.dynamical_mass_solar / self.luminous_mass,
            'num_galaxies': len(self.filtered_df)
        }
