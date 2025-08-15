import pandas as pd
import random

# Define crops and fertilizers
crops = ["Rice", "Maize", "ChickPea", "KidneyBeans", "PigeonPeas", "Blackgram",
         "Lentil", "Pomegranate", "Banana", "Mango", "Grapes"]

fertilizers = {
    "Urea": {"N": (60, 90), "P": (30, 50), "K": (20, 50)},
    "DAP": {"N": (70, 100), "P": (40, 70), "K": (20, 45)},
    "MOP": {"N": (0, 20), "P": (0, 30), "K": (70, 100)},
    "NPK": {"N": (40, 80), "P": (40, 80), "K": (40, 80)},
    "SSP": {"N": (20, 40), "P": (50, 80), "K": (10, 30)},
    "Ammonium Sulphate": {"N": (10, 30), "P": (10, 30), "K": (10, 30)}
}

soil_types = ["Sandy", "Loamy", "Clayey", "Silt", "Peaty", "Chalky"]

# Generate data points
data_points = []
for _ in range(150):
    crop = random.choice(crops)
    fertilizer = random.choice(list(fertilizers.keys()))
    nutrient_ranges = fertilizers[fertilizer]

    N = random.randint(*nutrient_ranges["N"])
    P = random.randint(*nutrient_ranges["P"])
    K = random.randint(*nutrient_ranges["K"])

    temperature = round(random.uniform(15, 35), 2)
    humidity = round(random.uniform(20, 90), 2)
    moisture = round(random.uniform(5, 60), 2)
    soil_type = random.choice(soil_types)

    data_points.append({
        "Nitrogen (N)": N,
        "Phosphorus (P)": P,
        "Potassium (K)": K,
        "Temperature (°C)": temperature,
        "Humidity (%)": humidity,
        "Moisture (%)": moisture,
        "Soil Type": soil_type,
        "Crop": crop,
        "Fertilizer": fertilizer
    })

# Create DataFrame and save as CSV
fertilizer_data = pd.DataFrame(data_points)
fertilizer_data.to_csv("Fertilizer_Dataset.csv", index=False)