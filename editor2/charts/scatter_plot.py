import streamlit as st
import plotly.express as px
import pandas as pd

def scatter_plot(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme, Color Scale)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="scatter_theme"
            )
        with col2:
            color_scale = st.selectbox(
                "Choose Color Scale", 
                ["Viridis", "Cividis", "Plasma", "Inferno", "Jet", "YlGnBu"], 
                key="scatter_color_scale"
            )
        with col3:
            x_axis = st.selectbox(
                "Select X-Axis", 
                updated_df.columns, 
                help="Choose a numeric or datetime column for the X-Axis."
            )
        with col4:
            y_axis = st.multiselect(
                "Select Y-Axis", 
                updated_df.columns, 
                help="Choose one or more numeric columns for the Y-Axis."
            )

    # Validate inputs
    if not x_axis or not y_axis:
        st.warning("Please select both X-Axis and at least one Y-Axis column.")
        return None

    # Ensure X-Axis is numeric or datetime
    try:
        if pd.api.types.is_datetime64_any_dtype(updated_df[x_axis]):
            updated_df[x_axis] = pd.to_datetime(updated_df[x_axis])  # Convert to datetime if not already
        elif pd.api.types.is_numeric_dtype(updated_df[x_axis]):
            pass  # Valid numeric column
        else:
            updated_df[x_axis] = pd.to_datetime(updated_df[x_axis], errors='coerce')  # Attempt conversion to datetime
            if updated_df[x_axis].isnull().any():
                raise ValueError(f"The column '{x_axis}' contains invalid dates or cannot be converted to datetime.")
    except Exception as e:
        st.warning(str(e))
        return None


    # Validate Y-Axis columns
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not pd.api.types.is_numeric_dtype(updated_df[col]):
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Scatter plot requires numeric data.")
            return None

    # Create scatter plots for each selected Y-Axis column
    fig = None
    for col in y_axis:
        scatter_fig = px.scatter(
            updated_df, 
            x=x_axis, 
            y=col, 
            title=f"Scatter Plot: {x_axis} vs {col}", 
            color=col,  # Optional color based on the current Y column
            color_continuous_scale=color_scale, 
            template=theme
        )

        if fig is None:
            fig = scatter_fig
        else:
            # Combine multiple scatter plots
            fig.add_traces(scatter_fig.data)

    # Update layout for combined plots
    if len(y_axis) > 1:
        fig.update_layout(title=f"Scatter Plot: {x_axis} vs Multiple Y-Axis Columns")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

    # Return the figure for potential export
    return fig
