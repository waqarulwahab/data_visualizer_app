import streamlit as st
import plotly.express as px

def pie_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="pie_theme"
            )
        with col2:
            x_axis = st.selectbox(
                "Select X-Axis (Category)", 
                updated_df.columns, 
                help="Select the categorical column for the pie chart."
            )  # Single column selection for X-Axis
        with col3:
            y_axis = st.selectbox(
                "Select Y-Axis (Values)", 
                updated_df.columns, 
                help="Select the numeric column for the pie chart values."
            )  # Single column selection for Y-Axis (values)
    
    # Validate inputs
    if not x_axis or not y_axis:
        st.warning("Please select both X-Axis (category) and Y-Axis (values) columns.")
        return None

    # Ensure x_axis and y_axis are strings
    if not isinstance(x_axis, str) or not isinstance(y_axis, str):
        st.warning("Invalid column selection. Please select valid X-Axis and Y-Axis columns.")
        return None

    # Dynamic warnings for column issues
    if updated_df[x_axis].isnull().any():
        st.warning(f"The column '{x_axis}' contains missing values. Consider cleaning the data.")
    if updated_df[y_axis].isnull().any():
        st.warning(f"The column '{y_axis}' contains missing values. Consider cleaning the data.")
    
    # Validate data types
    if updated_df[x_axis].dtype not in ['object', 'category']:
        st.warning(f"The column '{x_axis}' in X-Axis is not categorical. Pie charts require categorical data.")
        return None
    if updated_df[y_axis].dtype not in ['int64', 'float64']:
        st.warning(f"The column '{y_axis}' in Y-Axis is not numeric. Pie charts require numeric data.")
        return None

    # Create the pie chart using Plotly
    try:
        chart = px.pie(
            updated_df,
            names=x_axis,
            values=y_axis,
            title=f"Pie Chart: {x_axis} vs {y_axis}",
            template=theme
        )

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)

        # Return the chart object for exporting if needed
        return chart

    except Exception as e:
        st.error(f"An error occurred while creating the pie chart: {e}")
        return None
