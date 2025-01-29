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



import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import plotly.express as px


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def line_chart_3rd(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
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

    # Define a color scale if not provided
    if not color_scale:
        color_scale = 'Viridis'  # Default color scale

    # Generate a unique color sequence based on the number of columns
    color_sequence = px.colors.sequential.__getattribute__(color_scale)[:len(y_axis)]

    if multi_chart:
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

        # Find max and min values for Y-axis columns and add horizontal lines with annotations
        max_annotations = []
        min_annotations = []

        for col in y_axis:
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
                name=f"Max {col}"
            )
            # Add min value line (Horizontal line)
            fig.add_shape(
                type="line",
                x0=updated_df[x_axis].min(),
                x1=updated_df[x_axis].max(),
                y0=min_val,
                y1=min_val,
                line=dict(color="blue", width=2, dash="dash"),
                name=f"Min {col}"
            )

            # Collect annotations for max and min
            max_annotations.append((max_val, f"Max {col}: {max_val}", "left"))
            min_annotations.append((min_val, f"Min {col}: {min_val}", "right"))

        # Sort annotations by y-values to prevent overlap
        max_annotations = sorted(max_annotations, key=lambda x: x[0], reverse=True)
        min_annotations = sorted(min_annotations, key=lambda x: x[0])

        # Add max annotations
        for i, (y_val, text, position) in enumerate(max_annotations):
            fig.add_annotation(
                x=updated_df[x_axis].min(),
                y=y_val,
                text=text,
                showarrow=True,
                arrowhead=2,
                ax=10,
                ay=-40 - i * 30,  # Adjust distance to avoid overlap
                font=dict(size=10, color="red"),
                arrowcolor="red",
                align="center",
                xanchor="right" if position == "left" else "left"
            )

        # Add min annotations
        for i, (y_val, text, position) in enumerate(min_annotations):
            fig.add_annotation(
                x=updated_df[x_axis].max(),
                y=y_val,
                text=text,
                showarrow=True,
                arrowhead=2,
                ax=10,
                ay=40 + i * 30,  # Adjust distance to avoid overlap
                font=dict(size=10, color="blue"),
                arrowcolor="blue",
                align="center",
                xanchor="right" if position == "left" else "left"
            )

        # Get the reference filter and date
        dates = updated_df['Date'].unique()[0]
        refrence_filter = updated_df['Référence Pièce(s)'].unique()[0]

        if len(updated_df['Référence Pièce(s)'].unique()) > 1:
            # Update the layout with titles and secondary y-axis labels
            fig.update_layout(
                title=f"{x_axis} vs {', '.join(y_axis)}  ({dates}) ",
                template=theme,
                colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
            )        
        else:
            # Update the layout with titles and secondary y-axis labels
            fig.update_layout(
                title=f"{x_axis} vs {', '.join(y_axis)}  ({dates} - {refrence_filter}) ",
                template=theme,
                colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
            )
        
        # Update y-axes properties (for better visualization)
        fig.update_yaxes(title_text=y_axis[0], secondary_y=False)
        
        # Dynamically update secondary Y-axes with column names
        for i, col in enumerate(y_axis[1:], 1):
            fig.update_yaxes(title_text=col, secondary_y=True)

    else:
        # Single axis line chart with unique colors
        fig = px.line(
            updated_df,
            x=x_axis,
            y=y_axis,
            title=f"Line Chart: {x_axis} vs {', '.join(y_axis)}",
            template=theme,
            color_discrete_sequence=color_sequence  # Use the dynamically created color sequence
        )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    return fig  # Return the figure for export or further use



















# def line_chart_3rd(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
#     if not multi_chart:
#         col1, col2, col3 = st.columns([1, 1, 2])
        
#         with col1:
#             theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
#         with col2:
#             x_axis = st.selectbox("Select X-Axis", updated_df.columns)
#         with col3:
#             y_axis = st.multiselect("Select Y-Axis", updated_df.columns)

#     # Validate input
#     if not x_axis or not y_axis:
#         st.warning("Please select valid X and Y axes to generate a chart.")
#         return None  # Return None if input is invalid

#     # Check for issues in the Y-axis columns
#     for col in y_axis:
#         if updated_df[col].isnull().any():
#             st.warning(f"Column '{col}' contains missing values.")
#         if updated_df[col].dtype not in ['int64', 'float64']:
#             st.error(f"Column '{col}' is not numeric. Cannot plot this column.")
#             return None

#     if multi_chart:
#         # Create subplots with secondary y-axes
#         fig = make_subplots(
#             rows=1, cols=1, 
#             specs=[[{"secondary_y": True}]], 
#             shared_xaxes=True
#         )
        
#         # Add data for the first y-axis (primary)
#         fig.add_trace(
#             go.Scatter(x=updated_df[x_axis], y=updated_df[y_axis[0]], mode='lines', name=y_axis[0]),
#             secondary_y=False
#         )

#         # Add data for the remaining y-axes (secondary)
#         for i, col in enumerate(y_axis[1:], 1):
#             fig.add_trace(
#                 go.Scatter(x=updated_df[x_axis], y=updated_df[col], mode='lines', name=col),
#                 secondary_y=True
#             )

#         # Update the layout with titles and secondary y-axis labels
#         fig.update_layout(
#             title=f"Multi-Axis Line Chart: {x_axis} vs {', '.join(y_axis)}",
#             template=theme,
#             colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
#         )
        
#         # Update y-axes properties (for better visualization)
#         fig.update_yaxes(title_text=y_axis[0], secondary_y=False)
#         fig.update_yaxes(title_text="Secondary Y-Axis", secondary_y=True)

#     else:
#         # Single axis line chart as before
#         fig = px.line(
#             updated_df,
#             x=x_axis,
#             y=y_axis,
#             title=f"Line Chart: {x_axis} vs {', '.join(y_axis)}",
#             template=theme,
#             color_discrete_sequence=px.colors.sequential.__getattribute__(color_scale) if color_scale else None
#         )

#     # Display the chart
#     st.plotly_chart(fig, use_container_width=True)
#     return fig  # Return the figure for export or further use

