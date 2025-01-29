import streamlit as st
import pandas as pd
import plotly.express as px
from editor2.charts.line_chart import line_chart, line_chart_3rd
from editor2.charts.bar_chart import bar_chart, bar_chart_3rd
from editor2.charts.box_plot import box_plot, box_plot_3rd
from editor2.charts.scatter_plot import scatter_plot, scatter_plot_3rd
from editor2.charts.area_chart import area_chart
from editor2.charts.violin_plot import violin_plot
from editor2.charts.bubble_chart import bubble_chart
from editor2.charts.histogram_chart import histogram_chart
from editor2.charts.heatmap_chart import heatmap_chart
from editor2.charts.radar_chart import radar_chart
from editor2.charts.sunburst_chart import sunburst_chart
from editor2.charts.pie_charts import pie_chart


def interactive_charts_tab(updated_df):

    # List to store generated charts
    generated_charts = []

    multi_chart = st.toggle("Multi-Charts")
    if multi_chart:

        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
        with col2:
            color_scale = st.selectbox("Choose Color Scale", ["Viridis", "Cividis", "Plasma", "Inferno", "Jet", "YlGnBu"], key="color_scale")    
        with col3:
            x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
        with col4:
            y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

        col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
        with col1:
            line_chart_selected      = st.checkbox("Line")
        with col2:
            bar_chart_selected       = st.checkbox("Bar")
        with col3:
            scatter_chart_selected   = st.checkbox("Scatter")
        with col4:
            area_chart_selected      = st.checkbox("Area")
        with col5:
            histogram_chart_selected = st.checkbox("Histogram")
        with col6:    
            boxplot_chart_selected   = st.checkbox("Boxplot")

        col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
        with col1:
            violin_chart_selected    = st.checkbox("Violin")
        with col2:
            bubble_chart_selected    = st.checkbox("bubble")
        with col3:
            radar_chart_selected     = st.checkbox("Radar")
        with col4:
            sunburst_chart_selected  = st.checkbox("Sunburst")
        with col5: 
            pie_chart_selected       = st.checkbox("Pie")
        with col6:
            heatmap_chart_selected   = st.checkbox("Heatmap")

        if line_chart_selected:
            fig = line_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if bar_chart_selected:
            fig = bar_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if scatter_chart_selected:
            fig = scatter_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if area_chart_selected:
            fig = area_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if histogram_chart_selected:
            fig = histogram_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if boxplot_chart_selected:
            fig = box_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if violin_chart_selected:
            fig = violin_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if bubble_chart_selected:
            fig = bubble_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if radar_chart_selected:
            fig = radar_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if sunburst_chart_selected:
            fig = sunburst_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if pie_chart_selected:
            fig = pie_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)
        if heatmap_chart_selected:
            fig = heatmap_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
            generated_charts.append(fig)

    else:
        st.subheader("Create Interactive Charts")
        

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            chart_type = st.selectbox(
                            "Select Chart Type", 
                                                ["None", "Line", "Bar", "Scatter", "Area", "Histogram", "Boxplot", "Violin", "Bubble", "Radar", "Sunburst", "Pie", "Heatmap"], 
                                                key="chart_type"
                            )

        with col2:
            pass
        with col3:
            pass
        with col4:
            pass

        if chart_type == "None":
            st.info("Please select a chart type to proceed.")
        elif chart_type == "Line":
            fig = line_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Bar": 
            fig = bar_chart(updated_df, multi_chart)
            generated_charts.append(fig)
        elif chart_type == "Scatter":
            fig = scatter_plot(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Area":
            fig = area_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Boxplot":
             fig = box_plot(updated_df)
             generated_charts.append(fig)
        elif chart_type == "Violin":
            fig = violin_plot(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Bubble":
            fig = bubble_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Histogram":
            fig = histogram_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Heatmap":
            fig = heatmap_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Radar":
            fig = radar_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Sunburst":
            fig = sunburst_chart(updated_df)
            generated_charts.append(fig)
        elif chart_type == "Pie":
            fig = pie_chart(updated_df)
            generated_charts.append(fig)

    # Return the list of generated charts
    return generated_charts


    



def interactive_charts_tab_editor3(updated_df):

    # List to store generated charts
    generated_charts = []

    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        theme = st.selectbox("Choose Chart Theme", ["plotly", "ggplot2", "seaborn", "simple_white", "none"], key="theme")
    with col2:
        color_scale = st.selectbox("Choose Color Scale", ["Viridis", "Cividis", "Plasma", "Inferno", "Jet", "YlGnBu"], key="color_scale")    
    with col3:
        x_axis = st.selectbox("Select X-Axis", updated_df.columns)  # Single column selection for X-Axis
    with col4:
        y_axis = st.multiselect("Select Y-Axis", updated_df.columns)  # Multiple column selection for Y-Axis

    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
    with col1:
        line_chart_selected      = st.checkbox("Line")
    with col2:
        bar_chart_selected       = st.checkbox("Bar")
    with col3:
        box_chart_selected       = st.checkbox("Box")
    with col4:
        scatter_chart_selected   = st.checkbox("Scatter")
    
    multi_chart = None
    if line_chart_selected:
        fig = line_chart_3rd(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        generated_charts.append(fig)
    if bar_chart_selected:
        fig = bar_chart_3rd(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
    if box_chart_selected:
        fig = box_plot_3rd(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        generated_charts.append(fig)
    if scatter_chart_selected:
        fig = scatter_plot_3rd(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        generated_charts.append(fig)

    # Return the list of generated charts
    return generated_charts