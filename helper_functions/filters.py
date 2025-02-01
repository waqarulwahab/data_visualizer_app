import streamlit as st
import pandas as pd

def filter_by_date(df):
    # Check for potential date columns
    date_columns = [
        col for col in df.columns 
        if pd.to_datetime(df[col], errors='coerce').notnull().any()  # Check for at least one valid date
    ]

    if date_columns:
        # Automatically use the first valid date column
        date_column = date_columns[0]
        
        # Convert to datetime and drop invalid entries (NaT will be created for invalid values)
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        
        # Drop rows with invalid date entries (NaT)
        df = df.dropna(subset=[date_column])
        
        # Convert to datetime.date (removes time)
        df[date_column] = df[date_column].dt.date

        # Date Range Filter
        if not df.empty:  # Check if the DataFrame is not empty
            min_date = df[date_column].min()
            max_date = df[date_column].max()

            # Add date range pickers
            col1, col2 = st.sidebar.columns([1, 1])
            with col1:
                start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
            with col2:
                end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

            # Ensure comparison is between datetime.date objects
            if start_date and end_date:
                # Filter the DataFrame based on the selected date range
                df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
    return df
    
def refrence_pieces_filter(df):
    df = pd.DataFrame(df)
    # Check if the column exists
    if 'référence pièce(s)' in df.columns:
        unique_references = df['référence pièce(s)'].dropna().unique()  # Drop NaN values
        selected_references = st.sidebar.multiselect(
            "Filter by Référence Pièces",
            options=unique_references,
            help="Select one or more reference numbers to filter"
        )
        
        if selected_references:
            df = df[df['référence pièce(s)'].isin(selected_references)]
    return df



def filter_by_time(df):
    if 'time' in df.columns:
        try:
            # Convert the 'time' column to datetime format to extract hour
            df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S').dt.time

            # Extract the hour from the 'time' column
            df['hour'] = pd.to_datetime(df['time'].astype(str), format='%H:%M:%S').dt.hour

            # Get the dynamic default start and end hours from the data
            min_hour = int(df['hour'].min())  # Ensure min_hour is an integer
            max_hour = int(df['hour'].max())  # Ensure max_hour is an integer

            # Sidebar inputs with dynamic default values
            st.sidebar.header("Filter by Time Range")
            col1, col2 = st.sidebar.columns([1, 1])
            with col1:
                start_hour = st.number_input("Start Hour", min_value=0, max_value=23, step=1, value=min_hour, help="Enter the starting hour (0-23)")
            with col2:
                end_hour = st.number_input("End Hour", min_value=0, max_value=23, step=1, value=max_hour, help="Enter the ending hour (0-23)")

            # Validate the time range
            if start_hour > end_hour:
                st.sidebar.error("Error: Start hour must be less than or equal to end hour.")
                return df  # Return the unfiltered DataFrame if the range is invalid

            # Filter data based on start_hour and end_hour
            df = df[(df['hour'] >= start_hour) & (df['hour'] <= end_hour)]

        except Exception as e:
            st.error(f"An error occurred while processing the time column: {e}")
            return df  # Return the unfiltered DataFrame in case of an error

    return df
