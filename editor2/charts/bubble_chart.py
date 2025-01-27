import streamlit as st
import plotly.express as px

def bubble_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Size, Color Theme, Color Scale)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            color_scale = st.selectbox("Select Color Scale", ["Viridis", "Cividis", "Plasma", "Inferno", "Blues", "RdBu", "YlGnBu", "YlOrRd"])   
        with col3:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col4:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis


    # Check if at least one column is selected for Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for Y-Axis.")
    
    # Dynamic warnings if columns have issues
    if not updated_df[x_axis].dtype in ['object', 'category', 'int64', 'float64']:
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for a Bubble Chart.")
    
    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' has missing values.")
        if not updated_df[col].dtype in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis is not numeric. Bubble Chart requires numeric data.")
    
    # Determine the size column for the bubbles (if multiple Y-Axis, use the second one for size)
    if len(y_axis) > 1:
        size_column = y_axis[1]
    else:
        size_column = y_axis[0]  # If only one Y-Axis, use the same for size

    # Create the bubble chart using Plotly
    chart = px.scatter(updated_df, 
                       x=x_axis, 
                       y=y_axis[0],  # Use first Y-Axis column for Y values
                       size=size_column,  # Use second Y-Axis (or same Y-Axis for size)
                       title=f"Bubble Chart: {x_axis} vs {', '.join(y_axis)}", 
                       template=theme,
                       color=updated_df[y_axis[0]],  # Color by the first Y-Axis column (optional for categorization)
                       color_continuous_scale=color_scale)  # User-selected color scale

    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
