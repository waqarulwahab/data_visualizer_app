import streamlit as st
import plotly.express as px

def bubble_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Size, Color Theme, Color Scale)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="bubble_chart_theme"
            )
        with col2:
            color_scale = st.selectbox(
                "Select Color Scale", 
                ["Viridis", "Cividis", "Plasma", "Inferno", "Blues", "RdBu", "YlGnBu", "YlOrRd"], 
                key="bubble_chart_color_scale"
            )
        with col3:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col4:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

    # Validate user inputs
    if not x_axis:
        st.warning("Please select a column for X-Axis.")
        return None
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
        return None
    if len(y_axis) < 2:
        st.warning("Please select at least two columns for Y-Axis: one for Y values and one for bubble size.")
        return None

    # Dynamic warnings for column types and missing values
    if not updated_df[x_axis].dtype.name in ['object', 'category', 'int64', 'float64']:
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for a Bubble Chart.")
        return None

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype.name in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Bubble Chart requires numeric data.")
            return None

    # Assign Y values and size column
    y_value_column = y_axis[0]
    size_column = y_axis[1] if len(y_axis) > 1 else y_axis[0]  # Use the first column if only one Y-Axis is provided

    # Create the bubble chart using Plotly
    try:
        chart = px.scatter(
            updated_df,
            x=x_axis,
            y=y_value_column,
            size=size_column,
            title=f"Bubble Chart: {x_axis} vs {y_value_column} (Bubble Size: {size_column})",
            template=theme,
            color=updated_df[y_value_column],  # Use first Y-Axis column for color
            color_continuous_scale=color_scale,
            size_max=50  # Set maximum bubble size for better readability
        )
        chart.update_layout(
            xaxis_title=x_axis,
            yaxis_title=y_value_column,
            coloraxis_colorbar=dict(title=y_value_column),
        )
    except Exception as e:
        st.error(f"An error occurred while creating the bubble chart: {e}")
        return None

    # Display the chart
    st.plotly_chart(chart, use_container_width=True)

    # Return the chart for further use or export
    return chart
