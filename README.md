# 🔭 Galaxy Cluster Analyzer

A minimalist and interactive web application built with **Streamlit** to analyze galaxy cluster data. Upload your astronomical CSV data and get automatic visualizations and computations of key astrophysical properties like redshift distribution, velocity dispersion, angular diameter distance, and dynamical mass.

---
## 🚀 Features

- 📁 Upload galaxy cluster data (CSV)
- 📊 Visualizations:
  - Redshift distribution (boxplot + histograms)
  - Filtered redshift histogram
  - Velocity distribution
  - Angular separation histogram
- 🧠 Astrophysical calculations:
  - Mean and std. deviation of redshift
  - Velocity dispersion
  - Angular diameter distance (DA)
  - Physical diameter of the cluster
  - Dynamical mass estimation in solar masses
- 📐 Optional "View Formulas" button with LaTeX-rendered equations
- 🌙 Clean UI with metric blocks and minimal styling

---
## 🗂️ Project Structure
```plaintext
galaxy_cluster/
├── README.md # 
├── app.py # Main streamlit interface
├── analysis.py # Core analysis and plotting
├── requirements.txt # Dependencies list
└── skyserver_data #dataset used
```



