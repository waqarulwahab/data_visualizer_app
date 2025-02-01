import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from helper_functions.utils import load_file, display_logo, page_navigations, process_file


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



uploaded_files = load_file()

if uploaded_files:
    all_sheets = {}  # Dictionary to store sheets from all files

    for uploaded_file in uploaded_files:
        sheets = process_file(uploaded_file)
        
        for sheet_name, df in sheets.items():
            if sheet_name in all_sheets:
                # If the sheet already exists, concatenate the data
                all_sheets[sheet_name] = pd.concat([all_sheets[sheet_name], df], ignore_index=True)
            else:
                # If the sheet does not exist, add it to the dictionary
                all_sheets[sheet_name] = df


    # Sidebar for Sheet Selection (optional)
    with st.sidebar:
        sheet_names = list(all_sheets.keys())
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)
        df = all_sheets[selected_sheet]

    new_dfs, code = spreadsheet(df)
else:
    st.info("Please upload a file to get started.")