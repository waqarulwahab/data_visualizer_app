import streamlit as st
import plotly.express as px
import pandas as pd

def violin_plot(updated_df):
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
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for a Violin Plot.")
    
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Violin Plot requires numeric data.")
    
    # Melt the dataframe so that we can treat each Y-Axis column as a separate category
    melted_df = updated_df.melt(id_vars=[x_axis], value_vars=y_axis, var_name='Y-Axis Column', value_name='Values')
    
    # Create the violin plot using Plotly
    chart = px.violin(melted_df, 
                      x=x_axis, 
                      y='Values', 
                      color='Y-Axis Column',  # Color by the Y-Axis column
                      title=f"Violin Plot: {x_axis} vs {', '.join(y_axis)}", 
                      template=theme,
                      color_discrete_sequence=px.colors.qualitative.Set1,  # Custom color palette
                      box=True,  # Display box plot inside the violin plot
                      points="all")  # Show all points as dots on the violin plot
    
    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
