import streamlit as st
import os
import time
from helper_functions.utils import display_logo, page_navigations, clear_import_folder

st.set_page_config(layout="wide")

# Hide MitoSheet Pro Banner
st.markdown("""
    <style>
        .mito-pro-banner {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Display logo and navigation
display_logo()
page_navigations()

# Define the import folder
IMPORT_FOLDER = './data'
if not os.path.exists(IMPORT_FOLDER):
    os.makedirs(IMPORT_FOLDER)

# Main title
st.title("📊 Data Analysis & Visualization Platform")

# Section: About the Application
st.markdown("""
### **About This Application**
This platform is designed to help users **analyze and visualize their data with ease**. 
It provides **interactive charts, advanced analytics, and insightful reports** to assist in **data-driven decision-making**.

**Features:**
- 📂 **Upload & Process CSV/Excel Files**
- 📈 **Generate Interactive Charts**
- 🛠️ **Identify Trends & Anomalies**
- 🔍 **Extract Insights for Better Decision-Making**
- ⚡ **Fast & User-Friendly Interface**
""")

# Section: Instructions for Users
st.markdown("""
### **How to Use This Platform?**
1. **Upload Your Data** 📂  
   - Click on the **"Upload your CSV or Excel file"** button in the sidebar.
   - Supported formats: **CSV, XLS, XLSX**.
   - Ensure the data has **clear headers** and structured format.

2. **Analyze Your Data** 📊  
   - After uploading, explore **dynamic visualizations**.
   - Choose from **line charts, bar charts, scatter plots, box plots**, and more.

3. **Customize & Export** 🛠️  
   - Customize charts with **different themes, colors, and axis selections**.
   - Export analysis results for **further reporting and presentations**.

4. **Gain Insights** 🔍  
   - Identify **trends, patterns, and outliers**.
   - Make **data-driven decisions** with confidence.
""")

# Sidebar: File upload section
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xls", "xlsx"],
    help="Drag and drop or click to upload a CSV or Excel file."
)

if uploaded_file:
    clear_import_folder(IMPORT_FOLDER)
    file_path = os.path.join(IMPORT_FOLDER, uploaded_file.name)
    # Save the new file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("✅ File uploaded successfully!")
    time.sleep(1)  # Wait for 3 seconds
    st.switch_page("pages/editor1.py")

# Final Section: Additional Support
st.markdown("""
---
### **Need Help?**
📧 **Support Email:** support@example.com  
💡 **Tips:** Ensure your dataset is **clean and formatted** before analysis for better insights.
""")
