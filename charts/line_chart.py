import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots



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



import streamlit.components.v1 as components
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px



def line_chart_3rd(updated_df, x_axis=None, y_axis=None, theme=None, color_scale=None):
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

    # Create subplots with secondary y-axes
    fig = make_subplots(
        rows=1, cols=1, 
        specs=[[{"secondary_y": True}]], 
        shared_xaxes=True
    )
    
    # Add data for the first y-axis (primary) with unique color
    fig.add_trace(
        go.Scatter(x=updated_df[x_axis], y=updated_df[y_axis[0]], mode='lines', name=y_axis[0], line=dict(color=color_sequence[0])),
        secondary_y=False
    )

    # Add data for the remaining y-axes (secondary) with unique colors
    for i, col in enumerate(y_axis[1:], 1):
        fig.add_trace(
            go.Scatter(x=updated_df[x_axis], y=updated_df[col], mode='lines', name=col, line=dict(color=color_sequence[i])),
            secondary_y=True
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

    
    # Update y-axes properties (for better visualization)
    fig.update_yaxes(title_text=y_axis[0], secondary_y=False)
    
    # Dynamically update secondary Y-axes with column names
    for i, col in enumerate(y_axis[1:], 1):
        fig.update_yaxes(title_text=col, secondary_y=True)

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