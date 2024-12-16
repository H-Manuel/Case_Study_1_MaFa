import streamlit as st

from tabs import tab1, tab2

tab_1, tab_2 = st.tabs(["Geräteverwaltung", "Tab 2"])

with tab_1:
   tab1.run()
with tab_2:
   tab2.run()
