import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


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




def bar_chart_3rd(updated_df, x_axis=None, y_axis=None, theme=None, color_scale=None):
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

    # Create a figure for the bar chart
    fig = go.Figure()

    # Add bars for each Y-axis column
    for i, col in enumerate(y_axis):
        fig.add_trace(
            go.Bar(x=updated_df[x_axis], y=updated_df[col], name=col, marker=dict(color=color_sequence[i]))
        )

    # Get the reference filter and date
    dates = None
    # Get the reference filter and date
    if 'date' in updated_df.columns:
        dates = updated_df['date'].unique()[0]
    if 'Référence Pièce(s)' in updated_df.columns:
        refrence_filter = updated_df['Référence Pièce(s)'].unique()[0]
    
        if len(updated_df['Référence Pièce(s)'].unique()) == 1:
            # Update the layout with titles and secondary y-axis labels
            fig.update_layout(
                title=f"{x_axis} vs {', '.join(y_axis)}  ({dates} - {refrence_filter}) ",
                template=theme,
                colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
            )
    else:
        # Update the layout with titles and secondary y-axis labels
        fig.update_layout(
            title=f"{x_axis} vs {', '.join(y_axis)}  ({dates}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
        )  
    
    # Update y-axis label
    fig.update_yaxes(title_text=", ".join(y_axis))

    # Enable all Plotly interactive features
    config = {
        "scrollZoom": True,  # Allow zooming by scrolling
        "displayModeBar": True,  # Show the mode bar
        "modeBarButtonsToAdd": [
            "drawline",  # Add line drawing
            "drawopenpath",  # Add open path drawing
            "drawclosedpath",  # Add closed path drawing
            "drawcircle",  # Add circle drawing
            "drawrect",  # Add rectangle drawing
            "eraseshape",  # Add shape eraser
            "hoverClosestCartesian",  # Hover to show closest data points
            "hoverCompareCartesian",  # Compare data on hover
            "select2d",  # 2D selection
            "lasso2d",  # Lasso selection
            "zoomIn2d",  # Zoom in
            "zoomOut2d",  # Zoom out
            "autoScale2d",  # Auto-scale
            "resetScale2d",  # Reset scale
            "toImage",  # Download as image
            "toggleSpikelines",  # Toggle spike lines
            "resetViews",  # Reset views
            "hoverClosest3d",  # Hover closest in 3D
            "hoverClosestGeo",  # Hover closest in geo charts
            "hoverClosestGl2d",  # Hover closest in WebGL 2D
            "hoverClosestPie",  # Hover closest in pie charts
        ],
        "displaylogo": False,  # Hide the Plotly logo
        "responsive": True,  # Make the chart responsive
    }

    # Display the chart with all interactive features
    st.plotly_chart(fig, use_container_width=True, config=config)
    return fig  # Return the figure for export or further use







