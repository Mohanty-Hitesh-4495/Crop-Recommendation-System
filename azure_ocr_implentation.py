import streamlit as st
import os
from pathlib import Path
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv(Path(".env"))
endpoint = "https://syedsadiquh-doc-intelligence.cognitiveservices.azure.com/"
key = os.getenv("azure_api")

# Initialize Azure Document Analysis Client
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def format_bounding_box(bounding_box):
    """Format bounding box data"""
    if not bounding_box:
        return "N/A"
    return ", ".join([f"[{p.x}, {p.y}]" for p in bounding_box])

def analyze_read(file):
    """Analyze document for text using Azure Form Recognizer"""
    document = file.read()

    poller = document_analysis_client.begin_analyze_document("prebuilt-read", document=document)
    result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += f"Line: {line.content}\n"
    return extracted_text

def main():
    st.title("OCR using Azure Form Recognizer")

    # File uploader widget in Streamlit
    uploaded_file = st.file_uploader("Upload an image or document", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.write("Processing the document...")

        # Get the extracted text from the uploaded file
        extracted_text = analyze_read(uploaded_file)

        st.write("Extracted Text:")
        st.text_area("Extracted Data", extracted_text, height=300)

        # # You can process the extracted text to pass it to your recommendation models
        # if extracted_text:
        #     # Example: Parse extracted data (this should be customized based on your data)
        #     recommended_crop, recommended_fertilizer = get_crop_and_fertilizer(extracted_text)
        #     st.write(f"Recommended Crop: {recommended_crop}")
        #     st.write(f"Recommended Fertilizer: {recommended_fertilizer}")

if __name__ == "__main__":
    main()
