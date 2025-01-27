import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import os
import pandas as pd



st.set_page_config(layout="wide")

# Add custom CSS to hide Pro banner
st.markdown("""
    <style>
        .mito-pro-banner {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Use custom CSS to set the sidebar width and make it non-resizable
st.markdown(
    """
    <style>
    .css-1d391kg {
        width: 300px !important;  /* Set fixed width */
        resize: none !important;  /* Disable resizing */
    }
    </style>
    """, 
    unsafe_allow_html=True
)




import sys

# Import win32com only if running on Windows
if sys.platform == "win32":
    import win32com.client


# Sidebar logo
st.sidebar.image("LOGO.jpg", width=300 ,use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

# File upload section in the sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file", 
    type=["csv", "xlsx"], 
    help="Drag and drop or click to upload a CSV or Excel file."
)

st.sidebar.page_link("main.py", label="Editor-1", icon="1️⃣")
st.sidebar.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")

# Define the import folder
IMPORT_FOLDER = './data'

# Ensure the folder exists
if not os.path.exists(IMPORT_FOLDER):
    os.makedirs(IMPORT_FOLDER)

# Check if a file is uploaded
if uploaded_file is not None:
    # Save the uploaded file to the data folder
    file_path = os.path.join(IMPORT_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File '{uploaded_file.name}' saved to {IMPORT_FOLDER}")

    # Automatically analyze the uploaded file with MitoSheet
    new_dfs, code = spreadsheet(import_folder=IMPORT_FOLDER)  # The uploaded file will be available in MitoSheet
else:
    # Use the spreadsheet function with the import_folder parameter
    new_dfs, code = spreadsheet(import_folder=IMPORT_FOLDER)

