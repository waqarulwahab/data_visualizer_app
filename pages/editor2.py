import streamlit as st
import pandas as pd

from helper_functions.tab1 import viewer_editor_tab
from helper_functions.tab2 import interactive_charts_tab
from helper_functions.tab3 import export_graphs

from helper_functions.filters import refrence_pieces_filter
from helper_functions.filters import filter_by_time
from helper_functions.filters import filter_by_date

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

    df.columns = [str(col).strip() for col in df.columns]

    df = filter_by_date(df)
    df = filter_by_time(df)
    df = refrence_pieces_filter(df)

    # Check if the DataFrame is empty after filtering
    if df.empty:
        st.error("No data available after filtering.")
    else:
        # Main Layout
        tab1, tab2, tab3 = st.tabs(["📋 Data Editor", "📈 Visualization", "💾 Export Data"])

        # Tab 1: Data Editor
        with tab1:
            updated_df = viewer_editor_tab(df)

        # Tab 2: Visualization
        with tab2:
            try:
                generated_figures = interactive_charts_tab(updated_df)
            except KeyError as e:
                st.error(f"Error: Column {e} not found in the dataset.")
                generated_figures = []

        # Tab 3: Export Data
        with tab3:
            try:
                export_graphs(generated_figures)
            except KeyError as e:
                st.error(f"Error: Column {e} not found in the dataset.")
                            
else:
    st.info("Please upload a file to get started.")





