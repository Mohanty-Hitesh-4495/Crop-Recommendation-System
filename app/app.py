# from azure_ocr_implentation import main
import streamlit as st
from PIL import Image
from crop_recommendation import crop_recommendation_page
from crop_statistics import crop_statistics_page
from fertilizer_recommendation import fertilizer_recommendation_page
from streamlit_option_menu import option_menu

# Main heading for the application
st.markdown("<h1 style='font-size: 36px;'>🌾 FarmSathi: फसल का Perfect Match 🌾</h1>", unsafe_allow_html=True)
st.write("<h2 style='font-size: 26px;'>Your trusted guide for choosing the right crop based on soil, climate, and more!</h2>", unsafe_allow_html=True)

# Sidebar configuration
logo_image = Image.open("assets/farmsathi_logo.png")

# Create centered logo using columns
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image(logo_image, width=200)

# Comprehensive CSS to center the logo - multiple selectors for better compatibility
st.sidebar.markdown("""
    <style>
        /* Target all possible image containers in sidebar */
        div[data-testid="stSidebar"] .stImage {
            text-align: center;
        }
        
        div[data-testid="stSidebar"] .stImage > div {
            display: flex;
            justify-content: center;
        }
        
        div[data-testid="stSidebar"] img {
            display: block;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Force center alignment for sidebar content */
        .css-1d391kg, .css-ng1t4o, .css-1outpf7 {
            text-align: center;
        }
        
        /* Additional fallback selectors */
        [data-testid="stSidebar"] [data-testid="stImage"] {
            text-align: center;
        }
        
        [data-testid="stSidebar"] [data-testid="stImage"] > div {
            justify-content: center;
            display: flex;
        }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h2>Main Menu</h2>", unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "",
        ["Crop Recommendation", "Crop Statistics", "Fertilizer Recommendation", "Upload Report","About"],
        icons=["list", "bar-chart", "list-task", "upload","info-circle"],
        menu_icon="cast",
        default_index=0,
    )

# Navigation logic
if selected == "Crop Recommendation":
    crop_recommendation_page()
elif selected == "Crop Statistics":
    crop_statistics_page()
elif selected == "Fertilizer Recommendation":
    fertilizer_recommendation_page()
# elif selected == "Upload Report":
#     main()
elif selected == "About":
    st.markdown(
        """
        ### About FarmSathi 🌾
        **FarmSathi** is a state-of-the-art digital platform designed to empower farmers by leveraging the power of technology. Our mission is to provide intelligent solutions to optimize farming practices, boost productivity, and promote sustainable agriculture.

        #### Why Choose FarmSathi?
        - **Precision Farming**: Make informed decisions with data-driven recommendations tailored to your soil and crop needs.
        - **User-Friendly Interface**: A simple and intuitive interface ensures ease of use for farmers of all technical backgrounds.
        - **Advanced AI & ML Models**: Backed by cutting-edge artificial intelligence, our models offer reliable recommendations.
        - **Comprehensive Features**:
          - Crop recommendation based on soil nutrients, weather conditions, and other factors.
          - Fertilizer recommendation to ensure healthy crops and sustainable farming.
          - In-depth crop statistics to monitor performance and identify trends.

        #### Key Features:
        1. **Crop Recommendation System**:
           - Suggests the most suitable crop for your soil type and environmental conditions.
           - Helps improve yield and minimize resource wastage.
        
        2. **Fertilizer Recommendation System**:
           - Recommends fertilizers based on your soil's nutrient profile and crop type.
           - Ensures balanced nutrient supply for optimal growth.

        3. **Crop Statistics Dashboard**:
           - Analyze historical trends and monitor crop performance.
           - Helps in strategic decision-making and resource allocation.

        4. **Accessibility**:
           - Supports multilingual features to cater to farmers across regions.
           - Available on web and mobile platforms for easy access.

        #### Our Vision:
        At **FarmSathi**, we aim to revolutionize farming by integrating technology with traditional practices. Our vision is to create a future where every farmer has access to the tools and knowledge required for sustainable and profitable agriculture.

        #### Join Us!
        Be a part of the FarmSathi family and take the first step toward smarter farming. Together, we can build a sustainable future and support the backbone of our economy – **our farmers**. 🌱

        #### 🌟 Empowering Farmers, Growing Together 🌟
        """
    )