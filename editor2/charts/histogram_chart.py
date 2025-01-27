import streamlit as st
import plotly.express as px

def histogram_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Color Theme, Color Scale)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col3:
            pass
        with col4:
            pass
    # Check if the X-Axis is numeric
    if not updated_df[x_axis].dtype in ['int64', 'float64']:
        st.warning(f"The column '{x_axis}' is not numeric. Histograms require numeric data.")

    # Create the histogram using Plotly
    chart = px.histogram(updated_df, 
                         x=x_axis, 
                         title=f"Histogram of {x_axis}", 
                         template=theme)


    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
