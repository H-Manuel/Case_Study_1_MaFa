import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import streamlit as st
import pandas as pd
from devices_inheritance import Device
from users_inheritance import User



def run():
    # Initialisierung
    devices = Device.find_all()
    st.session_state.device_list = [device.id for device in devices]
    st.session_state.device_list.append("Neues Gerät hinzufügen...")
    
    # Lade Nutzer
    all_users = User.find_all()
    user_data = [{ "Email": user.id, "Name": user.name} for user in all_users]
    st.session_state.user_data = pd.DataFrame(user_data)

#UI 

    st.write("# Gerätemanagement")
    st.write("## Geräteauswahl")

    # Dropdown
    st.session_state.sb_current_device = st.selectbox(
        label="Gerät auswählen",
        options=st.session_state.device_list,
    )

    # Zeige das aktuelle Gerät an
    if st.session_state.sb_current_device != "Neues Gerät hinzufügen...":
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Bearbeiten"):
                st.session_state["edit"]=True

            if st.session_state.get("edit", False):
                new_supervisor = st.selectbox(
                    "Neuer Verantwortlicher:", options=st.session_state.user_data,key="new_supervisor"
                )
                
                if st.button("Speichern"):
                    device = Device.find_by_attribute(
                        "id", st.session_state.sb_current_device
                    )
                    if device:
                        device.set_managed_by_user_id(st.session_state.new_supervisor)
                        device.store_data()
                        st.success("Verantwortlicher wurde aktualisiert.")
                        st.session_state["edit"]=False
                        st.rerun()
                if st.button("abbrechen"):
                    st.session_state["edit"]=False
                    st.rerun()

        with col2:
            if st.button("Löschen"):
                device = Device.find_by_attribute(
                    "id", st.session_state.sb_current_device
                )
                if device:
                    device.delete()
                    st.success("Gerät wurde gelöscht.")
                    st.rerun()

    else:
        st.write("### Neues Gerät hinzufügen")
        new_device_name = st.text_input("Gerätename eingeben:")
        new_supervisor = st.selectbox(
                    "Neuer Verantwortlicher:", options=st.session_state.user_data,key="new_supervisor"
                )
        if st.button("Hinzufügen"):
            if new_device_name:
                new_device = Device(id=new_device_name, managed_by_user_id=new_supervisor)
                new_device.store_data()
                st.session_state.device_list.insert(-1, new_device_name)
                st.success("Neues Gerät wurde hinzugefügt.")
                st.rerun()

if __name__ == "__main__":
    run()