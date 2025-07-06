import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from astropy.constants import G as G_astropy, c as c_astropy, M_sun
from astropy.cosmology import Planck18 as cosmo
from astropy.coordinates import SkyCoord
import astropy.units as u
import io
import base64

# Convert matplotlib plot to base64-encoded string for display
def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()
    return image_base64

def analyze_galaxy_cluster(file):
    H_0 = cosmo.H0.to('1/s')
    c_val = c_astropy.to('m/s').value
    G_SI = G_astropy.value  # G in m^3 / kg / s^2
    q0 = -0.534
    H0 = cosmo.H0.value
    c_kms = c_astropy.to('km/s').value

    df = pd.read_csv(file)

    required_cols = {'objid', 'specz', 'ra', 'dec', 'proj_sep'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Uploaded file must contain these columns {required_cols}")

    averaged_df = df.groupby('objid').agg({
        'specz': 'mean',
        'ra': 'first',
        'dec': 'first',
        'proj_sep': 'first'
    }).reset_index()

    mean_specz = averaged_df['specz'].mean()
    std_specz = averaged_df['specz'].std()
    lower_bound = mean_specz - 3 * std_specz
    upper_bound = mean_specz + 3 * std_specz

    filtered_df = averaged_df[(averaged_df['specz'] >= lower_bound) & (averaged_df['specz'] <= upper_bound)].copy()
    averaged_df['velocity'] = averaged_df['specz'] * c_val

    z_cluster = filtered_df['specz'].mean()
    z = filtered_df['specz']
    disp = c_val * ((1 + z)**2 - (1 + z_cluster)**2) / ((1 + z)**2 + (1 + z_cluster)**2)
    disp = disp / 1000  # Convert m/s to km/s
    vel_disp = np.std(disp)

    ra_list = averaged_df['ra'].values
    dec_list = averaged_df['dec'].values
    galaxies = SkyCoord(ra=ra_list * u.degree, dec=dec_list * u.degree)
    cluster_center = SkyCoord(ra=np.mean(ra_list) * u.degree, dec=np.mean(dec_list) * u.degree)
    separations = galaxies.separation(cluster_center)
    theta_arcmin = separations.to(u.arcmin).value.max()
    theta_rad = (theta_arcmin * u.arcmin).to(u.radian).value

    z_mean = averaged_df['specz'].mean()
    r = (c_kms * z_mean / H0) * (1 - (z_mean / 2) * (1 + q0))
    DA = r / (1 + z_mean)
    diameter_Mpc = DA * theta_rad

    # Convert diameter to meters (1 Mpc = 3.086e22 m)
    radius_m = (diameter_Mpc * 1e6 * 3.086e22) / 2
    vel_mps = vel_disp * 1e3
    M_dyn_kg = 3 * vel_mps**2 * radius_m / G_SI
    M_dyn_solar = M_dyn_kg / M_sun.value

    plots = {}

    plt.title("Distribution of Redshift")
    plt.boxplot(averaged_df['specz'], vert=False)
    plt.xlabel('Redshift')
    plots['boxplot'] = plot_to_base64()

    plt.title('Redshift Histogram with Bounds')
    plt.axvline(lower_bound, color='red', label='Lower Bound')
    plt.axvline(upper_bound, color='green', label='Upper Bound')
    plt.hist(averaged_df['specz'], bins=50, alpha=0.5, edgecolor='k')
    plt.xlabel('Redshift')
    plt.ylabel('Number of Galaxies')
    plt.legend()
    plots['histogram_with_bounds'] = plot_to_base64()

    plt.title('Filtered Redshift Distribution')
    plt.hist(filtered_df['specz'], bins=30, alpha=0.5, edgecolor='k')
    plt.xlabel('Redshift')
    plt.ylabel('Number of Galaxies')
    plots['filtered_histogram'] = plot_to_base64()

    plt.title('Velocity Distribution (m/s)')
    plt.hist(averaged_df['velocity'], bins=30, alpha=0.5, edgecolor='k')
    plt.xlabel('Velocity')
    plt.ylabel('Number of Galaxies')
    plots['velocity_distribution'] = plot_to_base64()

    plt.title("Angular Separation Distribution")
    plt.hist(filtered_df['proj_sep'], bins=30, alpha=0.5, edgecolor='k')
    plt.xlabel('Projected Angular Separation')
    plt.ylabel('Number of Galaxies')
    plots['proj_sep_distribution'] = plot_to_base64()


    results = {
        "mean_specz": mean_specz,
        "std_specz": std_specz,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "velocity_dispersion_km_s": vel_disp,
        "theta_arcmin": theta_arcmin,
        "angular_diameter_distance_mpc": DA,
        "physical_diameter_mpc": diameter_Mpc,
        "dynamical_mass_solar": M_dyn_solar
    }

    return results, plots
