import streamlit as st
import plotly.express as px

def violin_plot(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (X-Axis, Y-Axis, Color Theme)
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            theme = st.selectbox(
                "Choose Chart Theme", 
                ["plotly", "ggplot2", "seaborn", "simple_white", "none"], 
                key="violin_theme"
            )
        with col2:
            x_axis = st.selectbox(
                "Select X-Axis", 
                updated_df.columns, 
                help="Choose a column for the X-Axis (categorical or numeric)."
            )  # Single column selection for X-Axis
        with col3:
            y_axis = st.multiselect(
                "Select Y-Axis", 
                updated_df.columns, 
                help="Select one or more columns for the Y-Axis (numeric only)."
            )  # Multiple column selection for Y-Axis

    # Validate X-Axis
    if not x_axis:
        st.warning("Please select a column for the X-Axis.")
        return

    if updated_df[x_axis].dtype not in ['object', 'category', 'int64', 'float64']:
        st.warning(f"The column '{x_axis}' in X-Axis is not suitable for a Violin Plot.")
        return

    # Validate Y-Axis
    if not y_axis:
        st.warning("Please select at least one column for the Y-Axis.")
        return

    for col in y_axis:
        if updated_df[col].isnull().any():
            st.warning(f"The column '{col}' contains missing values. These rows will be excluded.")
        if updated_df[col].dtype not in ['int64', 'float64']:
            st.warning(f"The column '{col}' in Y-Axis must be numeric.")
            return

    # Melt the DataFrame to create a unified structure for plotting
    try:
        melted_df = updated_df.melt(
            id_vars=[x_axis], 
            value_vars=y_axis, 
            var_name='Y-Axis Column', 
            value_name='Values'
        )

        # Create the violin plot using Plotly
        chart = px.violin(
            melted_df, 
            x=x_axis, 
            y='Values', 
            color='Y-Axis Column',  # Differentiate by the Y-Axis column
            title=f"Violin Plot: {x_axis} vs {', '.join(y_axis)}", 
            template=theme,
            box=True,  # Include box plot inside the violin plot
            points="all",  # Show individual data points
            color_discrete_sequence=px.colors.qualitative.Set1  # Custom color palette
        )

        # Display the chart
        st.plotly_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while creating the Violin Plot: {e}")
