import streamlit as st
import pickle

# Load the saved model
with open('models/crop_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

def crop_recommendation_page():
    st.header("Crop Recommendation System")
    st.write("Provide soil and climate details to get a crop recommendation:")

    # User inputs for soil nutrients, climate, etc.
    nitrogen = st.number_input("Nitrogen level in soil",min_value=0, max_value=100, step=1, value=50)
    phosphorus = st.number_input("Phosphorus level in soil",min_value=0, max_value=100, step=1, value=50)
    potassium = st.number_input("Potassium level in soil",min_value=0, max_value=100, step=1, value=50)
    temperature = st.number_input("Temperature (°C)",min_value=0, max_value=100, step=1, value=50)
    humidity = st.number_input("Humidity (%)",min_value=0, max_value=100, step=1, value=50)
    ph = st.number_input("pH of soil",min_value=0, max_value=100, step=1, value=50)
    rainfall = st.number_input("Rainfall (mm)",min_value=0, max_value=100, step=1, value=50)

    # Prediction button
    if st.button("Recommend Crop"):
        # Make prediction with user input values
        input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]
        prediction = model.predict(input_data)
        st.success(f"Recommended Crop: 🌱 {prediction[0]} 🌱")
