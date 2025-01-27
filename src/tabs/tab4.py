import os
import sys
from datetime import date, datetime
import streamlit as st
import pandas as pd
from reservation_service import ReservationService
from users_inheritance import User
from serializable import Serializable
from tinydb import TinyDB
from devices_inheritance import Device
from maintenance_service import MaintenanceService

# Initialize the database connector
Serializable.db_connector = TinyDB('c:/Schule_24-25/Python_Schule/Case_Study/Case_Study_1_MaFa/src/database.json')

def run():
    reservation_service = ReservationService()

    # Fetch users and devices from the database
    users = User.find_all()
    user_names = [user.id for user in users]
    devices = Device.find_all()
    st.session_state.device_list = [device.id for device in devices]

    # Initialize MaintenanceService
    maintenance_service = MaintenanceService()

    if "maintenance_data" not in st.session_state:
        maintenances = maintenance_service.find_all_maintenances()
        st.session_state.maintenance_data = pd.DataFrame(
            [
                {
                    "Gerät": maintenance.device_id,
                    "Datum": maintenance.end_date,
                    "Kosten (€)": getattr(maintenance, "cost", 0),
                    "Beschreibung": getattr(maintenance, "description", "N/A"),
                }
                for maintenance in maintenances
            ]
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
            device = st.selectbox("Gerät", st.session_state.device_list)
            start_date = st.date_input("Startdatum der Wartung", value=date.today())
            end_date = st.date_input("Enddatum der Wartung", value=date.today())
            interval_months = st.number_input("Intervall (Monate)", min_value=1, step=1)
            cost = st.number_input("Kosten (€)", min_value=0, step=1)
            description = st.text_input("Beschreibung")

            submit_button = st.form_submit_button("Hinzufügen")
            cancel_button = st.form_submit_button("Abbrechen")

            if submit_button:
                st.rerun()
                try:
                    maintenance_service.create_new_maintenance(
                        device_id=device,
                        start_date=datetime.combine(start_date, datetime.min.time()),
                        end_date=datetime.combine(end_date, datetime.min.time()),
                        interval_months=interval_months,
                        cost=cost,
                        description=description
                    )
                    st.success("Wartung erfolgreich hinzugefügt!")
                    st.session_state["add_maintenance_popup"] = False
                    st.rerun()
                except ValueError as e:
                    st.error(f"Fehler: {e}")
                    st.rerun()

            if cancel_button:
                st.session_state["add_maintenance_popup"] = False
                st.rerun()
if __name__ == "__main__":
    run()
