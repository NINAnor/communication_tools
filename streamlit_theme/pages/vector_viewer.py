import os
import geopandas as gpd
import leafmap.foliumap as leafmap
import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Web Map Service (WMS)", 
                page_icon="NINA_logo.png", 
                layout="wide")

# --- footer ---
st.markdown("""
<style>
    /* Add padding to body content to avoid overlay */
    .block-container {
        padding-bottom: 80px; 
    }

    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f0f0; /* Solid background */
        color: #333333; /* Solid dark text */
        text-align: center;
        padding: 10px;
        border-top: 1px solid #cccccc;
        font-size: 14px;
        font-weight: bold;
        z-index: 1000; /* Ensure footer stays on top */
    }

    .footer a {
        color: #007BFF;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Footer
footer_html = """
    <div class="footer">
        <p>Licensed under <a href='https://www.gnu.org/licenses/gpl-3.0.txt' target='_blank'>GNU General Public License v3.0</a></p>
        <p>© 2024 NINA template | All rights reserved.</p>
    </div>
"""

# Render the footer
st.markdown(footer_html, unsafe_allow_html=True)

# --- Sidebar ---
st.logo(
"NINA_logo.png", 
size="large",  
link="https://www.nina.no",  
icon_image="NINA_logo.png",    
)
with st.sidebar:

    st.markdown("### Contact")
    st.markdown(
        """
        - **Email**: firmapost@nina.no  
        - **Phone**: +47 00 00 00 00 
        - **Website**: [NINA](https://www.nina.no)
        """
    )
# --- MAIN ---
st.title("Display vector data")
st.markdown("""
An interactive web app for visualizing vector datasets such as Shapefiles (`.shp`) and GeoPackages (`.gpkg`).  
The app was built using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org).
""")

row1_col1, row1_col2 = st.columns([2, 1])

# Drag-and-Drop File Upload
uploaded_file = st.file_uploader("Drag and drop a Shapefile (.zip) or GeoPackage (.gpkg):", type=["zip", "gpkg"])

if uploaded_file:
    # Handle Shapefile Upload (as .zip)
    if uploaded_file.name.endswith(".zip"):
        temp_dir = "temp_shp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        zip_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Unzip the file
        import zipfile
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the .shp file
        shp_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith(".shp")]
        if len(shp_files) == 0:
            st.error("No .shp file found in the uploaded .zip.")
        else:
            shp_path = shp_files[0]
            gdf = gpd.read_file(shp_path)
            st.success(f"Loaded Shapefile: {shp_path}")
    
    # Handle GeoPackage Upload
    elif uploaded_file.name.endswith(".gpkg"):
        temp_dir = "temp_gpkg_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        gpkg_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(gpkg_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read the GeoPackage
        gdf = gpd.read_file(gpkg_path)
        st.success(f"Loaded GeoPackage: {uploaded_file.name}")

    # Convert Timestamp columns to strings
    if "gdf" in locals() and not gdf.empty:
        for col in gdf.columns:
            if pd.api.types.is_datetime64_any_dtype(gdf[col]):
                gdf[col] = gdf[col].astype(str)  # Convert Timestamps to strings


    # Display the geometries on the map
    m = leafmap.Map(center=(gdf.geometry.iloc[0].centroid.y, gdf.geometry.iloc[0].centroid.x), zoom=8)
    m.add_gdf(gdf, layer_name="Vector Data")

    with row1_col1:
        m.to_streamlit(height=700)

    with row1_col2:
        st.write("### File Information")
        st.write(f"**Coordinate Reference System (CRS):** {gdf.crs}")
        st.write(f"**Number of Features:** {len(gdf)}")
        st.write("**Attributes:**")
        st.write(gdf.head())

else:
    st.info("Upload a Shapefile (.zip) or GeoPackage (.gpkg) to visualize.")
