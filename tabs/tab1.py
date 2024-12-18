import streamlit as st


def run():
    if "sb_current_device" not in st.session_state:
        st.session_state.sb_current_device = ""

    if "add_device_popup" not in st.session_state:
        st.session_state["add_device_popup"] = False

    if "edit_popup" not in st.session_state:
        st.session_state["edit_popup"] = False

    if "delete_popup" not in st.session_state:
        st.session_state["delete_popup"] = False    

    if "device_list" not in st.session_state:
        st.session_state.device_list = [
            "Gerät_A",
            "Gerät_B",
            "Neues Gerät hinzufügen...",
        ]

    if "supervisor_dict" not in st.session_state:
        st.session_state.supervisor_dict = {
            "Gerät_A": "Max Mustermann",
            "Gerät_B": "Max Mustermann",
            "Neues Gerät hinzufügen...": " ",
        }

    st.write("# Gerätemanagement")

    st.write("## Geräteauswahl")

    # Geräteliste aus Session-State verwenden
    #device_list = st.session_state.device_list

    # Dropdown
    st.session_state.sb_current_device = st.selectbox(
        label="Gerät auswählen",
        options=st.session_state.device_list,######
    )

    # Zeige das aktuelle Gerät an
    st.write(
        f"Das ausgewählte Gerät ist: {st.session_state.sb_current_device} mit dem Verantwortlichen: {st.session_state.supervisor_dict[st.session_state.sb_current_device]}"
    )

    if st.session_state.sb_current_device != "Neues Gerät hinzufügen...":
        st.session_state["add_device_popup"] = False  
        col1, col2 = st.columns(2)

        with col1:
            if st.button("bearbeiten"):
                st.session_state["edit_popup"] = True

        with col2:
            if st.button("löschen"):
                st.session_state["delete_popup"] = True

    if st.session_state.sb_current_device == "Neues Gerät hinzufügen...":
        st.session_state["add_device_popup"] = True  

    if st.session_state.get("edit_popup", False):
        st.write(f"Gerät: {st.session_state.sb_current_device}")
        device_supervisor_update = st.text_input(
            "Name des Verantwortlichen für dieses Gerät eingeben:",
            value=st.session_state.supervisor_dict.get(
                st.session_state.sb_current_device, ""
            ),
            key="device_supervisor_update",
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Speichern"):
                st.session_state.supervisor_dict[st.session_state.sb_current_device] = (
                    device_supervisor_update
                )
                st.session_state["edit_popup"] = False
                st.success(
                    f"Verantwortlicher für {st.session_state.sb_current_device} wurde aktualisiert!"
                )
                st.rerun()
        with col2:
            if st.button("Abbrechen"):
                st.session_state["edit_popup"] = False

    if st.session_state.get("delete_popup", False):
        st.write("### Sind Sie sicher?")
        left, right = st.columns(2)
        with left:
            # st.write(f"device={st.session_state.sb_current_device} device list {st.session_state.device_list}")
            if "show_message" not in st.session_state:
                st.session_state.show_message = False 

            if st.button("Ja"):
                st.session_state.show_message = (
                    True
                )

            if st.session_state.show_message:
                # st.write("ja gedrückt")
                if st.session_state.sb_current_device in st.session_state.device_list:
                    st.session_state.device_list.remove(
                        st.session_state.sb_current_device
                    )
                    st.session_state.supervisor_dict.pop(
                        st.session_state.sb_current_device, None
                    )
                    st.session_state.sb_current_device = st.session_state.device_list[-1]  
                    st.session_state["delete_popup"] = False
                    st.session_state.show_message = False
                    st.success(f"{st.session_state.sb_current_device} wurde gelöscht.")
                    st.rerun()
                else:
                    st.write("Das Gerät existiert nicht in der Liste.")
        with right:
            if st.button("Abbrechen"):
                st.session_state["delete_popup"] = False

    if st.session_state.get("add_device_popup", False):
        st.write("### Neues Gerät hinzufügen")
        new_device_name = st.text_input(
            "Name des neuen Geräts eingeben:", key="new_device_name"
        )
        device_supervisor = st.text_input(
            "Name des Verantwortlichen für dieses Gerät eingeben",
            key="device_supervisor",
        )
        if st.button("Hinzufügen"):
            if new_device_name:
                st.session_state.sb_current_device = new_device_name
                st.session_state.supervisor_dict[st.session_state.sb_current_device] = (
                    device_supervisor
                )
                st.session_state.device_list.insert(-1, new_device_name)
                st.session_state["add_device_popup"] = False  
                st.rerun()
            else:
                st.error("Der Gerätename darf nicht leer sein.")


if __name__ == "__main__":
    run()
