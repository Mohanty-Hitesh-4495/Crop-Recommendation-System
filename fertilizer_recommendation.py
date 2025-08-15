import streamlit as st
import pickle
import numpy as np

# Load the pre-trained model
with open('models/fertilizer_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

def fertilizer_recommendation_page():
    st.header("Fertilizer Recommendation System 🌱")
    st.write("Provide soil and crop details to get a fertilizer recommendation:")

    # User inputs for soil and environmental factors
    nitrogen = st.number_input("Nitrogen Content (ppm)", min_value=0, max_value=100, step=1, value=50)
    phosphorus = st.number_input("Phosphorus Content (ppm)", min_value=0, max_value=100, step=1, value=50)
    potassium = st.number_input("Potassium Content (ppm)", min_value=0, max_value=100, step=1, value=50)
    temperature = st.number_input("Temperature (°C)", min_value=-10, max_value=50, step=1, value=25)
    humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, step=1, value=50)
    soil_type = st.selectbox("Soil Type", ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey', 'Peaty', 'Silt', 'Chalky'])
    crop_type = st.selectbox("Crop Type", [
        'Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley', 
        'Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts', 'Grapes', 
        'PigeonPeas', 'Pomegranate', 'Banana', 'Mango', 'Lentil', 
        'KidneyBeans', 'Blackgram', 'ChickPea', 'Rice'
    ])
    moisture = st.number_input("Moisture Level (%)", min_value=0, max_value=100, step=1, value=50)

    # Expanded mappings
    soil_type_mapping = {
        "Sandy": 0, "Loamy": 1, "Black": 2, "Red": 3, "Clayey": 4,
        "Peaty": 5, "Silt": 6, "Chalky": 7
    }

    crop_type_mapping = {
        'Maize': 0, 'Sugarcane': 1, 'Cotton': 2, 'Tobacco': 3, 'Paddy': 4,
        'Barley': 5, 'Wheat': 6, 'Millets': 7, 'Oil seeds': 8, 'Pulses': 9,
        'Ground Nuts': 10, 'Grapes': 11, 'PigeonPeas': 12, 'Pomegranate': 13,
        'Banana': 14, 'Mango': 15, 'Lentil': 16, 'KidneyBeans': 17, 
        'Blackgram': 18, 'ChickPea': 19, 'Rice': 20
    }

    # Encode categorical inputs
    soil_type_encoded = soil_type_mapping[soil_type]
    crop_type_encoded = crop_type_mapping[crop_type]

    # Prediction button
    if st.button("Recommend Fertilizer"):
        # Prepare input array for the model
        features = np.array([[temperature, humidity, moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorus]])

        # Make prediction
        prediction = model.predict(features)

        # Display the result
        st.success(f"Recommended Fertilizer: 🌱 **{prediction[0]}** 🌱")
