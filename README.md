``` mermaid
graph TD
    Farmer["Farmer (User)"] -->|Soil & Environmental Data| CropRec["Crop Recommendation"]
    Farmer -->|Soil & Crop Data| FertRec["Fertilizer Recommendation"]
    Farmer -->|Request for Analysis| StatAnalysis["Statistical Analysis"]
    
    CropRec -->|Prediction| Output1["Recommended Crop"]
    FertRec -->|Prediction| Output2["Recommended Fertilizer"]
    StatAnalysis -->|Insights| Graphs["Statistical Graphs"]
    
    CropRec -->|Access Data| Database[("Soil & Crop Data")]
    FertRec -->|Access Data| Database
    StatAnalysis -->|Access Data| Database
```

``` mermaid
classDiagram
    Farmer --> CropRecommendation : "Requests"
    Farmer --> FertilizerRecommendation : "Requests"
    Farmer --> StatisticalAnalysis : "Requests"
    
    class Farmer {
        +String name
        +String location
        +submitData()
        +viewRecommendations()
    }

    class CropRecommendation {
        -SoilData soilData
        -EnvironmentalData envData
        +String recommendCrop()
        +fetchCropData()
    }

    class FertilizerRecommendation {
        -SoilData soilData
        -CropData cropData
        +String recommendFertilizer()
        +fetchFertilizerData()
    }

    class StatisticalAnalysis {
        -AnalysisData analysisData
        +generateInsights()
        +createGraphs()
    }

    class SoilData {
        +float nitrogen
        +float phosphorus
        +float potassium
        +String soilType
    }

    class EnvironmentalData {
        +float temperature
        +float humidity
        +float moisture
    }

    class CropData {
        +String cropName
        +String cropType
    }

    class Database {
        +fetchSoilData()
        +fetchCropData()
        +fetchFertilizerData()
    }

    CropRecommendation --> SoilData : "Uses"
    CropRecommendation --> EnvironmentalData : "Uses"
    FertilizerRecommendation --> SoilData : "Uses"
    Fertilize
```
