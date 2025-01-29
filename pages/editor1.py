import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from helper_functions.utils import load_file, display_logo, page_navigations


# Custom CSS for styling and hiding the Mito banner
st.markdown(
    """
    <style>
        .mito-pro-banner {
            display: none !important;
        }    
        .main {
            background-color: #f5f5f5;
        }
        h1, h2, h3, h4 {
            color: #4CAF50;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

import sys

# Import win32com only if running on Windows
if sys.platform == "win32":
    import win32com.client

display_logo()

page_navigations()



uploaded_file = load_file()

if uploaded_file:
    file_extension = uploaded_file.suffix.lower()  # Get the extension in lowercase

    # Check if it's a CSV file and read it
    if file_extension == ".csv":
        df = pd.read_csv(uploaded_file)
        sheets = {"Sheet1": df}
    else:
        sheets = pd.read_excel(uploaded_file, sheet_name=None)

    # Sidebar for Sheet Selection
    with st.sidebar:
        sheet_names = list(sheets.keys())
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)
        df = sheets[selected_sheet]

    new_dfs, code = spreadsheet(df)
else:
    st.info("Please upload a file to get started.")