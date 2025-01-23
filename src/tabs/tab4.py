import os, sys
sys.path.append(os.path.dirname(__file__) + "/../")

import streamlit as st
import pandas as pd
from datetime import date
from reservation_service import ReservationService
from users_inheritance import User
from serializable import Serializable
from tinydb import TinyDB
from devices_inheritance import Device  

# Initialize the database connector
Serializable.db_connector = TinyDB('c:/Schule_24-25/Python_Schule/Case_Study/Case_Study_1_MaFa/src/database.json')

def run():
    reservation_service = ReservationService()

    # Fetch users from the database using User.find_all()
    users = User.find_all()
    user_names = [user.id for user in users]
    devices = Device.find_all()
    st.session_state.device_list = [device.id for device in devices]

    if "maintenance_data" not in st.session_state:
        st.session_state.maintenance_data = pd.DataFrame(
            {
                "Gerät": ["Laptop", "Beamer"], #device list hier eintragen
                "Datum": ["2024-01-15", "2024-01-20"],  #datum aus datenbank
                "Kosten (€)": [120.50, 80.00],  #kosten aus datenbank
                "Beschreibung": ["Reparatur Tastatur", "Lampenwechsel"],    #beschreibung aus datenbank
            }
        )

    if "add_maintenance_popup" not in st.session_state:
        st.session_state["add_maintenance_popup"] = False

    # Titel
    st.write("# Wartungsmanagement")

    # Wartungskosten und Historie anzeigen
    st.write("## Wartungskosten und Historie")
    st.dataframe(st.session_state.maintenance_data)

    # Gesamtkosten berechnen
    total_cost = st.session_state.maintenance_data["Kosten (€)"].sum()
    st.write(f"### Gesamtkosten der Wartungen: {total_cost:.2f} €")

    # Button für neue Wartung
    if st.button("Neue Wartung hinzufügen"):
        st.session_state["add_maintenance_popup"] = True

    # Popup: Neue Wartung hinzufügen
    if st.session_state.get("add_maintenance_popup", False):
        with st.form("maintenance_form"):
            device = st.text_input("Gerät") #devices aus datenbank dropdown
            date_performed = st.date_input("Datum der Wartung", value=date.today()) #start und enddatum eintragen
            cost = st.number_input("Kosten (€)", min_value=0.0, step=0.01)
            description = st.text_area("Beschreibung")
            submit_button = st.form_submit_button("Hinzufügen")
            cancel_button = st.form_submit_button("Abbrechen")

            if submit_button:
                if device and cost > 0 and description:
                    new_entry = {
                        "Gerät": device,
                        "Datum": date_performed.strftime("%Y-%m-%d"),
                        "Kosten (€)": cost,
                        "Beschreibung": description,
                    }
                    st.session_state.maintenance_data = pd.concat(
                        [
                            st.session_state.maintenance_data,
                            pd.DataFrame([new_entry]),
                        ],
                        ignore_index=True,
                    )
                    st.success("Wartung erfolgreich hinzugefügt!")
                    st.session_state["add_maintenance_popup"] = False
                    st.rerun()
                else:
                    st.error("Alle Felder müssen korrekt ausgefüllt sein.")
            if cancel_button:
                st.session_state["add_maintenance_popup"] = False
                st.rerun()

if __name__ == "__main__":
    run()
