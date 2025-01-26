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
        bar_chart(updated_df)
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



    



