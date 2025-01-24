import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import streamlit as st
from datetime import datetime, date, time
import pandas as pd
from devices_inheritance import Device
from users_inheritance import User
from reservation_service import ReservationService

def run():
    # Initialisiere Reservierungen in Session State

    reservierungen = ReservationService.find_all_reservations()
    formatted_reservierungen = [
        {
            "Name": res.user_id,
            "Startzeit": res.start_date,
            "Endzeit": res.end_date,
            "Gerät": res.device_id
        }
        for res in reservierungen
    ]
    st.session_state.reservierungen = pd.DataFrame(formatted_reservierungen)

    all_users = User.find_all()
    user_data = [{ "Email": user.id, "Name": user.name} for user in all_users]
    st.session_state.user_data = pd.DataFrame(user_data)

    if "reservierung_popup" not in st.session_state:
        st.session_state["reservierung_popup"] = False

    if "reservierung_loeschen_popup" not in st.session_state:
        st.session_state["reservierung_loeschen_popup"] = False

    # Initialisiere Geräte-Liste in Session State
    devices = Device.find_all()
    st.session_state.device_list = [device.id for device in devices]

    # Überschrift
    st.write("# Reservierungssystem")

    # Reservierungen anzeigen
    st.write("## Reservierungen")
    st.dataframe(st.session_state.reservierungen)

    col_links, col_rechts = st.columns(2)
    with col_links:
        if st.button("## Reservierung tätigen"):
            st.session_state["reservierung_popup"] = True
    with col_rechts:
        if st.button("## Reservierung löschen"):
            st.session_state["reservierung_loeschen_popup"] = True

    if st.session_state.get("reservierung_popup", False):
        with st.form("reservierung_form"):
            name = st.selectbox(
                    "User", options=st.session_state.user_data,key="user"
                )
            datum = st.date_input(
                "Zeitspanne",
                (date(2024, 1, 1), date(2024, 1, 7)),
                min_value=date(2024, 1, 1),
                max_value=date(2024, 12, 31),
            )
            start_time = st.time_input("Startzeit", time(8, 0))
            end_time = st.time_input("Endzeit", time(18, 0))

            startzeit = datetime.combine(datum[0], start_time)
            endzeit = datetime.combine(datum[1], end_time)
            geraet = st.selectbox(
                label="Gerät auswählen", options=st.session_state.device_list
            )
            links, rechts = st.columns(2)
            with links:
                submit_button = st.form_submit_button("Reservieren")
            with rechts:
                abbrechen_button = st.form_submit_button("abbrechen")

            if submit_button and name:
                if(ReservationService.check_conflict(geraet,startzeit,endzeit)):
                    st.error("Reservierungskonflikt!")
                    return
                ReservationService.create_reservation(name,geraet,startzeit,endzeit)
                st.success("Reservierung hinzugefügt!")
                st.session_state["reservierung_popup"] = False
                st.rerun()
            elif submit_button:
                st.error("Name darf nicht leer sein")
            if abbrechen_button:
                st.session_state["reservierung_popup"] = False
                st.rerun()

    if st.session_state.get("reservierung_loeschen_popup", False):
        reservierung=ReservationService()
        auswahl=st.selectbox("Reservierung auswählen", options=reservierung.find_all_reservations())
        if st.button("Löschen"):
            # Index der zu löschenden Zeile finden
            try:
                auswahl.delete()
                st.success("Reservierung gelöscht!")
                st.session_state["reservierung_loeschen_popup"]=False
                st.rerun()
            except IndexError:
                st.error("Reservierung nicht gefunden")
        if st.button("abbrechen"):
            st.session_state["reservierung_loeschen_popup"]=False
            st.rerun()

if __name__ == "__main__":
    run()
