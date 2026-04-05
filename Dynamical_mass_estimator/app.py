"""
Streamlit Web UI for Dynamical Mass Estimator

This application provides an interactive interface to estimate galaxy cluster
masses using SDSS data and the virial theorem.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cluster_analyzer import ClusterAnalyzer

# Custom HTML for Google Fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)


# Page configuration with theme support
st.set_page_config(
    page_title="Dynamical Mass Estimator",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com",
        "Report a bug": "https://github.com",
        "About": "Dynamical Mass Estimator for Galaxy Clusters"
    }
)

# Initialize Session States
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'console_logs' not in st.session_state:
    st.session_state.console_logs = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'

# Sidebar Theme Toggle (Moved up for reactivity)
with st.sidebar:
    st.markdown('<div class="sidebar-header">UI PREFERENCES</div>', unsafe_allow_html=True)
    theme_options = ["🌙 Dark Mode", "☀️ Light Mode"]
    selected_theme = st.radio("ThemeSelect", theme_options, label_visibility="collapsed", index=0 if st.session_state.theme_mode == 'dark' else 1)
    st.session_state.theme_mode = "dark" if "Dark" in selected_theme else "light"

# Dynamic Palette Definition
if st.session_state.theme_mode == "dark":
    p_bg = "#020617"          # Deepest Slate
    s_bg = "#0F172A"          # Surface Slate
    acc_blue = "#38BDF8"      # Bright Precision Blue
    acc_emerald = "#10B981"   # Scientific Emerald
    txt_main = "#F8FAFC"      # Slate White
    txt_mute = "#64748B"      # Muted Slate
    brd = "rgba(255, 255, 255, 0.05)"
    shd = "0 4px 6px -1px rgba(0, 0, 0, 0.5)"
else:
    p_bg = "#F8FAFC"          # Light Slate
    s_bg = "#FFFFFF"          # Pure White
    acc_blue = "#0284C7"      # Deep Precision Blue
    acc_emerald = "#059669"
    txt_main = "#0F172A"      # Deep Slate Text
    txt_mute = "#475569"
    brd = "rgba(0, 0, 0, 0.08)"
    shd = "0 4px 6px -1px rgba(0, 0, 0, 0.1)"

# Plotly Theme Sync
plotly_tpl = "plotly_dark" if st.session_state.theme_mode == "dark" else "plotly_white"
p_grid = "rgba(255,255,255,0.05)" if st.session_state.theme_mode == "dark" else "rgba(0,0,0,0.05)"

# Redesign 2.0: Celestial Precision CSS System (A-tier Minimalist)
st.markdown(f"""
    <style>
    :root {{
        --bg-primary: {p_bg};
        --bg-secondary: {s_bg};
        --accent-blue: {acc_blue};
        --accent-emerald: {acc_emerald};
        --text-primary: {txt_main};
        --text-secondary: {txt_mute};
        --border-primary: {brd};
        --shadow-main: {shd};
        --font-main: 'Inter', sans-serif;
        --font-code: 'JetBrains Mono', monospace;
        --font-hand: 'Caveat', cursive;
    }}

    /* Base Layout */
    .stApp {{
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: var(--font-main);
    }}

    /* Typography */
    h1, h2, h3 {{ font-weight: 700 !important; letter-spacing: -0.025em; }}
    h1 {{ font-size: 2.25rem !important; margin-bottom: 2rem !important; border: none !important; color: var(--text-primary) !important; }}
    h2 {{ font-size: 1.125rem !important; text-transform: uppercase; color: var(--accent-blue) !important; letter-spacing: 0.05em; border: none !important; padding: 0 !important; margin-bottom: 1.5rem !important; }}

    /* Bento Cards */
    .bento-card {{
        background: var(--bg-secondary);
        border: 1px solid var(--border-primary);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow-main);
        transition: all 0.2s ease;
        margin-bottom: 1rem;
    }}
    .bento-card:hover {{ border-color: var(--accent-blue); }}

    /* Telemetry Labels */
    .telemetry-label {{
        font-family: var(--font-code);
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }}
    .telemetry-value {{
        font-family: var(--font-code);
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
    }}

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {{
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-primary);
    }}
    .sidebar-header {{
        font-family: var(--font-code);
        font-size: 0.7rem;
        color: var(--accent-blue);
        letter-spacing: 0.2em;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border-primary);
    }}

    /* Scientific Console */
    .status-console {{
        background: #000000;
        border-radius: 4px;
        padding: 1rem;
        font-family: var(--font-code);
        font-size: 0.8rem;
        color: #A3E635; /* Terminal Lime */
        border: 1px solid #1E293B;
        height: 200px;
        overflow-y: auto;
        margin-top: 2rem;
    }}
    .console-line {{ margin-bottom: 0.25rem; display: flex; gap: 0.5rem; }}
    .console-timestamp {{ color: #475569; }}

    /* Button Reset */
    .stButton > button {{
        background: var(--accent-blue) !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        width: 100% !important;
        transition: background 0.2s ease !important;
    }}
    .stButton > button:hover {{ background: #2563EB !important; }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{ background: var(--bg-secondary); border-radius: 8px 8px 0 0; padding: 0.5rem 1rem 0 1rem; }}
    .stTabs [data-baseweb="tab"] {{ color: var(--text-secondary) !important; font-weight: 600 !important; }}
    .stTabs [aria-selected="true"] {{ color: var(--accent-blue) !important; border-bottom: 2px solid var(--accent-blue) !important; background: transparent !important; }}

    /* Tooltip Fixes */
    div[data-testid="stTooltipIcon"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# Initialize Other Session States (Already handled above)
# ... removed duplicates

def log_to_console(message):
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.console_logs.append(f'<div class="console-line"><span class="console-timestamp">[{timestamp}]</span> {message}</div>')

def custom_metric(label, value, unit=""):
    """Render a minimalist scientific readout card."""
    st.markdown(f"""
    <div class="bento-card">
        <div class="telemetry-label">{label}</div>
        <div class="telemetry-value">{value}<span style="font-size: 0.8rem; margin-left: 0.5rem; color: var(--text-secondary);">{unit}</span></div>
    </div>
    """, unsafe_allow_html=True)

# Main Title
st.markdown("<h1>CELESTIAL PRECISION</h1>", unsafe_allow_html=True)
st.markdown('<p style="color: var(--text-secondary); margin-top: -1.5rem; margin-bottom: 2rem;">Dynamical Mass Estimator Analysis Portal</p>', unsafe_allow_html=True)

# Sidebar (Continued)
with st.sidebar:
    st.markdown("---")
    st.header("Spectroscopic Parameters")
    ra = st.number_input("Right Ascension (RA)", value=150.0)
    dec = st.number_input("Declination (DEC)", value=2.0)
    radius = st.slider("Search Radius (arcmin)", 1, 30, 10)
    
    st.markdown("---")
    st.header("Algorithmic Constraints")
    stellar_mass = st.number_input("Galaxy Mass (M☉)", value=1e11, format="%.2e")
    sigma_cutoff = st.slider("Redshift Filter (σ)", 1, 5, 3)

# Main content area
tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📈 Plots", "📋 Data"])

with tab1:
    st.header("Analysis Console")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="bento-card">
            <div class="telemetry-label">Mission Configuration</div>
            <div style="font-family: var(--font-code); font-size: 0.9rem;">
                TARGET_RA: {ra}°<br>
                TARGET_DEC: {dec}°<br>
                SEARCH_RAD: {radius}'<br>
                STELLAR_MASS: {stellar_mass:.2e} M☉
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("EXECUTE ANALYSIS SEQUENCE", use_container_width=True):
            st.session_state.analyzer = ClusterAnalyzer(plot_dir="./plots", data_dir="./data")
            log_to_console("Initializing Spectroscopic Analyzer...")
            log_to_console(f"Targeting RA={ra}, DEC={dec}")
            
            with st.spinner("QUERYING SDSS SkyServer..."):
                try:
                    log_to_console("Connecting to SDSS SkyServer DR16...")
                    results = st.session_state.analyzer.run_full_analysis(
                        ra=ra, dec=dec, radius_arcmin=radius, stellar_mass=stellar_mass
                    )
                    st.session_state.results = results
                    st.session_state.analysis_complete = True
                    log_to_console("Data acquisition synchronized.")
                    log_to_console("Virial Theorem application successful.")
                except Exception as e:
                    st.error(f"SYSTEM FAILURE: {str(e)}")
                    log_to_console(f"ERROR: {str(e)}")
    
    # Console Log Output
    if st.session_state.console_logs:
        st.markdown(f'<div class="status-console">{"".join(st.session_state.console_logs[-10:])}</div>', unsafe_allow_html=True)
    
    if st.session_state.analysis_complete and st.session_state.results:
        st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        st.header("Telemetry Output")
        
        results = st.session_state.results
        m1, m2, m3 = st.columns(3)
        with m1: custom_metric("Redshift (z)", f"{results['cluster_redshift']:.4f}")
        with m2: custom_metric("Dispersion", f"{results['velocity_dispersion']:.0f}", "km/s")
        with m3: custom_metric("Diameter", f"{results['diameter_Mpc']:.2f}", "Mpc")
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        m4, m5 = st.columns(2)
        with m4: custom_metric("Dynamical Mass", f"{results['dynamical_mass']:.2e}", "M☉")
        with m5: custom_metric("Luminous Mass", f"{results['luminous_mass']:.2e}", "M☉")
        
        # Dark matter analysis
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.subheader("🌌 DARK MATTER COMPOSITION")
        
        dm_col1, dm_col2, dm_col3 = st.columns(3)
        
        with dm_col1:
            custom_metric("DM Factor", f"{results['dark_matter_ratio']:.1f}x", "Ratio of dynamical to luminous mass")
        
        with dm_col2:
            dark_matter_mass = results['dynamical_mass'] - results['luminous_mass']
            custom_metric("DM Mass", f"{dark_matter_mass:.2e} M☉")
        
        with dm_col3:
            dark_matter_fraction = (dark_matter_mass / results['dynamical_mass']) * 100
            custom_metric("DM Percentage", f"{dark_matter_fraction:.1f}%")
        
        # Scientific Summary Stats
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        st.header("Algorithmic Diagnostics")
        diag1, diag2 = st.columns(2)
        with diag1:
            st.markdown(f'<div class="bento-card"><div class="telemetry-label">Member Count</div><div class="telemetry-value">{results["num_galaxies"]}</div></div>', unsafe_allow_html=True)
        with diag2:
            virial_ratio = results['dynamical_mass'] / results['luminous_mass']
            st.markdown(f'<div class="bento-card"><div class="telemetry-label">Mass/Light Ratio</div><div class="telemetry-value">{virial_ratio:.1f}</div></div>', unsafe_allow_html=True)


with tab2:
    st.header("Diagnostic Visualizations")
    
    if st.session_state.analysis_complete and st.session_state.analyzer:
        analyzer = st.session_state.analyzer
        df = analyzer.filtered_df
        
        # 3D Cluster Topology
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("Spatial Cluster Topology (3D)")
        fig_3d = px.scatter_3d(
            df, x='ra', y='dec', z='specz',
            color='velocity',
            labels={'ra': 'RA', 'dec': 'DEC', 'specz': 'Z'},
            color_continuous_scale='Blues',
            template=plotly_tpl
        )
        fig_3d.update_traces(marker=dict(size=3, opacity=0.8, line=dict(width=0)))
        fig_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(gridcolor=p_grid, zerolinecolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor=p_grid, zerolinecolor='rgba(255,255,255,0.1)'),
                zaxis=dict(gridcolor=p_grid, zerolinecolor='rgba(255,255,255,0.1)'),
            )
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("Velocity Histogram")
            fig_vel = px.histogram(
                df, x='velocity', nbins=30,
                color_discrete_sequence=['#3B82F6'],
                template=plotly_tpl
            )
            fig_vel.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                bargap=0.1,
                xaxis=dict(gridcolor=p_grid),
                yaxis=dict(gridcolor=p_grid)
            )
            st.plotly_chart(fig_vel, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with p_col2:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("Mass Distribution")
            m_data = pd.DataFrame({
                'Source': ['Luminous', 'Dynamical'],
                'Mass (M☉)': [st.session_state.results['luminous_mass'], st.session_state.results['dynamical_mass']]
            })
            fig_mass = px.bar(
                m_data, x='Source', y='Mass (M☉)',
                color='Source',
                color_discrete_map={'Luminous': '#10B981', 'Dynamical': '#3B82F6'},
                log_y=True,
                template=plotly_tpl
            )
            fig_mass.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                xaxis=dict(gridcolor=p_grid),
                yaxis=dict(gridcolor=p_grid)
            )
            st.plotly_chart(fig_mass, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="bento-card"><strong>ℹ️ ANALYZER_IDLE:</strong> Execute analysis sequence to generate diagnostic visualizations.</div>', unsafe_allow_html=True)


with tab3:
    st.header("Spectroscopic Datastream")
    
    if st.session_state.analysis_complete and st.session_state.analyzer:
        analyzer = st.session_state.analyzer
        
        if analyzer.filtered_df is not None:
            st.markdown(f"""
            <div class="bento-card">
                <div class="telemetry-label">Datastream Status</div>
                <div style="font-family: var(--font-code); color: var(--accent-emerald);">SYNC_COMPLETE // {len(analyzer.filtered_df)} objects identified</div>
            </div>
            """, unsafe_allow_html=True)
            
            display_cols = ['ra', 'dec', 'specz', 'velocity', 'proj_sep']
            available_cols = [col for col in display_cols if col in analyzer.filtered_df.columns]
            
            st.dataframe(
                analyzer.filtered_df[available_cols].head(100),
                use_container_width=True,
                height=400
            )
            
            csv = analyzer.filtered_df[available_cols].to_csv(index=False)
            st.download_button(
                label="EXPORT TELEMETRY (CSV)",
                data=csv,
                file_name="cluster_precision_data.csv",
                mime="text/csv"
            )
    else:
        st.markdown('<div class="bento-card"><strong>ℹ️ STREAM_OFFLINE:</strong> Execute analysis to populate data grid.</div>', unsafe_allow_html=True)


# Footer - Theoretical Architecture Section
st.markdown('<div style="height: 5rem;"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style="padding: 2.5rem; border-radius: 12px; background: {s_bg}; border: 1px solid {brd}; box-shadow: {shd};">
    <div style="color: {acc_blue}; font-family: var(--font-main); font-size: 0.75rem; letter-spacing: 0.2em; font-weight: 700; margin-bottom: 1.5rem; text-transform: uppercase;">
        Theoretical Architecture & Physics Model
    </div>
    <p style="font-family: var(--font-main); font-size: 0.9rem; color: {txt_mute}; line-height: 1.8; margin-bottom: 2rem;">
        This workstation implements the <strong>Virial Theorem</strong> algorithmic framework for large-scale structure mass estimation. 
        By deriving the line-of-sight velocity dispersion and approximating the structural gravitational radius, we estimate the total dynamical mass required for gravitational stability.
    </p>
    <!-- Handwritten Formula Card -->
    <div style="background: rgba(0,0,0,0.2); padding: 2rem; border-radius: 8px; border: 1px dashed {brd}; position: relative; margin-bottom: 2.5rem;">
        <div style="position: absolute; top: -10px; left: 20px; background: {s_bg}; padding: 0 10px; font-family: var(--font-code); font-size: 0.65rem; color: {acc_blue};">
            RESEARCH_NOTE // RE-V2.0
        </div>
        <div style="font-family: var(--font-hand); font-size: 2.5rem; color: {acc_emerald}; text-align: center; letter-spacing: 2px;">
            M<sub style="font-size: 1rem;">dyn</sub> = <span style="display: inline-block; vertical-align: middle; text-align: center;">
                <span style="display: block; border-bottom: 2px solid {acc_emerald}; padding: 0 10px;">3σ²R</span>
                <span style="display: block; padding-top: 5px;">G</span>
            </span>
        </div>
    </div>
    <!-- Data Specs Grid -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; border-top: 1px solid {brd}; padding-top: 2rem;">
        <div>
            <div style="color: {txt_main}; font-family: var(--font-code); font-size: 0.65rem; letter-spacing: 0.15em; font-weight: 700; margin-bottom: 0.5rem;">
                FEDERATED DATA SOURCE
            </div>
            <div style="font-family: var(--font-code); font-size: 0.85rem; color: {txt_mute};">
                SDSS SKY-SERVER DR16 // DR17-BETA
            </div>
        </div>
        <div>
            <div style="color: {txt_main}; font-family: var(--font-code); font-size: 0.65rem; letter-spacing: 0.15em; font-weight: 700; margin-bottom: 0.5rem;">
                ANALYTIC SPECIFICATION
            </div>
            <div style="font-family: var(--font-code); font-size: 0.85rem; color: {txt_mute};">
                VIRIAL_MASS_ESTIMATOR_V2.0
            </div>
        </div>
    </div>
    <div style="text-align: right; margin-top: 2rem; font-family: var(--font-code); font-size: 0.6rem; color: {txt_mute}; opacity: 0.5; letter-spacing: 2px;">
        INSTRUMENT_SERIAL_NO: 7741-CP-09 // FOR OFFICIAL RESEARCH ONLY
    </div>
</div>
""", unsafe_allow_html=True)

