import streamlit as st

from tabs import tab1, tab2, tab3 

tab_1, tab_2, tab_3 = st.tabs(["Geräteverwaltung", "Tab 2", "Reservierungssystem"])


with tab_1:
    tab1.run()  
with tab_2:
    tab2.run()  
with tab_3:
    tab3.run()  
