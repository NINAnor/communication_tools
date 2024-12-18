import ee
import streamlit as st
import geemap.foliumap as geemap

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



def search_data():

    # st.header("Search Earth Engine Data Catalog")

    Map = geemap.Map()

    if "ee_assets" not in st.session_state:
        st.session_state["ee_assets"] = None
    if "asset_titles" not in st.session_state:
        st.session_state["asset_titles"] = None

    col1, col2 = st.columns([2, 1])

    dataset = None
    with col2:
        keyword = st.text_input(
            "Enter a keyword to search (e.g., elevation)", "")
        if keyword:
            ee_assets = geemap.search_ee_data(keyword)
            asset_titles = [x["title"] for x in ee_assets]
            asset_types = [x["type"] for x in ee_assets]

            translate = {
                "image_collection": "ee.ImageCollection('",
                "image": "ee.Image('",
                "table": "ee.FeatureCollection('",
                "table_collection": "ee.FeatureCollection('",
            }

            dataset = st.selectbox("Select a dataset", asset_titles)
            if len(ee_assets) > 0:
                st.session_state["ee_assets"] = ee_assets
                st.session_state["asset_titles"] = asset_titles

            if dataset is not None:
                with st.expander("Show dataset details", True):
                    index = asset_titles.index(dataset)

                    html = geemap.ee_data_html(
                        st.session_state["ee_assets"][index])
                    html = html.replace("\n", "")
                    st.markdown(html, True)

                ee_id = ee_assets[index]["id"]
                uid = ee_assets[index]["uid"]
                st.markdown(f"""**Earth Engine Snippet:** `{ee_id}`""")
                ee_asset = f"{translate[asset_types[index]]}{ee_id}')"
                vis_params = st.text_input(
                    "Enter visualization parameters as a dictionary", {}
                )
                layer_name = st.text_input("Enter a layer name", uid)
                button = st.button("Add dataset to map")
                if button:
                    vis = {}
                    try:
                        if vis_params.strip() == "":
                            vis_params = "{}"
                        vis = eval(vis_params)
                        if not isinstance(vis, dict):
                            st.error(
                                "Visualization parameters must be a dictionary")
                        try:
                            Map.addLayer(eval(ee_asset), vis, layer_name)
                        except Exception as e:
                            st.error(f"Error adding layer: {e}")
                    except Exception as e:
                        st.error(f"Invalid visualization parameters: {e}")

            with col1:
                Map.to_streamlit()
        else:
            with col1:
                Map.to_streamlit()


def app():
    st.title("Earth Engine Data Catalog")
    st.markdown("""
    Visualize earth engine data sets. For template purpses, this code has been copied [from](https://github.com/opengeos/streamlit-geospatial/blob/master/pages/10_%F0%9F%8C%8D_Earth_Engine_Datasets.py)
    """)

    search_data()


app()
