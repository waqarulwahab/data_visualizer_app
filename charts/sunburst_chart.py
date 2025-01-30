import streamlit as st
import plotly.express as px

def sunburst_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="sunburst_theme"
            )
        with col2:
            x_axis = st.selectbox(
                "Select X-Axis (Parent)", 
                updated_df.columns, 
                help="Choose a column to represent the parent level."
            )
        with col3:
            y_axis = st.multiselect(
                "Select Y-Axis (Child Levels)", 
                updated_df.columns, 
                help="Select one or more columns to represent child levels in the hierarchy."
            )

    # Validate inputs
    if not x_axis or not y_axis:
        st.warning("Please select both X-Axis (Parent) and at least one Y-Axis (Child Levels).")
        return None

    # Dynamic warnings for column issues
    if updated_df[x_axis].isnull().any():
        st.warning(f"The column '{x_axis}' has missing values.")
    if updated_df[x_axis].dtype not in ['object', 'category']:
        st.warning(f"The column '{x_axis}' in X-Axis (Parent) is not categorical.")

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if updated_df[col].dtype not in ['object', 'category']:
            st.warning(f"The column '{col}' in Y-Axis (Child Levels) is not categorical.")

    # Create the sunburst chart using Plotly
    if x_axis and y_axis:
        try:
            chart = px.sunburst(
                updated_df, 
                path=[x_axis] + y_axis,  # Combine X-Axis (Parent) and Y-Axis (Child Levels)
                title="Sunburst Chart", 
                template=theme
            )

            # Display the chart
            st.plotly_chart(chart, use_container_width=True)
            
            # Return the chart for potential export
            return chart
        
        except Exception as e:
            st.error(f"An error occurred while creating the Sunburst Chart: {e}")
            return None
