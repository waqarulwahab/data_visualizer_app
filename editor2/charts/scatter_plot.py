import streamlit as st
import plotly.express as px

def scatter_plot(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Scale)
        col1, col2, col3 , col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            color_scale = st.selectbox("Choose Color Scale", ["Viridis", "Cividis", "Plasma", "Inferno", "Jet", "YlGnBu"], key="color_scale")    
        with col3:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col4:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis


    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
    

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Scatter plot requires numeric data.")
    

    # Create the scatter plot using Plotly
    chart = px.scatter(
        updated_df, 
        x=x_axis, 
        y=y_axis, 
        title=f"Scatter Plot: {x_axis} vs {', '.join(y_axis)}", 
        color=y_axis[0] if y_axis else None,  # Optional color based on the first Y column
        color_continuous_scale=color_scale,  # Apply the selected color scale
        template=theme
    )
    
    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
