import streamlit as st
import plotly.express as px

def sunburst_chart(updated_df):
    # Layout for user input (X-Axis, Y-Axis, Color Theme)
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
    with col2:
        x_axis = st.selectbox("Select X-Axis (Parent)", updated_df.columns)  # Single column selection for X-Axis
    with col3:
        y_axis = st.multiselect("Select Y-Axis (Child)", updated_df.columns)  # Multiple column selection for Y-Axis
    
    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
    
    # Dynamic warnings if columns have issues
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if updated_df[col].dtype not in ['object', 'category']:
            st.warning(f"The column '{col}' in Y-Axis is not categorical.")
    
    # Create the sunburst chart using Plotly
    if x_axis and y_axis:
        chart = px.sunburst(updated_df, path=[x_axis] + [y_axis[0]], title="Sunburst Chart", template=theme)

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)
