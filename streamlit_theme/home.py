import streamlit as st
import os
from PIL import Image
from streamlit_navigation_bar import st_navbar
import pages as pg

# --- Page Configuration ---
st.set_page_config(page_title="NINA Dashboard", 
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



st.title("Welcome to a NINA dashboard")

col1, col2 = st.columns(2)

# Add logo
image = Image.open("NINA_logo.png")  # Add other logos here
col1.image(image, caption="Norwegian Institute for Nature Research", width=300)

col2.write("""
## About this dashboard
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer condimentum ornare vehicula. 
Vestibulum eget sapien tortor. Vivamus tortor libero, consectetur et pellentesque at, sollicitudin nec ex. 
Nam mattis bibendum risus, nec facilisis purus tristique quis. Pellentesque habitant morbi 
tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas rutrum, ipsum nec tincidunt sagittis, 
tellus nisi consequat nisl, eu dictum nulla felis et nulla. In dignissim nibh ut ante ornare, ut molestie
felis varius. Mauris sollicitudin lectus id ligula venenatis, ac pretium libero egestas. Sed a magna nec nisl venenatis cursus. 
Vestibulum id pulvinar nisi, non vehicula ligula.

""")
