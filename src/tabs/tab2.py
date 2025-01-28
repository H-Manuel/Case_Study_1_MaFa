import os,sys
sys.path.append(os.path.dirname(__file__)+"/../")

import streamlit as st
import pandas as pd
from users_inheritance import User

def run():
    if "user_data" not in st.session_state:
        all_users = User.find_all()
        user_data = [{ "Email": user.id, "Name": user.name} for user in all_users]
        st.session_state.user_data = pd.DataFrame(user_data)

    if "add_user_popup" not in st.session_state:
        st.session_state["add_user_popup"] = False
    if "delete_user_popup" not in st.session_state:
        st.session_state["delete_user_popup"] = False

    if st.session_state["add_user_popup"]:
        st.session_state["delete_user_popup"] = False
    if st.session_state["delete_user_popup"]:
        st.session_state["add_user_popup"] = False

    st.write("# Nutzerverwaltung")

    st.write("## Aktuelle Nutzer")
    st.dataframe(st.session_state.user_data)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nutzer hinzufügen"):
            st.session_state["add_user_popup"] = True
    with col2:
        if st.button("Nutzer löschen"):
            st.session_state["delete_user_popup"] = True

    if st.session_state.get("add_user_popup", False):
        with st.form("add_user_form"):
            new_name = st.text_input("Name des neuen Nutzers:")
            new_email = st.text_input("Email-Adresse des neuen Nutzers:")
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Hinzufügen")
            with col2:
                cancel = st.form_submit_button("Abbrechen")

            if submit:
                if new_name and new_email:
                    if new_email not in st.session_state.user_data["Email"].values:
                        new_user = User(new_email, new_name)
                        new_user.store_data()
                        
                        new_entry = {"Name": new_name, "Email": new_email}
                        st.session_state.user_data = pd.concat(
                            [st.session_state.user_data, pd.DataFrame([new_entry])], ignore_index=True
                        )
                        st.success(f"Nutzer '{new_name}' hinzugefügt!")
                        st.session_state["add_user_popup"] = False
                        st.rerun()
                    else:
                        st.error("Diese Email-Adresse existiert bereits.")
                else:
                    st.error("Name und Email dürfen nicht leer sein.")
            if cancel:
                st.session_state["add_user_popup"] = False
                st.rerun()

    if st.session_state.get("delete_user_popup", False):
        if not st.session_state.user_data.empty:
            user_to_delete = st.selectbox(
                "Nutzer auswählen:", st.session_state.user_data.apply(lambda row: f"{row['Name']} ({row['Email']})", axis=1)
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Löschen", key="delete_user_submit"):
                    email_to_delete = user_to_delete.split(" (")[-1][:-1] 
                    user = User.find_by_attribute("id", email_to_delete)
                    if user:
                        user.delete()
                    
                    selected_index = st.session_state.user_data[
                        st.session_state.user_data.apply(
                            lambda row: f"{row['Name']} ({row['Email']})", axis=1
                        ) == user_to_delete
                    ].index[0]
                    st.session_state.user_data = st.session_state.user_data.drop(selected_index).reset_index(drop=True)
                    st.success(f"Nutzer '{user_to_delete}' gelöscht!")
                    st.session_state["delete_user_popup"] = False
                    st.rerun()
            with col2:
                if st.button("Abbrechen", key="delete_user_cancel"):
                    st.session_state["delete_user_popup"] = False
                    st.rerun()
        else:
            st.error("Keine Nutzer vorhanden, die gelöscht werden können.")

if __name__ == "__main__":
    run()