import streamlit as st
from PIL import Image

def main():
    # --- Page Configuration ---
    st.set_page_config(page_title="NINA Dashboard", 
                       page_icon="\U0001F4C8", 
                       layout="wide")
    
    # --- footer ---
    # Footer with fixed position
    st.markdown("""
    <style>
        /* Add padding to body content to avoid overlay */
        .block-container {
            padding-bottom: 80px; /* Adjust this value to match footer height */
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
            <p>© 2024 My Streamlit App | All rights reserved.</p>
        </div>
    """

    # Render the footer
    st.markdown(footer_html, unsafe_allow_html=True)

    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Home", "About Us", "Analytics", "Contact"])
    st.sidebar.info(
    """
    Dr. A. Nordman: <https://www.nina.no>
    #test prosjekt
    """
)

    # --- Page Content Based on Navigation ---
    if page == "Home":
        home_page()
    elif page == "About Us":
        about_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Contact":
        contact_page()

# --- Home Page ---
def home_page():
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

    # KPIs Section
    st.markdown("---")
    st.subheader("Key Performance Indicators (KPIs)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", "$1.5M", "+10%")
    col2.metric("New Clients", "250", "+25")
    col3.metric("Customer Satisfaction", "95%", "\u2b06 5%")

# --- About Page ---
def about_page():
    st.title("About Us")
    st.write("""
    NINA er en uavhengig stiftelse som forsker på natur og samspillet natur – samfunn.
    
    """)

# --- Analytics Page ---
def analytics_page():
    st.title("Company Analytics Dashboard")
    st.write("""
    ## Key Analytics
    Explore our interactive charts and metrics to analyze company performance.
    """)
    
    # Placeholder for Interactive Charts
    chart_type = st.selectbox("Select a Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])
    if chart_type == "Bar Chart":
        st.bar_chart({"Sales": [10, 20, 30, 40], "Profit": [5, 15, 25, 35]})
    elif chart_type == "Line Chart":
        st.line_chart({"2021": [50, 60, 70], "2022": [80, 90, 100]})
    elif chart_type == "Pie Chart":
        st.write("Pie Chart placeholder - Replace with actual data visualization")

# --- Contact Page ---
def contact_page():
    st.title("Contact Us")
    st.write("""
    ## Get In Touch
    Norsk institutt for naturforskning
    

    
    - **Email:** firmapost@nina.no
    - **Phone:** +47 73 80 14 00
    - **Address:** Postboks 5685 Torgarden, 7485 Trondheim, Norway

    """)
    

if __name__ == "__main__":
    main()
