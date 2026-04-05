# 🚀 Quick Start Guide

## Installation

### Step 1: Install Dependencies
```bash
cd Dynamical_mass_estimator
pip install -r requirements.txt
```

### Step 2: Run the Web UI
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🎯 How to Use

### 1. **Set Parameters** (Left Sidebar)
   - **RA (Right Ascension)**: Cluster center's RA coordinate (0-360°)
   - **DEC (Declination)**: Cluster center's DEC coordinate (-90 to 90°)
   - **Search Radius**: How far to search from cluster center (1-30 arcmin)
   - **Stellar Mass**: Assumed stellar mass per galaxy (default: 1×10¹¹ M☉)
   - **Redshift Filter**: Outlier removal threshold (1-5σ)

### 2. **Start Analysis**
   Click the **🚀 Start Analysis** button. The app will:
   - Query SDSS DR16 SkyServer
   - Filter galaxies by redshift
   - Calculate velocity dispersion
   - Estimate cluster diameter
   - Compute dynamical mass using the virial theorem
   - Compare luminous vs dark matter

### 3. **View Results**
   - **Analysis Tab**: Summary metrics and dark matter analysis
   - **Plots Tab**: Velocity distribution & mass comparison charts
   - **Data Tab**: Download filtered galaxy data as CSV

---

## 📊 Understanding the Results

### Key Metrics:

- **Cluster Redshift (z)**: Distance indicator (higher z = farther away)
- **Velocity Dispersion (σ)**: Spread in galaxy motions (higher σ = more massive)
- **Dynamical Mass**: Total mass from virial theorem
- **Luminous Mass**: Visible matter (stars) only
- **Dark Matter Factor**: Ratio of total to visible mass
- **Dark Matter Fraction**: Percentage of mass that's invisible

### The Virial Theorem:
$$M_{dyn} = \\frac{3σ^2 R}{G}$$

This assumes the cluster is in gravitational equilibrium.

---

## 📝 Example Coordinates

Try these famous galaxy clusters:

| Cluster | RA | DEC | Notes |
|---------|----|----|-------|
| Coma Cluster | 194.95 | 27.96 | Nearby, well-studied |
| Virgo | 187.71 | 12.39 | Closest major cluster |
| Fornax | 56.11 | -35.47 | Southern hemisphere |

---

## 🔗 Integration with Jupyter Notebook

The core analysis functions are in `src/cluster_analyzer.py`:

```python
from src.cluster_analyzer import ClusterAnalyzer

# Create analyzer instance
analyzer = ClusterAnalyzer()

# Run full pipeline
results = analyzer.run_full_analysis(
    ra=150.0,
    dec=2.0,
    radius_arcmin=10,
    stellar_mass=1e11
)

# Access results
print(f"Dynamical Mass: {results['dynamical_mass']:.2e} M☉")
print(f"Dark Matter Ratio: {results['dark_matter_ratio']:.1f}x")
```

Can also be used directly in the Jupyter notebook:

```python
from src.cluster_analyzer import ClusterAnalyzer

analyzer = ClusterAnalyzer()
df = analyzer.query_sdss(ra=150, dec=2, radius_arcmin=10)
```

---

## 📂 Project Structure

```
Dynamical_mass_estimator/
├── app.py                      # 🌐 Streamlit web interface
├── src/
│   ├── cluster_analyzer.py     # 🔧 Core analysis module
│   └── Notebookpart.ipynb      # 📓 Original Jupyter notebook
├── requirements.txt            # 📦 Dependencies
├── plots/                      # 📊 Generated visualizations
├── data/                       # 💾 Downloaded SDSS data
└── README.md                   # 📖 Documentation
```

---

## 🐛 Troubleshooting

### "Connection Error: SDSS Query Failed"
- Check your internet connection
- The SDSS server might be temporarily unavailable
- Try again in a few moments

### "ModuleNotFoundError: No module named 'streamlit'"
- Run: `pip install -r requirements.txt`

### "No data returned from SDSS"
- The coordinates might not have enough galaxies
- Try adjusting the search radius or coordinates

---

## 📖 References

- **SDSS DR16**: https://www.sdss.org/
- **Virial Theorem**: Press & Schecter (1974)
- **Velocity Dispersion**: Spectroscopic Redshift Analysis

---

## 📧 Notes

This application connects:
1. ✅ **Web UI (Streamlit)** - Interactive interface
2. ✅ **Python Module** - Reusable analysis functions
3. ✅ **Jupyter Notebook** - Original workflow
4. ✅ **SDSS Database** - Real astronomical data

Use the Streamlit app for interactive analysis, or import `ClusterAnalyzer` in your own scripts/notebooks.
