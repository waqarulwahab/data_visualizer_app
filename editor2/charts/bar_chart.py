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





def bar_chart_3rd(updated_df, multi_chart=False, x_axis=None, y_axis=None, theme=None, color_scale=None):
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
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            barmode="group"
        )        
    else:
        # Update the layout with titles and secondary y-axis labels
        fig.update_layout(
            title=f"{x_axis} vs {', '.join(y_axis)}  ({dates} - {refrence_filter}) ",
            template=theme,
            colorway=px.colors.sequential.__getattribute__(color_scale) if color_scale else None,
            barmode="group"
        )
    
    # Update y-axis label
    fig.update_yaxes(title_text=", ".join(y_axis))

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    return fig  # Return the figure for export or further use












