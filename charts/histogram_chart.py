import streamlit as st
import plotly.express as px

def histogram_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Color Theme, Color Scale, Grouping Column)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="histogram_theme"
            )
        with col2:
            x_axis = st.selectbox(
                "Select X-Axis", 
                updated_df.columns, 
                help="Choose the numeric column to create a histogram."
            )  # Single column selection for X-Axis
        with col3:
            group_by = st.selectbox(
                "Group By (Optional)", 
                ["None"] + list(updated_df.columns), 
                index=0,
                help="Optional: Select a column to group the histogram."
            )
        with col4:
            color_scale = st.selectbox(
                "Select Color Scale", 
                ["Viridis", "Cividis", "Plasma", "Inferno", "Blues", "RdBu", "YlGnBu", "YlOrRd"], 
                key="histogram_color_scale"
            )

        # Ensure the 'group_by' value is valid
        group_by = None if group_by == "None" else group_by

    # Check if the selected X-Axis column is numeric
    if x_axis is None or not updated_df[x_axis].dtype in ['int64', 'float64']:
        st.warning(f"The column '{x_axis}' is not numeric. Histograms require numeric data.")
        return None

    # Create the histogram using Plotly
    try:
        chart = px.histogram(
            updated_df,
            x=x_axis,
            color=group_by,  # Add grouping if selected
            title=f"Histogram of {x_axis}" + (f" grouped by {group_by}" if group_by else ""),
            template=theme,
            color_discrete_sequence=px.colors.sequential.__getattribute__(color_scale)
            if hasattr(px.colors.sequential, color_scale) else None
        )

        # Customize the layout for better aesthetics
        chart.update_layout(
            xaxis_title=x_axis,
            yaxis_title="Frequency",
            title_x=0.5,  # Center the title
            legend_title=group_by if group_by else None
        )

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)

        # Return the chart object for potential exporting
        return chart

    except Exception as e:
        st.error(f"An error occurred while creating the histogram: {e}")
        return None
