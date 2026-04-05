# 🌌 Dynamical Mass Estimator for Galaxy Clusters - Complete Implementation

A professional **Web-Based and Python** system to estimate galaxy cluster masses using SDSS data and the virial theorem. Connects the original Jupyter notebook with an interactive Streamlit web UI and reusable Python modules.

## ✨ What's Included

### 🌐 Web UI (Streamlit App)
**File**: `app.py`
- Interactive parameter input interface
- Real-time SDSS data queries
- Instant visualizations
- Download capability for results
- Professional dashboard with 3 tabs: Analysis • Plots • Data

### 🔧 Python Module
**File**: `src/cluster_analyzer.py`
- `ClusterAnalyzer` class with complete analysis pipeline
- Easy integration with Jupyter notebooks
- Reusable functions for custom workflows
- Full documentation and examples

### 📓 Original Notebook
**File**: `src/Notebookpart.ipynb`
- Original workflow preserved
- Now can use imported functions instead of duplicating code
- Can be enhanced with web UI results

### 📚 Documentation
- `QUICKSTART.md` - Step-by-step setup guide
- `examples.py` - Code examples for Python usage
- `setup.sh` - Automated installation script
- This README with full reference

---

## 🚀 Quick Start

### 1. One-Line Setup (Automated)
```bash
cd Dynamical_mass_estimator
chmod +x setup.sh
./setup.sh
```

### 2. Manual Setup
```bash
# Clone/navigate to project
cd Dynamical_mass_estimator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Web UI
```bash
streamlit run app.py
```
Opens automatically in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Option A: Web UI (No Coding Required)
1. Set cluster coordinates (RA, DEC) in the sidebar
2. Adjust search radius if needed
3. Click **Start Analysis**
4. View results in 3 tabs: Analysis • Plots • Data
5. Download results as CSV

### Option B: Python/Jupyter Integration
```python
from src.cluster_analyzer import ClusterAnalyzer

# Quick analysis
analyzer = ClusterAnalyzer()
results = analyzer.run_full_analysis(
    ra=150.0,
    dec=2.0, 
    radius_arcmin=10
)

# Access results
print(f"Mass: {results['dynamical_mass']:.2e} M☉")
print(f"Dark Matter: {results['dark_matter_ratio']:.1f}x")
```

### Option C: Enhanced Notebook Workflow
```python
# In Jupyter, use the module functions instead of duplicating code
from src.cluster_analyzer import ClusterAnalyzer

analyzer = ClusterAnalyzer()
df = analyzer.query_sdss(ra=150, dec=2, radius_arcmin=10)
analyzer.average_by_objid()
# ... etc, then visualize with your notebook cells
```

---

## 📊 Features

### Analysis Capabilities
- ✅ Query SDSS DR16 SkyServer for galaxies
- ✅ Filter by spectroscopic redshift (3-sigma outlier removal)
- ✅ Calculate velocity dispersion
- ✅ Estimate cluster diameter from angular extent
- ✅ Compute dynamical mass using virial theorem
- ✅ Assess dark matter content
- ✅ Generate publication-ready plots

### User Interface
- ✅ Interactive sidebar parameters
- ✅ Real-time progress indicators
- ✅ 3-tab dashboard (Analysis • Plots • Data)
- ✅ Key metrics with tooltips
- ✅ Download data as CSV
- ✅ Responsive dark mode support

### Python API
- ✅ `ClusterAnalyzer` class for automation
- ✅ Individual functions for custom workflows
- ✅ Batch processing capability
- ✅ Integration with Jupyter notebooks
- ✅ Full docstrings and type hints

---

## 📁 Project Structure

```
Dynamical_mass_estimator/
│
├── app.py                      # 🌐 Streamlit web interface
├── examples.py                 # 📚 Python usage examples
├── setup.sh                    # 🔧 Automated setup
├── requirements.txt            # 📦 Dependencies
│
├── src/
│   ├── cluster_analyzer.py     # 🔧 Core analysis module (NEW)
│   └── Notebookpart.ipynb      # 📓 Original notebook
│
├── plots/                      # 📊 Generated visualizations (auto-created)
├── data/                       # 💾 Downloaded SDSS data (auto-created)
│
├── QUICKSTART.md               # ⚡ 5-minute setup guide
├── README.md                   # 📖 This file
└── IMPLEMENTATION_GUIDE.md     # 🎯 Architecture details
```

---

## 📊 Analysis Pipeline

### The Virial Theorem Approach

```
Query SDSS Data (RA, DEC, Radius)
         ↓
Average by Object ID
         ↓
Filter Outliers (3-sigma redshift cut)
         ↓
Calculate Velocity Dispersion (σ)
    from spectroscopic redshifts
         ↓
Estimate Angular Diameter Distance
    based on cluster redshift
         ↓
Convert Angular Extent → Physical Diameter
         ↓
Apply Virial Theorem: M = (3σ²R)/G
         ↓
Compare to Luminous Mass (Stars)
         ↓
Quantify Dark Matter Content
```

### Key Equation
$$M_{dyn} = \\frac{3σ^2 R}{G}$$

Where:
- **M** = Dynamical mass
- **σ** = Velocity dispersion (km/s)
- **R** = Cluster radius (meters)
- **G** = Gravitational constant

---

## 🔗 Connection to Jupyter Notebook

### Before (Original Workflow)
```
Jupyter Notebook.ipynb
  └─ All analysis code in cells
  └─ Functions duplicated
  └─ Web UI: Manual separate effort
