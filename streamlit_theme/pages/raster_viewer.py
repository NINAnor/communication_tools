import os
import leafmap.foliumap as leafmap
import leafmap.colormaps as cm
import streamlit as st

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
st.title("Visualize Raster Datasets")
st.markdown(
    """
An interactive web app for visualizing local raster datasets and Cloud Optimized GeoTIFF ([COG](https://www.cogeo.org)).
The app was built using [streamlit](https://streamlit.io), [leafmap](https://leafmap.org), and [Titiler](https://developmentseed.org/titiler/).
"""
)

row1_col1, row1_col2 = st.columns([2, 1])

# Drag-and-Drop File Upload
uploaded_file = st.file_uploader("Drag and drop a GeoTIFF file here:", type=["tif", "tiff"])

if uploaded_file:
    # Save the uploaded file to a temporary directory
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Verify and process the GeoTIFF
    try:
        dataset = gdal.Open(file_path)
        st.success(f"Successfully loaded GeoTIFF: {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error loading GeoTIFF: {e}")

    # Visualization Parameters
    add_params = st.checkbox("Add visualization parameters")
    if add_params:
        vis_params = st.text_area("Enter visualization parameters as a dictionary", "{}")
    else:
        vis_params = {}

    if len(vis_params) > 0:
        try:
            vis_params = eval(vis_params)
        except Exception as e:
            st.error(f"Invalid visualization parameters: {e}")
            vis_params = {}

    # Display the raster on the map
    m = leafmap.Map(latlon_control=False)
    try:
        m.add_raster(file_path, **vis_params)
    except Exception as e:
        st.error(f"Error displaying raster: {e}")

    with row1_col1:
        m.to_streamlit(height=700)
else:
    st.info("Upload a GeoTIFF file to visualize.")