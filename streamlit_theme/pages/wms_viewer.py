import ast
import streamlit as st
import leafmap.foliumap as leafmap



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

@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


def app():

    st.title("WMS viewer")    
    st.markdown(
        """
    This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service 
    in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find 
    some WMS URLs if needed.

    Some further text here
    """
    )

    row1_col1, row1_col2 = st.columns([3, 1.3])
    width = 800
    height = 600
    layers = None

    with row1_col2:

        esa_landcover = "https://services.terrascope.be/wms/v2"
        url = st.text_input(
            "Enter a WMS URL:", value="https://services.terrascope.be/wms/v2"
        )
        empty = st.empty()

        if url:
            options = get_layers(url)

            default = None
            if url == esa_landcover:
                default = "WORLDCOVER_2020_MAP"
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            add_legend = st.checkbox("Add a legend to the map", value=True)
            if default == "WORLDCOVER_2020_MAP":
                legend = str(leafmap.builtin_legends["ESA_WorldCover"])
            else:
                legend = ""
            if add_legend:
                legend_text = st.text_area(
                    "Enter a legend as a dictionary {label: color}",
                    value=legend,
                    height=200,
                )

        with row1_col1:
            m = leafmap.Map(center=(36.3, 0), zoom=2)

            if layers is not None:
                for layer in layers:
                    m.add_wms_layer(
                        url, layers=layer, name=layer, attribution=" ", transparent=True,  format="image/png"
                    )
            if add_legend and legend_text:
                legend_dict = ast.literal_eval(legend_text)
                m.add_legend(legend_dict=legend_dict)

            m.to_streamlit(height=height)

    st.markdown(
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer condimentum ornare vehicula. 
        Vestibulum eget sapien tortor. Vivamus tortor libero, consectetur et pellentesque at, sollicitudin nec ex. 
        Nam mattis bibendum risus, nec facilisis purus tristique quis. Pellentesque habitant morbi 
        tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas rutrum, ipsum nec tincidunt sagittis, 
        tellus nisi consequat nisl, eu dictum nulla felis et nulla. In dignissim nibh ut ante ornare, ut molestie
        felis varius. Mauris sollicitudin lectus id ligula venenatis, ac pretium libero egestas. Sed a magna nec nisl venenatis cursus. 
        Vestibulum id pulvinar nisi, non vehicula ligula.
    """
    )


app()
