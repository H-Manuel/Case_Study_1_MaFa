import streamlit as st

def update_name_tab_2():
    st.session_state.name = st.session_state.ti_tab2_name
    st.session_state.ti_tab1_name = st.session_state.ti_tab2_name

def run():
    st.title("Tab 2")
    st.session_state.name = st.text_input("Enter animal name", key="ti_tab2_name",on_change=update_name_tab_2)
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
