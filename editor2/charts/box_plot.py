import streamlit as st
import plotly.express as px
import plotly.express as px
import plotly.graph_objects as go

def box_plot(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="box_plot_theme"
            )
        with col2:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col3:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
        return None

    # Validate the selected X-Axis
    if x_axis is None or not updated_df[x_axis].dtype.name in ['object', 'category', 'int64', 'float64']:
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for a Box Plot.")
        return None

    # Validate the selected Y-Axis columns
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype.name in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Box Plot requires numeric data.")

    # Create the box plot using Plotly
    try:
        chart = px.box(
            updated_df, 
            x=x_axis, 
            y=y_axis, 
            title=f"Box Plot: {x_axis} vs {', '.join(y_axis)}", 
            template=theme,
            color_discrete_sequence=px.colors.sequential.Viridis if color_scale == "Viridis" else None
        )
        chart.update_layout(xaxis_title=x_axis, yaxis_title="Values")
    except Exception as e:
        st.error(f"An error occurred while creating the box plot: {e}")
        return None

    # Display the chart
    st.plotly_chart(chart, use_container_width=True)

    # Return the chart for potential export
    return chart




import plotly.graph_objects as go
import streamlit as st
import plotly.express as px

def box_plot_3rd(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
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

    # Create a figure for the box plot
    fig = go.Figure()

    # Define x-axis positions for each box
    x_positions = list(range(len(y_axis)))  # Assign distinct x positions

    # Add box plots for each Y-axis column at separate x-axis positions
    for i, col in enumerate(y_axis):
        fig.add_trace(
            go.Box(
                y=updated_df[col],
                name=col,
                marker=dict(color=color_sequence[i]),
                boxmean='sd',
                x=[x_positions[i]] * len(updated_df[col]),  # Ensuring box plots are spaced apart
            )
        )

    # Add horizontal min/max lines & annotations for each box plot separately
    for i, col in enumerate(y_axis):
        max_val = updated_df[col].max()
        min_val = updated_df[col].min()

        # Add max value line (Horizontal line above the box)
        fig.add_shape(
            type="line",
            x0=x_positions[i] - 0.4,
            x1=x_positions[i] + 0.4,
            y0=max_val,
            y1=max_val,
            line=dict(color="red", width=2, dash="dash"),
        )

        # Add min value line (Horizontal line below the box)
        fig.add_shape(
            type="line",
            x0=x_positions[i] - 0.4,
            x1=x_positions[i] + 0.4,
            y0=min_val,
            y1=min_val,
            line=dict(color="blue", width=2, dash="dash"),
        )

        # Add max value annotation
        fig.add_annotation(
            x=x_positions[i] + 0.5,  # Shift right for better placement
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
            x=x_positions[i] + 0.5,  # Shift right for better placement
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
            title=f"Box Plot for {', '.join(y_axis)}  ({dates}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            xaxis=dict(
                tickmode='array',
                tickvals=x_positions,
                ticktext=y_axis,
                title="",
            ),
        )
    else:
        # Update the layout with titles
        fig.update_layout(
            title=f"Box Plot for {', '.join(y_axis)}  ({dates} - {reference_filter}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            xaxis=dict(
                tickmode='array',
                tickvals=x_positions,
                ticktext=y_axis,
                title="",
            ),
        )

    # Update y-axis label
    fig.update_yaxes(title_text="Values", showgrid=True)

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    return fig  # Return the figure for export or further use

