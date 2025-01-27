import streamlit as st
import plotly.express as px

def line_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Line Color)
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
    

    # Create the line chart using Plotly (with multiple columns in Y-Axis)
    chart = px.line(updated_df, x=x_axis, y=y_axis, title=f"Line Chart: {x_axis} vs {', '.join(y_axis)}", template=theme)
    
    # Automatically assign different colors to each line
    chart.update_traces(marker=dict(color='rgb(0,0,0)'))  # Reset all traces to default colors (this is optional)
    
    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
