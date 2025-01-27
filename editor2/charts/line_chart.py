import plotly.express as px
import streamlit as st

def line_chart(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)
        with col3:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)

    # Validate input
    if not x_axis or not y_axis:
        st.warning("Please select valid X and Y axes to generate a chart.")
        return None  # Return None if input is invalid

    # Check for issues in the Y-axis columns
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"Column '{col}' contains missing values.")
        if updated_df[col].dtype not in ['int64', 'float64']:
            st.error(f"Column '{col}' is not numeric. Cannot plot this column.")
            return None

    # Generate line chart
    fig = px.line(
        updated_df,
        x=x_axis,
        y=y_axis,
        title=f"Line Chart: {x_axis} vs {', '.join(y_axis)}",
        template=theme,
        color_discrete_sequence=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    return fig  # Return the figure for export or further use
