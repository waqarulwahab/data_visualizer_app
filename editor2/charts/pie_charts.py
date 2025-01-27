import streamlit as st
import plotly.express as px

def pie_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            x_axis = st.selectbox("Select X-Axis (Category)", updated_df.columns)  # Single column selection for X-Axis
        with col3:
            y_axis = st.multiselect("Select Y-Axis (Values)", updated_df.columns)  # Single column selection for Y-Axis (values)
    
    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
    
    # Dynamic warnings if columns have issues
    if x_axis and y_axis:
        if updated_df[x_axis].isnull().any():
            st.warning(f"The column '{x_axis}' has missing values.")
        if updated_df[y_axis[0]].isnull().any():
            st.warning(f"The column '{y_axis[0]}' has missing values.")
        
        if not updated_df[x_axis].dtype in ['object', 'category']:
            st.warning(f"The column '{x_axis}' in X-Axis is not categorical.")
        if not updated_df[y_axis[0]].dtype in ['int64', 'float64']:
            st.warning(f"The column '{y_axis[0]}' in Y-Axis is not numeric.")
    
    # Create the Pie chart using Plotly
    if x_axis and y_axis:
        chart = px.pie(updated_df, names=x_axis, values=y_axis[0], title="Pie Chart", template=theme)

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)
