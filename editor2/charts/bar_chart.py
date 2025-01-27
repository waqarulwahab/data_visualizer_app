import streamlit as st
import plotly.express as px

def bar_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Bar Color)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="bar_chart_theme"
            )
        with col2:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col3:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
        return None

    # Dynamic warnings if columns have issues
    if x_axis is None or not updated_df[x_axis].dtype.name in ['object', 'category', 'string']:
        st.warning(f"The column '{x_axis}' in X-Axis is not categorical or suitable for a Bar Chart.")

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype.name in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric.")

    # Create the bar chart using Plotly (with multiple columns in Y-Axis)
    try:
        chart = px.bar(
            updated_df, 
            x=x_axis, 
            y=y_axis, 
            title=f"Bar Chart: {x_axis} vs {', '.join(y_axis)}", 
            template=theme, 
            color_discrete_sequence=px.colors.sequential.Viridis if color_scale == "Viridis" else None
        )
        chart.update_layout(xaxis_title=x_axis, yaxis_title="Values")
    except Exception as e:
        st.error(f"An error occurred while creating the bar chart: {e}")
        return None

    # Display the chart
    st.plotly_chart(chart, use_container_width=True)

    # Return the chart for potential export
    return chart