# Dynamical Mass Estimator for Galaxy Clusters

This repository provides a pipeline to estimate the dynamical mass of galaxy clusters using redshift and photometric data sourced from the Sloan Digital Sky Survey (SDSS DR16). It utilizes astrophysical methods such as velocity dispersion and the virial theorem to infer the total mass of clusters.

---

## 🚀 Quick Start

### 1. **Setup (First Time Only)**
```bash
cd Dynamical_mass_estimator
chmod +x setup.sh
./setup.sh
```

### 2. **Activate Virtual Environment**
```bash
source venv/bin/activate
```

### 3. **Run the Web UI**
```bash
streamlit run app.py
```

The application will automatically open in your browser 🌌

---

## 📋 Overview

Galaxy clusters are the most massive gravitationally bound systems in the universe. This project analyzes cluster member galaxies and computes the dynamical mass from redshift-based velocity dispersions.

---

## ✨ Features

### 🌐 Web UI Interface
- **Interactive Dashboard**: Parameter controls with real-time feedback
- **3 Analysis Tabs**: 
  - 📊 **Analysis**: View results & statistics
  - 📈 **Plots**: Velocity distribution & mass comparisons
  - 📋 **Data**: Download filtered galaxy data
- **Dark/Light Mode Toggle**: Switch themes seamlessly
- **Responsive Design**: Works on desktop and tablet
- **Publication-Ready Output**: Export data & visualizations

### 🔍 Analysis Capabilities
- Query SDSS DR16 SkyServer directly
- Filter galaxies by spectroscopic redshift
- Calculate velocity dispersion
- Estimate cluster diameter from angular extent
- Compute dynamical mass using the virial theorem
- Assess dark matter content
- Generate statistical comparisons

### 💻 Python Integration
- Reusable `ClusterAnalyzer` class
- Jupyter notebook support
- Batch processing capability
- Custom workflow automation

---

## 🎨 User Interface

### Dark Mode / Light Mode Toggle
Located in the **left sidebar**, toggle between:
- **🌙 Dark Mode**: Comfortable for evening analysis
- **☀️ Light Mode**: Better for presentations

### Theme Features
- **Smooth Transitions**: No page reload needed
- **Persistent Styling**: Colors adjust automatically
- **High Contrast Text**: Excellent readability in both modes
- **Gradient Backgrounds**: Professional appearance

### Dashboard Layout
```
┌─────────────────────────────────────┐
│  🌌 Galaxy Cluster Estimator        │  <- Title with theme colors
│  [Info Box with Current Settings]   │
├─────────────────────────────────────┤
│  [📊 Analysis] [📈 Plots] [📋 Data] │  <- Tab Navigation
├─────────────────────────────────────┤
│  Results Cards with Real-time Data  │
│  - Cluster Redshift                 │
│  - Velocity Dispersion              │
│  - Dynamical Mass                   │
│  - Dark Matter Analysis             │
└─────────────────────────────────────┘
```

---

## 📖 How to Use

### Step 1: Set Query Parameters (Sidebar)
- **RA**: Right Ascension (0-360°)
- **DEC**: Declination (-90 to 90°)
- **Search Radius**: 1-30 arcminutes
- **Stellar Mass**: Per galaxy (default: 10¹¹ M☉)
- **Redshift Filter**: Outlier removal threshold (1-5σ)

### Step 2: Click "🚀 Start Analysis"
The application will:
1. Query SDSS SkyServer (queries can take 30-60 seconds)
2. Filter galaxies by redshift
3. Calculate velocity dispersion
4. Estimate cluster size
5. Compute dynamical mass
6. Assess dark matter percentage

### Step 3: Review Results
- **Analysis Tab**: Key metrics and dark matter ratios
- **Plots Tab**: Velocity distribution & mass comparison
- **Data Tab**: Download detailed galaxy table as CSV

### Step 4: Download Results
- Click **📥 Download Filtered Data** to export as CSV
- Plots are automatically saved to `./plots/` directory

---

## 🧮 The Virial Theorem

The application uses the virial theorem to estimate cluster mass:

$$M_{dyn} = \frac{3\sigma^2 R}{G}$$

