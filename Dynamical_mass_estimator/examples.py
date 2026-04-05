"""
Example script showing how to use ClusterAnalyzer in Python/Jupyter

This demonstrates how to integrate the analysis module with the original notebook
"""

# Example 1: Basic Usage
# ======================

from src.cluster_analyzer import ClusterAnalyzer

# Initialize analyzer
analyzer = ClusterAnalyzer(
    plot_dir="./plots",
    data_dir="./data"
)

# Query SDSS for a galaxy cluster
df = analyzer.query_sdss(
    ra=150.0,           # Right Ascension
    dec=2.0,            # Declination  
    radius_arcmin=10    # Search radius
)

print(f"Downloaded {len(df)} galaxies from SDSS")


# Example 2: Step-by-Step Analysis
# ==================================

# Step 1: Average by object ID
averaged_df = analyzer.average_by_objid()
print(f"Averaged to {len(averaged_df)} objects")

# Step 2: Filter by redshift (3-sigma cut)
filtered_df, z_min, z_max, mean_z, std_z = analyzer.filter_by_redshift(sigma=3)
print(f"After filtering: {len(filtered_df)} galaxies")

# Step 3: Calculate velocity dispersion
cluster_z, velocity_disp, filtered_df = analyzer.calculate_velocity_dispersion(z_min, z_max)
print(f"Velocity Dispersion: {velocity_disp:.2f} km/s")

# Step 4: Calculate cluster diameter
diameter = analyzer.calculate_diameter()
print(f"Cluster Diameter: {diameter:.3f} Mpc")

# Step 5: Calculate dynamical mass
dyn_mass = analyzer.calculate_dynamical_mass()
print(f"Dynamical Mass: {dyn_mass:.2e} M☉")

# Step 6: Calculate luminous mass
lum_mass, dm_ratio = analyzer.calculate_luminous_mass(stellar_mass_per_galaxy=1e11)
print(f"Luminous Mass: {lum_mass:.2e} M☉")
print(f"Dark Matter Ratio: {dm_ratio:.1f}x")


# Example 3: Quick Full Analysis
# ===============================

analyzer_quick = ClusterAnalyzer()

results = analyzer_quick.run_full_analysis(
    ra=150.0,
    dec=2.0,
    radius_arcmin=10,
    stellar_mass=1e11
)

# Access all results at once
print("\n=== FULL ANALYSIS RESULTS ===")
for key, value in results.items():
    if isinstance(value, float):
        print(f"{key}: {value:.3e}" if abs(value) > 1000 or abs(value) < 0.001 else f"{key}: {value:.4f}")
    else:
        print(f"{key}: {value}")


# Example 4: Generate Plots
# ==========================

# Create individual plots
analyzer_quick.plot_velocity_distribution(save=True)
analyzer_quick.plot_mass_comparison(save=True)

print("\nPlots saved to ./plots/")


# Example 5: Batch Processing Multiple Clusters
# ===============================================

clusters = [
    {"name": "Coma", "ra": 194.95, "dec": 27.96},
    {"name": "Virgo", "ra": 187.71, "dec": 12.39},
]

results_batch = {}

for cluster in clusters:
    print(f"\nAnalyzing {cluster['name']} Cluster...")
    
    analyzer_batch = ClusterAnalyzer()
    
    try:
        result = analyzer_batch.run_full_analysis(
            ra=cluster['ra'],
            dec=cluster['dec'],
            radius_arcmin=10
        )
        results_batch[cluster['name']] = result
    except Exception as e:
        print(f"Error analyzing {cluster['name']}: {e}")

# Compare results
print("\n=== CLUSTER COMPARISON ===")
for cluster_name, result in results_batch.items():
    print(f"\n{cluster_name}:")
    print(f"  Redshift: {result['cluster_redshift']:.4f}")
    print(f"  Velocity Dispersion: {result['velocity_dispersion']:.0f} km/s")
    print(f"  Dynamical Mass: {result['dynamical_mass']:.2e} M☉")
    print(f"  Dark Matter Factor: {result['dark_matter_ratio']:.1f}x")
