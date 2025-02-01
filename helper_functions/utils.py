import os
import streamlit as st
from pathlib import Path
import pandas as pd

def display_logo():
    # Sidebar logo
    st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

def load_file():
    # Define the data folder path
    data_folder = Path("data")

    # Get a list of all files in the folder
    files = [file for file in data_folder.iterdir() if file.is_file()]

    # Select the first file if files exist
    # uploaded_file = files[0] if files else None  # This is a Path object

    return files

def process_file(file_path):
    file_extension = file_path.suffix.lower()  # Get the file extension in lowercase

    # Check if it's a CSV file and read it
    if file_extension == ".csv":
        df = pd.read_csv(file_path)
        sheets = {"Sheet1": df}
    else:
        # Read all sheets from an Excel file
        sheets = pd.read_excel(file_path, sheet_name=None)

    return sheets

def page_navigations():
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,3,3])
    with col1:
        st.page_link("main.py", label="Home", icon="🏠")
    with col2:
        st.page_link("pages/editor1.py", label="Editor-1", icon="1️⃣")
    with col3:
        st.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")
    with col4:
        st.page_link("pages/editor3.py", label="Editor-3", icon="3️⃣")


def normalize_column_names(df):
    """Convert all column names to lowercase."""
    df.columns = df.columns.str.lower()
    return df


# Function to remove old files before saving a new one
def clear_import_folder(folder):
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete old files
        except Exception as e:
            st.error(f"Error deleting {file_name}: {e}")