**Where:**
- **M** = Dynamical mass of the cluster
- **σ** = Velocity dispersion (from spectroscopic redshifts)
- **R** = Cluster radius (derived from angular extent)
- **G** = Gravitational constant

This assumes the cluster is in gravitational equilibrium.

---

## 📁 Project Structure

```
Dynamical_mass_estimator/
│
├── app.py                            🌐 Streamlit web interface
├── examples.py                       📚 Python usage examples
├── setup.sh                          🔧 Automated setup script
├── requirements.txt                  📦 Python dependencies
│
├── src/
│   ├── cluster_analyzer.py           🔧 Core analysis module
│   └── Notebookpart.ipynb            📓 Original Jupyter notebook
│
├── venv/                             (Created by setup.sh)
│   └── lib/python3.x/site-packages/   Virtual environment
│
├── plots/                            (Auto-created)
│   └── *.png                         Saved visualizations
│
├── data/                             (Auto-created)
│   └── *.csv                         Downloaded SDSS data
│
└── Documentation
    ├── README.md                     This file
    ├── QUICKSTART.md                 5-minute setup guide
    ├── IMPLEMENTATION_GUIDE.md       Complete reference
    └── SETUP_COMPLETE.md             Summary of changes
```

---

## 🔗 Integration with Jupyter

### Using the Module in Notebooks

```python
from src.cluster_analyzer import ClusterAnalyzer

# Create analyzer instance
analyzer = ClusterAnalyzer()

# Query SDSS
df = analyzer.query_sdss(ra=150, dec=2, radius_arcmin=10)

# Run complete analysis
results = analyzer.run_full_analysis(
    ra=150,
    dec=2,
    radius_arcmin=10,
    stellar_mass=1e11
)

# Access results
print(f"Dynamical Mass: {results['dynamical_mass']:.2e} M☉")
print(f"Dark Matter Ratio: {results['dark_matter_ratio']:.1f}x")
```

---

## 📊 Example Analysis

### Sample Galaxies Clusters

| Cluster | RA | DEC | Type | Complexity |
|---------|----|----|------|-----------|
| Coma | 194.95° | 27.96° | nearby | ⭐⭐⭐ |
| Virgo | 187.71° | 12.39° | closest | ⭐⭐ |
| Fornax | 56.11° | -35.47° | southern | ⭐⭐ |
| Perseus | 49.95° | 41.51° | rich | ⭐⭐⭐ |

Try these coordinates in the web UI sidebar!

---

## 🛠️ Technical Details

### Dependencies
- **numpy, pandas**: Data manipulation
- **matplotlib, seaborn**: Visualization
- **astropy**: Astronomical constants
- **requests**: API queries to SDSS
- **streamlit**: Web interface framework

### Requirements
- Python 3.8+
- Internet connection (for SDSS queries)
- ~2GB disk space (for dependencies)

### System Support
- Linux ✅
- macOS ✅
- Windows ✅ (with WSL or native Python)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" on setup.sh | Run: `chmod +x setup.sh` |
| "streamlit not found" | Activate venv: `source venv/bin/activate` |
| "SDSS query fails" | Check internet; SDSS servers may be temporarily down |
| "No data returned" | Check coordinates; ensure SDSS covers that region |
| "ModuleNotFoundError" | Run setup.sh again: `./setup.sh` |

---

## 📝 References

- **Virial Theorem**: Press & Schecter (1974)
- **SDSS DR16**: https://www.sdss.org/
- **Spectroscopic Redshifts**: https://asdf.readthedocs.io/
- **Galaxy Clusters**: https://en.wikipedia.org/wiki/Galaxy_cluster

---

## 📧 Usage

This project demonstrates:
- ✅ Connecting Jupyter notebooks with web UIs
- ✅ Building interactive dashboards with Streamlit
- ✅ Astronomical data analysis workflows
- ✅ Python module architecture for science
- ✅ Dark/light mode UI implementation

---

## 📄 License

Licensed for educational and research purposes.

---

## ✅ Verification

After setup, verify everything works:

```bash
# Check virtual environment
ls venv/

# Test imports
python3 -c "from src.cluster_analyzer import ClusterAnalyzer; print('✅ Module loaded')"

# Start the UI
streamlit run app.py
```

All checks pass? **Ready to analyze!** 🌌✨

