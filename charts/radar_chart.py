import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def radar_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None,  color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="radar_theme"
            )
        with col2:
            x_axis = st.selectbox(
                "Select X-Axis (Categories)", 
                updated_df.columns, 
                help="Select a categorical column for the radar chart."
            )  # Single column selection for X-Axis
        with col3:
            y_axis = st.multiselect(
                "Select Y-Axis (Values)", 
                updated_df.columns, 
                help="Select one or more numeric columns for the radar chart."
            )  # Multiple column selection for Y-Axis

    # Validate inputs
    if not x_axis or not y_axis:
        st.warning("Please select both X-Axis (categories) and at least one Y-Axis (values) column.")
        return None

    # Dynamic warnings for column issues
    if updated_df[x_axis].isnull().any():
        st.warning(f"The column '{x_axis}' has missing values.")
    if updated_df[x_axis].dtype not in ['object', 'category']:
        st.warning(f"The column '{x_axis}' in X-Axis is not categorical. Radar charts require categorical data.")
        return None

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if updated_df[col].dtype not in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Radar charts require numeric data.")
            return None

    # Create the radar chart using Plotly
    try:
        fig = go.Figure()

        for col in y_axis:
            fig.add_trace(
                go.Scatterpolar(
                    r=updated_df[col], 
                    theta=updated_df[x_axis], 
                    mode='lines+markers', 
                    name=col
                )
            )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True),
            ),
            title="Radar Chart",
            template=theme,
            showlegend=True
        )

        # Display the chart
        st.plotly_chart(fig, use_container_width=True)

        # Return the chart object for exporting if needed
        return fig

    except Exception as e:
        st.error(f"An error occurred while creating the radar chart: {e}")
        return None
