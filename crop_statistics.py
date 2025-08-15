import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('dataset/Crop_recommendation_Dataset.csv')

# Load crop summaries from a text file
crop_summaries = {}
with open('docs/crop_summaries.txt', 'r') as f:
    for line in f:
        crop, summary = line.split(': ', 1)
        crop_summaries[crop] = summary.strip()

def crop_statistics_page():
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
