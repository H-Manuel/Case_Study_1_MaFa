import streamlit as st
import datetime
import pandas as pd


def run():
    # Initialisiere Reservierungen in Session State
    if "reservierungen" not in st.session_state:
        st.session_state.reservierungen = pd.DataFrame(
            {
                "Name": ["Max Mustermann"],
                "Zeitspanne": ["12.11.2024-12.12.2024"],
                "Startzeit": ["08:00"],
                "Endzeit": ["18:00"],
                "Gerät": ["Laptop"],
            }
        )

    if "reservierung_popup" not in st.session_state:
        st.session_state["reservierung_popup"] = False

    if "reservierung_loeschen_popup" not in st.session_state:
        st.session_state["reservierung_loeschen_popup"] = False

    # Initialisiere Geräte-Liste in Session State
    if "device_list" not in st.session_state:
        st.session_state.device_list = ["Laptop", "Tablet", "Smartphone", "Beamer"]

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
            name = st.text_input("Name")
            datum = st.date_input(
                "Zeitspanne",
                (datetime.date(2024, 1, 1), datetime.date(2024, 1, 7)),
                min_value=datetime.date(2024, 1, 1),
                max_value=datetime.date(2024, 12, 31),
            )
            startzeit = st.time_input("Startzeit", datetime.time(8, 0))
            endzeit = st.time_input("Endzeit", datetime.time(18, 0))
            geraet = st.selectbox(
                label="Gerät auswählen", options=st.session_state.device_list[:-1]
            )
            links, rechts = st.columns(2)
            with links:
                submit_button = st.form_submit_button("Reservieren")
            with rechts:
                abbrechen_button = st.form_submit_button("abbrechen")

            if submit_button and name:
                # Zeitspanne als String formatieren
                zeitspanne = (
                    f"{datum[0].strftime('%d.%m.%Y')}-{datum[1].strftime('%d.%m.%Y')}"
                )
                neue_reservierung = pd.DataFrame(
                    [
                        {
                            "Name": name,
                            "Zeitspanne": zeitspanne,
                            "Startzeit": startzeit.strftime("%H:%M"),
                            "Endzeit": endzeit.strftime("%H:%M"),
                            "Gerät": geraet,
                        }
                    ]
                )
                # Reservierungen aktualisieren mit pd.concat
                st.session_state.reservierungen = pd.concat(
                    [st.session_state.reservierungen, neue_reservierung],
                    ignore_index=True,
                )
                st.success("Reservierung hinzugefügt!")
                st.session_state["reservierung_popup"] = False
                st.rerun()
            elif submit_button:
                st.error("Name darf nicht leer sein")
            if abbrechen_button:
                st.session_state["reservierung_popup"] = False
                st.rerun()

    if st.session_state.get("reservierung_loeschen_popup", False):
        optionen = st.session_state.reservierungen.apply(
            lambda row: f"{row['Name']}, {row['Zeitspanne']}, {row['Startzeit']}, {row['Endzeit']}, {row['Gerät']}",
            axis=1
        )
        line_to_del=st.selectbox("Welche Reservierung soll gelöscht werden", optionen)
        if st.button("Löschen"):
            # Index der zu löschenden Zeile finden
            try:
                index_to_del = optionen[optionen == line_to_del].index[0]
                st.session_state.reservierungen = st.session_state.reservierungen.drop(index=index_to_del).reset_index(drop=True)
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
