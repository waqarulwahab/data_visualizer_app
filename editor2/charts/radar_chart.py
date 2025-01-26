import streamlit as st
import plotly.express as px

def radar_chart(updated_df):
    # Layout for user input (X-Axis, Y-Axis, Color Theme)
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
    with col2:
        x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
    with col3:
        y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
    
    # Dynamic warnings if columns have issues
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric.")
    
    # Create the radar chart using Plotly (with multiple columns in Y-Axis)
    chart = px.scatter_polar(updated_df, r=y_axis[0], theta=x_axis, title="Radar Chart", template=theme)
    
    # Add additional traces for each column in Y-Axis
    for i in range(1, len(y_axis)):
        chart.add_scatterpolar(r=updated_df[y_axis[i]], theta=updated_df[x_axis], mode='lines', name=y_axis[i])
    
    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
