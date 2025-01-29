import streamlit as st

def page_navigations():
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,3,3,3])
    with col1:
        st.page_link("main.py", label="Editor-1", icon="1️⃣")
    with col2:
        st.page_link("pages/editor2.py", label="Editor-2", icon="2️⃣")
    with col3:
        st.page_link("pages/editor3.py", label="Editor-3", icon="3️⃣")