```

### After (New Integration)
```
Notebook.ipynb ←──┐
                  │
                  ├─ imports cluster_analyzer.py
                  │
App.py (Streamlit) │
                  │
examples.py ──────┘

All share same ClusterAnalyzer class
```

### Use the Module in Notebook
Replace your notebook code with:
```python
from src.cluster_analyzer import ClusterAnalyzer

analyzer = ClusterAnalyzer()

# Instead of: df = query_sdss(...) 
# Now use:
df = analyzer.query_sdss(ra=150, dec=2, radius_arcmin=10)

# Instead of: filtered_df = ... (manual filtering)
# Now use:
filtered_df, z_min, z_max, m_z, s_z = analyzer.filter_by_redshift(sigma=3)
```

---

## 🎯 Web UI Navigation

### Analysis Tab
- **Sidebar**: Input parameters (RA, DEC, radius, etc.)
- **Run Button**: Executes complete pipeline
- **Results**: 6 metric cards showing key findings
- **Dark Matter Analysis**: 3 additional cards with insights

### Plots Tab
- **Velocity Distribution**: Histogram of galaxy velocities
- **Mass Comparison**: Bar chart (Luminous vs Dynamical)
- Auto-refreshes after each analysis

### Data Tab
- **Galaxy Table**: First 50 galaxies with relevant columns
- **Download Button**: Export filtered data as CSV
- **Statistics**: Summary information

---

## 💻 PyPI-Style Installation (Future)

Once packaged:
```bash
pip install dynamical-mass-estimator
```

Then use anywhere:
```python
from dynamical_mass_estimator import ClusterAnalyzer
```

---

## 🔬 Example Coordinates

Ready-to-use cluster coordinates:

| Cluster | RA | DEC | Complexity |
|---------|----|----|-----------|
| Coma | 194.95° | 27.96° | ⭐⭐⭐ |
| Virgo | 187.71° | 12.39° | ⭐⭐ |
| Fornax | 56.11° | -35.47° | ⭐⭐ |
| Perseus | 49.95° | 41.51° | ⭐⭐⭐ |
| Hercules | 229.20° | 12.31° | ⭐⭐⭐ |

**Note**: Search results depend on SDSS coverage and data availability.

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `numpy`, `pandas` | Data manipulation |
| `matplotlib`, `seaborn` | Visualization |
| `astropy` | Astronomy constants & utilities |
| `requests` | URL queries to SDSS |
| `streamlit` | 🌐 Web UI framework |
| `plotly` | Interactive plots |

See `requirements.txt` for versions.

---

## 🐛 Troubleshooting

### Issue: "SDSS Query Failed"
**Solution**: Internet connection check. SDSS servers occasionally go down. Retry after 5 minutes.

### Issue: "No module named cluster_analyzer"
**Solution**: Ensure you're in the `Dynamical_mass_estimator` directory and have run the setup.

### Issue: "streamlit: command not found"
**Solution**: Run `pip install -r requirements.txt` again, or activate the virtual environment: `source venv/bin/activate`

### Issue: No data returned
**Solution**: 
- Try different coordinates
- Increase search radius
- Check that SDSS covers those coordinates

---

## 🔄 Development Roadmap

Potential enhancements:
- [ ] Support for other surveys (GAMA, 2dF, etc.)
- [ ] Interactive cluster visualization (3D scatter plot)
- [ ] Export analysis to LaTeX format
- [ ] Batch cluster processing from CSV input
- [ ] Add uncertainty quantification
- [ ] Docker containerization
- [ ] Cloud deployment templates
- [ ] REST API for automation

---

## 📝 Citation & References

If you use this tool in research, cite:

```bibtex
@software{dyn_mass_2024,
  title={Dynamical Mass Estimator for Galaxy Clusters},
  year={2024},
  note={Web UI + Python module for SDSS-based mass estimation}
}
```

**Primary References**:
- Press & Schecter (1974) - Virial theorem application
- SDSS DR16 Documentation: https://www.sdss.org/
- Spectroscopic Redshift Analysis: https://asdf.readthedocs.io/

---

## 📧 Support & Feedback

- **Questions?** Check `QUICKSTART.md` and `examples.py`
- **Bug reports?** Test with the example coordinates first
- **Feature requests?** The codebase is modular and extensible

---

## 📄 License

This project demonstrates data science workflows combining:
- Jupyter notebooks
- Python modules
- Web UI with Streamlit
- Scientific computing

Licensed for educational and research purposes.

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] `python3 -c "import streamlit"` - No errors
- [ ] `python3 -c "from src.cluster_analyzer import ClusterAnalyzer"` - No errors
- [ ] `streamlit run app.py` - Opens web UI
- [ ] Can adjust parameters in sidebar
- [ ] Plots directory exists: `ls plots/`
- [ ] Data directory exists: `ls data/`

**All checkmarks = Ready to analyze!** ✨

---

## 🎓 Learning Outcomes

By exploring this codebase, you'll learn:
- ✅ Connecting Jupyter notebooks with web UIs
- ✅ Object-oriented Python design for scientific computing
- ✅ Streamlit for rapid dashboard creation
- ✅ API integration (SDSS SkyServer)
- ✅ Astronomical data analysis workflows
- ✅ Virial theorem applications

---

**Happy Cluster Analyzing!** 🌌✨
