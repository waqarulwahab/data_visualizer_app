import streamlit as st
import plotly.express as px

def heatmap_chart(updated_df, multi_chart, x_axis=None, y_axis=None, theme=None, color_scale=None):
    if not multi_chart:
        # Layout for user input (Color Theme, Columns for Correlation, Color Scale)
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            color_scale = st.selectbox("Select Color Scale", ["Viridis", "Cividis", "Plasma", "Inferno", "Blues", "RdBu", "YlGnBu", "YlOrRd"])
        with col3:
            columns = st.multiselect("Select Columns for Correlation", updated_df.columns, default=updated_df.columns.tolist())  # Multiple columns selection for correlation

    # Check if selected columns are numeric (correlation only works with numeric data)
    numeric_columns = updated_df[columns].select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) == 0:
        st.warning("Selected columns must be numeric for correlation.")
    
    # Create the correlation matrix and plot the heatmap
    corr_matrix = updated_df[numeric_columns].corr()  # Compute correlation matrix for numeric columns
    chart = px.imshow(corr_matrix, 
                      color_continuous_scale=color_scale, 
                      title="Heatmap of Correlations", 
                      template=theme)

    # Display the chart
    st.plotly_chart(chart, use_container_width=True)
