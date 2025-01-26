import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


def viewer_editor_tab(df):
    st.subheader("Spreadsheet Viewer & Editor")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, resizable=True)
    grid_options = gb.build()
    grid_response = AgGrid(df, gridOptions=grid_options, editable=True)
    updated_df = pd.DataFrame(grid_response["data"])

    return updated_df