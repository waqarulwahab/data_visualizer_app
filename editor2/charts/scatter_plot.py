import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


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



def scatter_plot_3rd(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
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

    # Define a color scale if not provided
    if not color_scale:
        color_scale = 'Viridis'  # Default color scale

    # Generate a unique color sequence based on the number of columns
    color_sequence = px.colors.sequential.__getattribute__(color_scale)[:len(y_axis)]

    # Create a figure for the scatter plot
    fig = go.Figure()

    # Add scatter points for each Y-axis column
    for i, col in enumerate(y_axis):
        fig.add_trace(
            go.Scatter(
                x=updated_df[x_axis],
                y=updated_df[col],
                mode='markers',
                name=col,
                marker=dict(color=color_sequence[i], size=8, opacity=0.7)
            )
        )

    # Add horizontal min/max lines & annotations for each column
    for i, col in enumerate(y_axis):
        max_val = updated_df[col].max()
        min_val = updated_df[col].min()

        # Add max value line (Horizontal line)
        fig.add_shape(
            type="line",
            x0=updated_df[x_axis].min(),
            x1=updated_df[x_axis].max(),
            y0=max_val,
            y1=max_val,
            line=dict(color="red", width=2, dash="dash"),
        )

        # Add min value line (Horizontal line)
        fig.add_shape(
            type="line",
            x0=updated_df[x_axis].min(),
            x1=updated_df[x_axis].max(),
            y0=min_val,
            y1=min_val,
            line=dict(color="blue", width=2, dash="dash"),
        )

        # Add max value annotation
        fig.add_annotation(
            x=updated_df[x_axis].max(),
            y=max_val,
            text=f"Max {col}: {max_val}",
            showarrow=True,
            arrowhead=2,
            ax=20,
            ay=-30,
            font=dict(size=10, color="red"),
            arrowcolor="red",
            align="left",
        )

        # Add min value annotation
        fig.add_annotation(
            x=updated_df[x_axis].max(),
            y=min_val,
            text=f"Min {col}: {min_val}",
            showarrow=True,
            arrowhead=2,
            ax=20,
            ay=30,
            font=dict(size=10, color="blue"),
            arrowcolor="blue",
            align="left",
        )

    # Get the reference filter and date
    dates = updated_df['Date'].unique()[0]
    reference_filter = updated_df['Référence Pièce(s)'].unique()[0]

    if len(updated_df['Référence Pièce(s)'].unique()) > 1:
        # Update the layout with titles
        fig.update_layout(
            title=f"Scatter Plot for {', '.join(y_axis)} vs {x_axis}  ({dates}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            xaxis_title=x_axis,
            yaxis_title="Values",
        )
    else:
        # Update the layout with titles
        fig.update_layout(
            title=f"Scatter Plot for {', '.join(y_axis)} vs {x_axis}  ({dates} - {reference_filter}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            xaxis_title=x_axis,
            yaxis_title="Values",
        )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    return fig  # Return the figure for export or further use
