import streamlit as st
import pickle

# Load the saved model
with open('crop_recommendation_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit app
st.title("Crop Recommendation System")

# Example user inputs for soil nutrients, climate, etc.
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
    st.write(f"Recommended Crop: {prediction[0]}")
