import streamlit as st
import pandas as pd
import plotly.express as px
from editor2.charts.line_chart import line_chart
from editor2.charts.bar_chart import bar_chart
from editor2.charts.scatter_plot import scatter_plot
from editor2.charts.area_chart import area_chart
from editor2.charts.box_plot import box_plot
from editor2.charts.violin_plot import violin_plot
from editor2.charts.bubble_chart import bubble_chart
from editor2.charts.histogram_chart import histogram_chart
from editor2.charts.heatmap_chart import heatmap_chart
from editor2.charts.radar_chart import radar_chart
from editor2.charts.sunburst_chart import sunburst_chart
from editor2.charts.pie_charts import pie_chart


def interactive_charts_tab(updated_df):

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
            line_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if bar_chart_selected:
            bar_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if scatter_chart_selected:
            scatter_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if area_chart_selected:
            area_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if histogram_chart_selected:
            histogram_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if boxplot_chart_selected:
            box_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if violin_chart_selected:
            violin_plot(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if bubble_chart_selected:
            bubble_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if radar_chart_selected:
            radar_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if sunburst_chart_selected:
            sunburst_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if pie_chart_selected:
            pie_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)
        if heatmap_chart_selected:
            heatmap_chart(updated_df, multi_chart, x_axis, y_axis, theme, color_scale)

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
            line_chart(updated_df)
        elif chart_type == "Bar": 
            bar_chart(updated_df, multi_chart)
        elif chart_type == "Scatter":
            scatter_plot(updated_df)
        elif chart_type == "Area":
            area_chart(updated_df)
        elif chart_type == "Boxplot":
            box_plot(updated_df)
        elif chart_type == "Violin":
            violin_plot(updated_df)
        elif chart_type == "Bubble":
            bubble_chart(updated_df)
        elif chart_type == "Histogram":
            histogram_chart(updated_df)
        elif chart_type == "Heatmap":
            heatmap_chart(updated_df)
        elif chart_type == "Radar":
            radar_chart(updated_df)
        elif chart_type == "Sunburst":
            sunburst_chart(updated_df)
        elif chart_type == "Pie":
            pie_chart(updated_df)



    



