import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import os
import pandas as pd
import sys

st.set_page_config(layout="wide")

# Hide MitoSheet Pro Banner
st.markdown("""
    <style>
        .mito-pro-banner {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar logo
st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)

# File upload section
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file", 
    type=["csv", "xls", "xlsx"], 
    help="Drag and drop or click to upload a CSV or Excel file."
)

st.sidebar.page_link("main.py", label="Editor-1", icon="1️⃣")
st.sidebar.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")
st.sidebar.page_link("pages/editor3.py", label="Editor-3", icon="3️⃣")

# Define the import folder
IMPORT_FOLDER = './data'
if not os.path.exists(IMPORT_FOLDER):
    os.makedirs(IMPORT_FOLDER)

# Function to remove old files before saving a new one
def clear_import_folder(folder):
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete old files
        except Exception as e:
            st.error(f"Error deleting {file_name}: {e}")

# Check if a file is uploaded
if uploaded_file is not None:
    # Clear old files before saving a new one
    clear_import_folder(IMPORT_FOLDER)

    file_path = os.path.join(IMPORT_FOLDER, uploaded_file.name)
    
    # Save the new file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' has been uploaded and previous files have been removed.")

# Load MitoSheet (it will automatically detect only the latest file)
new_dfs, code = spreadsheet(import_folder=IMPORT_FOLDER)
