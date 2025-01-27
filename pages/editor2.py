import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
from io import BytesIO

from editor2.helper_functions.tab1 import viewer_editor_tab
from editor2.helper_functions.tab2 import interactive_charts_tab

# Custom CSS for styling and hiding the Mito banner
st.markdown(
    """
    <style>
        .mito-pro-banner {
            display: none !important;
        }    
        .main {
            background-color: #f5f5f5;
        }
        h1, h2, h3, h4 {
            color: #4CAF50;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border-radius: 5px;
            padding: 0.5em 1em;
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

import sys

# Import win32com only if running on Windows
if sys.platform == "win32":
    import win32com.client


# Sidebar logo
st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

# File upload section in the sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file", 
    type=["csv", "xlsx"], 
    help="Drag and drop or click to upload a CSV or Excel file."
)

if uploaded_file:
    # Load File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        sheets = {"Sheet1": df}
    else:
        sheets = pd.read_excel(uploaded_file, sheet_name=None)

    # Sidebar for Sheet Selection
    with st.sidebar:
        sheet_names = list(sheets.keys())
        selected_sheet = st.selectbox("Select a Sheet", sheet_names)
        df = sheets[selected_sheet]

    # Ensure all column names are strings and stripped of whitespace
    df.columns = [str(col).strip() for col in df.columns]

    # Check for potential date columns
    date_columns = [
        col for col in df.columns 
        if pd.to_datetime(df[col], errors='coerce').notnull().any()  # Check for at least one valid date
    ]

    if date_columns:
        # Automatically use the first valid date column
        date_column = date_columns[0]
        # Convert to datetime and drop invalid entries
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df[df[date_column].notnull()]  # Remove rows with invalid dates
        df[date_column] = df[date_column].dt.date  # Convert to date only

        # Date Range Filter
        if not df.empty:  # Check if the DataFrame is not empty
            min_date = df[date_column].min()
            max_date = df[date_column].max()

            # Add date range pickers
            col1, col2 = st.sidebar.columns([1,1])
            with col1:
                start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
            with col2:
                end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

            # Filter DataFrame based on the date range
            if start_date and end_date:
                df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

    # Check if the DataFrame is empty after filtering
    if df.empty:
        st.error("No data available after filtering.")
    else:
        # Main Layout
        tab1, tab2, tab3 = st.tabs(["📋 Data Editor", "📈 Visualization", "💾 Export Data"])

        # Tab 1: Data Editor
        with tab1:
            updated_df = viewer_editor_tab(df)

        # Tab 2: Visualization
        with tab2:
            try:
                interactive_charts_tab(updated_df)
            except KeyError as e:
                st.error(f"Error: Column {e} not found in the dataset.")

        # Tab 3: Export Data
        with tab3:
            st.subheader("Export Modified Data")
            def to_excel(sheets):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    for sheet_name, sheet_data in sheets.items():
                        sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
                processed_data = output.getvalue()
                return processed_data

            export_data = to_excel({selected_sheet: updated_df})
            st.download_button(
                label="📥 Download Excel File",
                data=export_data,
                file_name="updated_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
else:
    st.info("Please upload a file to get started.")





# import streamlit as st
# import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder
# import plotly.express as px
# from io import BytesIO

# from editor2.helper_functions.tab1 import viewer_editor_tab
# from editor2.helper_functions.tab2 import interactive_charts_tab

# # Custom CSS for styling and hiding the Mito banner
# st.markdown(
#     """
#     <style>
#         .mito-pro-banner {
#             display: none !important;
#         }    
#         .main {
#             background-color: #f5f5f5;
#         }
#         h1, h2, h3, h4 {
#             color: #4CAF50;
#         }
#         .stButton>button {
#             color: white;
#             background-color: #4CAF50;
#             border-radius: 5px;
#             padding: 0.5em 1em;
#             font-size: 16px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# import sys

# # Import win32com only if running on Windows
# if sys.platform == "win32":
#     import win32com.client


# # Sidebar logo
# st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

# # File upload section in the sidebar
# uploaded_file = st.sidebar.file_uploader(
#     "Upload your CSV or Excel file", 
#     type=["csv", "xlsx"], 
#     help="Drag and drop or click to upload a CSV or Excel file."
# )

# if uploaded_file:
#     # Load File
#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#         sheets = {"Sheet1": df}
#     else:
#         sheets = pd.read_excel(uploaded_file, sheet_name=None)

#     # Sidebar for Sheet Selection
#     with st.sidebar:
#         sheet_names = list(sheets.keys())
#         selected_sheet = st.selectbox("Select a Sheet", sheet_names)
#         df = sheets[selected_sheet]

#     # Ensure all column names are strings
#     df.columns = [str(col) for col in df.columns]

#     # Check for potential date columns
#     date_columns = [
#         col for col in df.columns 
#         if pd.to_datetime(df[col], errors='coerce').notnull().any()  # Check for at least one valid date
#     ]

#     if date_columns:
#         # Automatically use the first valid date column
#         date_column = date_columns[0]
#         # Convert to datetime and drop invalid entries
#         df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
#         df = df[df[date_column].notnull()]  # Remove rows with invalid dates
#         df[date_column] = df[date_column].dt.date  # Convert to date only

#         # Date Range Filter
#         st.sidebar.subheader("Date Range Filter")
#         min_date = df[date_column].min()
#         max_date = df[date_column].max()

#         # Add date range pickers
#         start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
#         end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

#         # Filter DataFrame based on the date range
#         if start_date and end_date:
#             df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

#     # Main Layout
#     tab1, tab2, tab3 = st.tabs(["📋 Data Editor", "📈 Visualization", "💾 Export Data"])

#     # Tab 1: Data Editor
#     with tab1:
#         updated_df = viewer_editor_tab(df)

#     # Tab 2: Visualization
#     with tab2:
#         interactive_charts_tab(updated_df)

#     # Tab 3: Export Data
#     with tab3:
#         st.subheader("Export Modified Data")
#         def to_excel(sheets):
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#                 for sheet_name, sheet_data in sheets.items():
#                     sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
#             processed_data = output.getvalue()
#             return processed_data

#         export_data = to_excel({selected_sheet: updated_df})
#         st.download_button(
#             label="📥 Download Excel File",
#             data=export_data,
#             file_name="updated_file.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         )
# else:
#     st.info("Please upload a file to get started.")






# import streamlit as st
# import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder
# import plotly.express as px
# from io import BytesIO

# from editor2.helper_functions.tab1 import viewer_editor_tab
# from editor2.helper_functions.tab2 import interactive_charts_tab

# # Custom CSS for styling and hiding the Mito banner
# st.markdown(
#     """
#     <style>
#         .mito-pro-banner {
#             display: none !important;
#         }    
#         .main {
#             background-color: #f5f5f5;
#         }
#         h1, h2, h3, h4 {
#             color: #4CAF50;
#         }
#         .stButton>button {
#             color: white;
#             background-color: #4CAF50;
#             border-radius: 5px;
#             padding: 0.5em 1em;
#             font-size: 16px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# import sys

# # Import win32com only if running on Windows
# if sys.platform == "win32":
#     import win32com.client


# # Sidebar logo
# st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

# # File upload section in the sidebar
# uploaded_file = st.sidebar.file_uploader(
#     "Upload your CSV or Excel file", 
#     type=["csv", "xlsx"], 
#     help="Drag and drop or click to upload a CSV or Excel file."
# )

# # Sidebar navigation links
# st.sidebar.page_link("main.py", label="Editor-1", icon="1️⃣")
# st.sidebar.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")

# if uploaded_file:
#     # Load File
#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#         sheets = {"Sheet1": df}
#     else:
#         sheets = pd.read_excel(uploaded_file, sheet_name=None)

#     # Sidebar for Sheet Selection
#     with st.sidebar:
#         sheet_names = list(sheets.keys())
#         selected_sheet = st.selectbox("Select a Sheet", sheet_names)
#         df = sheets[selected_sheet]

#     # Check for Date Column
#     date_columns = [col for col in df.columns if pd.to_datetime(df[col], errors='coerce').notnull().all()]
#     if date_columns:
#         # Use the first detected date column
#         date_column = date_columns[0]
#         df[date_column] = pd.to_datetime(df[date_column]).dt.date  # Remove time from date column

#         # Date Range Filter
#         st.sidebar.subheader("Date Range Filter")
#         min_date = df[date_column].min()
#         max_date = df[date_column].max()
#         start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
#         end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

#         # Filter DataFrame based on the date range
#         if start_date and end_date:
#             df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

#     # Main Layout
#     tab1, tab2, tab3 = st.tabs(["📋 Data Editor", "📈 Visualization", "💾 Export Data"])

#     # Tab 1: Data Editor
#     with tab1:
#         updated_df = viewer_editor_tab(df)

#     # Tab 2: Visualization
#     with tab2:
#         interactive_charts_tab(updated_df)

#     # Tab 3: Export Data
#     with tab3:
#         st.subheader("Export Modified Data")
#         def to_excel(sheets):
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#                 for sheet_name, sheet_data in sheets.items():
#                     sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
#             processed_data = output.getvalue()
#             return processed_data

#         export_data = to_excel({selected_sheet: updated_df})
#         st.download_button(
#             label="📥 Download Excel File",
#             data=export_data,
#             file_name="updated_file.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         )
# else:
#     st.info("Please upload a file to get started.")










# import streamlit as st
# import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder
# import plotly.express as px
# from io import BytesIO

# from editor2.helper_functions.tab1 import viewer_editor_tab
# from editor2.helper_functions.tab2 import interactive_charts_tab

# # Custom CSS for styling and hiding the Mito banner
# st.markdown(
#     """
#     <style>
#         .mito-pro-banner {
#             display: none !important;
#         }    
#         .main {
#             background-color: #f5f5f5;
#         }
#         h1, h2, h3, h4 {
#             color: #4CAF50;
#         }
#         .stButton>button {
#             color: white;
#             background-color: #4CAF50;
#             border-radius: 5px;
#             padding: 0.5em 1em;
#             font-size: 16px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# import sys

# # Import win32com only if running on Windows
# if sys.platform == "win32":
#     import win32com.client


# # Sidebar logo
# st.sidebar.image("LOGO.jpg", width=300, use_container_width=False)  # Update 'path_to_logo/logo.png' with the correct path

# # File upload section in the sidebar
# uploaded_file = st.sidebar.file_uploader(
#     "Upload your CSV or Excel file", 
#     type=["csv", "xlsx"], 
#     help="Drag and drop or click to upload a CSV or Excel file."
# )

# # Sidebar navigation links
# st.sidebar.page_link("main.py", label="Editor-1", icon="1️⃣")
# st.sidebar.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")

# if uploaded_file:
#     # Load File
#     if uploaded_file.name.endswith(".csv"):
#         df = pd.read_csv(uploaded_file)
#         sheets = {"Sheet1": df}
#     else:
#         sheets = pd.read_excel(uploaded_file, sheet_name=None)

#     # Sidebar for Sheet Selection
#     with st.sidebar:
#         sheet_names = list(sheets.keys())
#         selected_sheet = st.selectbox("Select a Sheet", sheet_names)
#         df = sheets[selected_sheet]

#     # Main Layout
#     tab1, tab2, tab3 = st.tabs(["📋 Data Editor", "📈 Visualization", "💾 Export Data"])

#     # Tab 1: Data Editor
#     with tab1:
#         updated_df = viewer_editor_tab(df)


#     # Tab 2: Visualization
#     with tab2:
#         interactive_charts_tab(updated_df)



#     # Tab 3: Export Data
#     with tab3:
#         st.subheader("Export Modified Data")
#         def to_excel(sheets):
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#                 for sheet_name, sheet_data in sheets.items():
#                     sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
#             processed_data = output.getvalue()
#             return processed_data

#         export_data = to_excel({selected_sheet: updated_df})
#         st.download_button(
#             label="📥 Download Excel File",
#             data=export_data,
#             file_name="updated_file.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         )
# else:
#     st.info("Please upload a file to get started.")
