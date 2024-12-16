import streamlit as st

def update_name_tab_1():
    st.session_state.name = st.session_state.ti_tab1_name
    st.session_state.ti_tab2_name = st.session_state.ti_tab1_name

def run():

    # Initialisiere Session-State
    if "sb_current_device" not in st.session_state:
        st.session_state.sb_current_device = ""

    if "show_modal" not in st.session_state:
        st.session_state["show_modal"] = False

    if "device_list" not in st.session_state:
        # Geräteliste mit Standardwerten initialisieren
        st.session_state.device_list = ["Gerät_A", "Gerät_B", "Neues Gerät hinzufügen..."]

    # Eine Überschrift der ersten Ebene
    st.write("# Gerätemanagement")

    # Eine Überschrift der zweiten Ebene
    st.write("## Geräteauswahl")

    # Geräteliste aus Session-State verwenden
    device_list = st.session_state.device_list

    # Suchleiste/Dropdown für Geräteauswahl
    st.session_state.sb_current_device = st.selectbox(
        label="Gerät auswählen",
        options=device_list,
    )

    if st.button("löschen"):
        st.session_state["popup"]= True
        if st.session_state.get("popup", False):
            st.write ("### Sind Sie sicher?")
            left, right =st.columns(2)
            with left:
                if st.button("Ja"):
                    if st.session_state.sb_current_device in st.session_state.device_list:
                        st.session_state.device_list.remove(st.session_state.sb_current_device)
                    else:
                        st.write("Das Gerät existiert nicht in der Liste.")
                    print(st.session_state.device_list)
                    st.session_state["popup"]=False
                    st.session_state.sb_current_device= st.session_state.device_list[1]
                    st.rerun()

            with right:
                if st.button("Abbrechen"):
                    st.session_state["popup"]=False
                

    # Logik für den letzten Eintrag (Neues Gerät hinzufügen)
    if st.session_state.sb_current_device == "Neues Gerät hinzufügen...":
        st.session_state["show_modal"] = True  # Zeige Modal-Inhalt

    # Zeige das aktuell ausgewählte Gerät an
    st.write(f"Das ausgewählte Gerät ist: {st.session_state.sb_current_device}")

    # Modales Fenster (Inhalt erscheint unterhalb der Hauptseite)
    if st.session_state.get("show_modal", False):
        st.write("### Neues Gerät hinzufügen")
        new_device_name = st.text_input("Name des neuen Geräts eingeben:", key="new_device_name")
        if st.button("Hinzufügen"):
            if new_device_name:
                st.session_state.sb_current_device = new_device_name
                # Füge das neue Gerät in die Liste vor "Neues Gerät hinzufügen..." ein
                st.session_state.device_list.insert(-1, new_device_name)
                st.session_state["show_modal"] = False  # Fenster schließen
                st.rerun()   
            else:
                st.error("Der Gerätename darf nicht leer sein.")
        if st.session_state.get("show_modal", True):
            st.session_state["show_modal"] = False  # Fenster schließen
            st.rerun() 