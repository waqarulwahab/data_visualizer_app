import streamlit as st
import plotly.express as px

def area_chart(updated_df):
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
    if not updated_df[x_axis].dtype in ['object', 'category', 'int64', 'float64']:
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for an Area Chart.")
    
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Area Chart requires numeric data.")
    
    # Create the area chart using Plotly
    chart = px.area(updated_df, 
                    x=x_axis, 
                    y=y_axis, 
                    title=f"Area Chart: {x_axis} vs {', '.join(y_axis)}", 
                    template=theme)
    
    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
