import streamlit as st
import pickle
import pandas as pd
import numpy as np  # Import numpy for numerical operations
from PIL import Image  
import matplotlib.pyplot as plt

# Load the saved model
with open('models/crop_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the dataset
data = pd.read_csv('dataset/Crop_recommendation.csv') 

# Load crop summaries from a text file
crop_summaries = {}
with open('docs/crop_summaries.txt', 'r') as f:
    for line in f:
        crop, summary = line.split(': ', 1)
        crop_summaries[crop] = summary.strip()

# Initialize session state variable for page navigation if not already initialized
if 'page' not in st.session_state:
    st.session_state.page = "Crop Recommendation"  # Default page

# Main heading for the application
st.markdown("<h1 style='font-size: 36px;'>🌾 FarmSathi: फसल का Perfect Match 🌾</h1>", unsafe_allow_html=True)
st.write("<h2 style='font-size: 26px;'> Your trusted guide for choosing the right crop based on soil, climate, and more!</h2>", unsafe_allow_html=True)

# Load the image
logo_image = Image.open('assets/farmsathi logo.png')  # Ensure this path is correct

# Sidebar for page navigation and logo
with st.sidebar:
    # Display the image using st.image
    st.image(logo_image, width=150)
    st.title("FarmSathi")
    # Navigation buttons
    if st.button("Crop Statistics"):
        st.session_state.page = "Crop Statistics"
    if st.button("Crop Recommendation"):
        st.session_state.page = "Crop Recommendation"

# Crop Recommendation Page
if st.session_state.page == "Crop Recommendation":
    st.header("Crop Recommendation System")
    st.write("Provide soil and climate details to get a crop recommendation:")

    # User inputs for soil nutrients, climate, etc.
    nitrogen = st.number_input("Nitrogen level in soil")
    phosphorus = st.number_input("Phosphorus level in soil")
    potassium = st.number_input("Potassium level in soil")
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    ph = st.number_input("pH of soil")
    rainfall = st.number_input("Rainfall (mm)")

    # Prediction button
    if st.button("Recommend Crop"):
        # Make prediction with user input values
        input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
        prediction = model.predict(input_data)
        st.write(f"Recommended Crop: 🌱 {prediction[0]} 🌱")

# Crop Statistics Page
elif st.session_state.page == "Crop Statistics":
    st.header("Crop Statistics")
    st.write("Explore Crop-Specific Nutrient and Climate Requirements")

    # Crop selection
    selected_crop = st.selectbox("Select a Crop", options=list(data['Crop'].unique()))

    # Display crop-specific statistics
    if selected_crop:
        x = data[data['Crop'] == selected_crop]

        st.write(f"### Nutrient and Climate Statistics for {selected_crop}")

        # Collecting data for plotting
        min_values = [
            x['Nitrogen'].min(),
            x['Phosphorus'].min(),
            x['Potassium'].min(),
            x['Temperature'].min(),
            x['Humidity'].min(),
            x['pH_Value'].min(),
            x['Rainfall'].min()
        ]
        
        avg_values = [
            x['Nitrogen'].mean(),
            x['Phosphorus'].mean(),
            x['Potassium'].mean(),
            x['Temperature'].mean(),
            x['Humidity'].mean(),
            x['pH_Value'].mean(),
            x['Rainfall'].mean()
        ]
        
        max_values = [
            x['Nitrogen'].max(),
            x['Phosphorus'].max(),
            x['Potassium'].max(),
            x['Temperature'].max(),
            x['Humidity'].max(),
            x['pH_Value'].max(),
            x['Rainfall'].max()
        ]
        
        categories = ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']

        # Display textual statistics
        st.subheader("Statistical Overview")
        stats_df = pd.DataFrame({
            'Parameter': categories,
            'Minimum': min_values,
            'Average': avg_values,
            'Maximum': max_values
        })
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns([2, 1])  # Adjust column ratios as needed
        
        with col1:
            st.write(stats_df)

        with col2:
            # Crop summary based on the selected crop from the loaded dictionary
            crop_summary = crop_summaries.get(selected_crop, "No summary available for this crop.")
            st.subheader(f"Summary for {selected_crop}")
            st.write(crop_summary)

        # Plotting in a single subplot
        x = np.arange(len(categories))  # the label locations
        width = 0.25  # the width of the bars

        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar(x - width, min_values, width, label='Minimum', color='green')
        bars2 = ax.bar(x, avg_values, width, label='Average', color='orange')
        bars3 = ax.bar(x + width, max_values, width, label='Maximum', color='red')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Values')
        ax.set_title(f'{selected_crop} Nutrient and Climate Requirements')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()

        st.pyplot(fig)
