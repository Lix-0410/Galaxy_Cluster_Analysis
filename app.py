# app.py
import streamlit as st
from analysis import analyze_galaxy_cluster

st.set_page_config(
    layout="wide",
    page_title="Galaxy Cluster Analyzer",
    page_icon="🔭"
)

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            background-color: #f4f6f8;
            color: #2c3e50;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
        }

        .main {
            padding: 2rem;
        }

        h1, h2, h3 {
            color: #1a2e3b;
            font-weight: 600;
        }

        .stButton>button {
            background-color: #1f77b4;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 0.5em 1.2em;
            font-size: 1rem;
            font-weight: 500;
            transition: background-color 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #155a91;
        }

        img {
            display: block;
            margin: 1.5rem auto;
            max-width: 95%;
            border-radius: 12px;
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        }

        .block-container {
            padding: 1.5rem 2.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Upload UI ---
st.title("🔭 Galaxy Cluster Analyzer")
st.markdown("Upload your astronomical CSV file to analyze galaxy cluster properties and view statistical visualizations.")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

# --- File Processing ---
if uploaded_file:
    try:
        st.write("📡 Reading and processing data...")
        results, plots = analyze_galaxy_cluster(uploaded_file)

        # --- Results in Metric Columns ---
        st.markdown("### 📊 Computed Results")

        pretty_names = {
            "mean_specz": "Mean Redshift",
            "std_specz": "Redshift Std. Dev.",
            "lower_bound": "Lower Redshift Bound",
            "upper_bound": "Upper Redshift Bound",
            "velocity_dispersion_km_s": "Velocity Dispersion (km/s)",
            "theta_arcmin": "Max Angular Size (arcmin)",
            "angular_diameter_distance_mpc": "Angular Diameter Dist. (Mpc)",
            "physical_diameter_mpc": "Physical Diameter (Mpc)",
            "dynamical_mass_solar": "Dynamical Mass (Solar Masses)"
        }

        result_items = [(pretty_names.get(k, k), v) for k, v in results.items()]
        n_cols = 3

        for i in range(0, len(result_items), n_cols):
            cols = st.columns(n_cols)
            for col, (label, val) in zip(cols, result_items[i:i + n_cols]):
                if "mass" in label.lower():
                    col.metric(label, f"{val:.2e}")
                else:
                    col.metric(label, f"{val:.4f}")
        
        # --- View Formulas Section ---
        st.markdown("### 📐 Want to know the math behind the results?")
        if st.button("📘 View Formulas"):
            st.markdown("""
            <style>
                .formula-title {
                    background-color: #f0f4f8;
                    padding: 0.6rem 1rem;
                    border-left: 5px solid #1f77b4;
                    border-radius: 6px;
                    margin-top: 1rem;
                    margin-bottom: 0.2rem;
                    font-weight: bold;
                }
            </style>
            """, unsafe_allow_html=True)

            # Display formulas directly
            st.markdown('<div class="formula-title">🔹 1. Velocity from Redshift</div>', unsafe_allow_html=True)
            st.latex(r"v = z \times c")

            st.markdown('<div class="formula-title">🔹 2. Velocity Dispersion</div>', unsafe_allow_html=True)
            st.latex(r"\sigma = c \cdot \frac{(1+z)^2 - (1+\bar{z})^2}{(1+z)^2 + (1+\bar{z})^2}")

            st.markdown('<div class="formula-title">🔹 3. Angular Diameter Distance</div>', unsafe_allow_html=True)
            st.latex(r"DA = \frac{r}{1 + \bar{z}}")
            st.markdown("where:")
            st.latex(r"r = \frac{c \cdot \bar{z}}{H_0} \left(1 - \frac{\bar{z}}{2}(1 + q_0)\right)")

            st.markdown('<div class="formula-title">🔹 4. Physical Diameter</div>', unsafe_allow_html=True)
            st.latex(r"D = \theta \cdot DA")

            st.markdown('<div class="formula-title">🔹 5. Dynamical Mass</div>', unsafe_allow_html=True)
            st.latex(r"M_{\mathrm{dyn}} = \frac{3 \cdot \sigma^2 \cdot R}{G}")



        # --- Plots in Grid Layout ---
        st.markdown("---")
        st.markdown("### 🖼️ Visualizations")
        st.markdown("Each plot below shows a characteristic feature of your galaxy cluster data:")

        plots_per_row = 2
        plot_items = list(plots.items())

        for i in range(0, len(plot_items), plots_per_row):
            cols = st.columns(plots_per_row)
            for col, (plot_key, img_base64) in zip(cols, plot_items[i:i + plots_per_row]):
                label = plot_key.replace('_', ' ').capitalize()
                col.subheader(f"📌 {label}")
                col.image(f"data:image/png;base64,{img_base64}", use_container_width=True)
                col.caption(f"Figure: {label}")


    except Exception as e:
        st.error(f"❌ Error processing the file: {e}")
else:
    st.info("👆 Please upload a CSV file with columns: `objid`, `specz`, `ra`, `dec`, and `proj_sep`.")
