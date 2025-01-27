import streamlit as st
import plotly.express as px

def heatmap_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (Theme, Color Scale, Columns for Correlation)
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="heatmap_theme"
            )
        with col2:
            color_scale = st.selectbox(
                "Select Color Scale", 
                ["Viridis", "Cividis", "Plasma", "Inferno", "Blues", "RdBu", "YlGnBu", "YlOrRd"], 
                key="heatmap_color_scale"
            )
        with col3:
            y_axis = st.multiselect(
                "Select Y-Axis Columns for Correlation", 
                updated_df.columns, 
                default=updated_df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            )  # Default to numeric columns for correlation

    # Validate Y-Axis selection
    if not y_axis or len(y_axis) < 2:
        st.warning("Please select at least two numeric columns for correlation.")
        return None

    # Ensure all selected columns are numeric
    try:
        numeric_columns = updated_df[y_axis].select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) == 0:
            st.warning("Selected Y-Axis columns must be numeric for correlation.")
            return None
    except Exception as e:
        st.error(f"Error validating Y-Axis columns: {e}")
        return None

    # Compute the correlation matrix
    try:
        corr_matrix = updated_df[numeric_columns].corr()

        # Create the heatmap using Plotly
        chart = px.imshow(
            corr_matrix,
            labels=dict(color="Correlation"),
            x=numeric_columns,
            y=numeric_columns,
            color_continuous_scale=color_scale,
            title="Heatmap of Correlations (Y-Axis Columns)",
            template=theme
        )

        # Update layout for better readability
        chart.update_layout(
            title_x=0.5,  # Center the title
            xaxis_title="Features (Y-Axis)",
            yaxis_title="Features (Y-Axis)",
            coloraxis_colorbar=dict(title="Correlation Coefficient"),
        )

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)

        # Return the chart for export
        return chart
    except Exception as e:
        st.error(f"An error occurred while creating the heatmap: {e}")
        return None
