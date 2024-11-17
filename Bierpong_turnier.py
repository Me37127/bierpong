import json
import pandas as pd
import streamlit as st
import requests
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Dein Service Account JSON-Daten als Python Dictionary (aus deiner Datei)
service_account_info = {
  "type": "service_account",
  "project_id": "bierpongturnier",
  "private_key_id": "ea13df843d5889c3544d37088a9691be3579a810",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDXpRgIGMMpZOh1\nhMhheTXYPwd1Qm9UAGrs/BDuGVd8s67IZlr3rq1Vi/fClBMfbS9YZiA0pca9L/K4\njn/HdEUnogymTccWJl0WCUl0EjOXyan7+q545WCNjCMYVt4nECGPeQX40HV3p3Pu\nO9kkPfvT65h/m6g3Bu3t9Qse79wh6AIOyuq0q/VSO9bHp6zRsOM1Zq0DRKFEXln0\n2WZ+oIdZtob2wHw5GV+YvCJdcTdvtxteSWbruEtyu284f21syiqmnYL6bC+Vj+jd\nL1MpsxgEh/M67hTMPuMZ1NGLpxsL1QwdbDtX82cargwsE0TeA5T1aKdrC/ZkDTPU\n9WL8DjTtAgMBAAECggEAFpxrN2gfSI8Z176vQxcyR+Ud+1PWuAReMdChVtHl7D+r\n7zvaRHe2mY52UVr04Vnxua9lp5eNTeeB6AubBtcgbC4v7N0hZ6dooceiAc9pxPvi\nfLcVhbwpYlYkFOiA3TAyEKjkMSlsc7olbACu/T+ZkOg2YoT3/6MUnhuQSbNlTdGk\nY9q140OYIf7z3fAk201qm/fR/g5N0iV8/YgARIV3n/gBfb/Yeh5RvKFrKXEbSae0\nn9tMeAEzz15Xaj1KE7YTZbQg5CgCgEz/2tGeTGjmHFnAE0uKwbZhzbdwWEVRaF9z\naaOjXFexJyG3KRzKMaYP1YaEIMDtXqLghp6S1nez8QKBgQDvFTUOw82JgQWsyP55\nWk3IT4ZKqjApXl4PPpgRTTmPG3bjfDAtD9HSh3GY8xKq6uCzIZ5Wm1RCrShdlFl/\ngZ6Qjqyqs3NyfhpTctUprEA6DdnzYfN11ooO82G5vvBO+m0Hu3w6f+t35Ot1faw2\npRB7JZDv4yai/lsXsuvgRwe1vQKBgQDm51PC9oqagwDD/PcpoiA6aOkhijwe2DvM\nyvM6Xok1wHlrxknagHO692APBdRYw2ypIY87cV0L9rKQ3q0E5R7DjlxkvfbqqQnb\npV0N393JAhzOBytnML+tp2LIYo/luDT6VHfjHaziyHY8KRdPstgqtm6D6itzqCXL\ny34SDxN28QKBgAiusHqUycYQlXAs7HDjwqdfm/TiMVWPQ8Mx9rvKHikASlUAkY9R\nX8FRgeKYETl7xiU7N1DV2z2ApFKhrI5g2q1NQSAB3FNwGOym4u7cfoidMCkSiZDh\n9amNVSM1t+xmU8dQG7bUJmz4N0TRB4wEepC+UIElsqWArzYxHTfL3I/RAoGAaYWB\n8/EzelUv/mEWmwIqdEcJc3h27SmoenitGxmk3tmtI6GkkqRtPx5Z2cOyPTZh7BEY\nIfQ2r4b4J9h7fWcv3fKrKqbdtnO1u5kgo3yRIJFElKsWHLxcfIGoVScl17eNDnGX\nsEUZgzJVRj0JGDUFMM/aRZK4dMx9KVs/rAUTwiECgYB1Ni94BJeb+VGZ9Z3Jy88v\nY5v5ezJGGcUScJ+B4/Z3ksgxR5NRalB1Io/as7N571eD2ED3N9Im8OPt6oT+L0Gu\nVhUeQZkvUcMViX++unWsYbQHiAsYRJ1TKMKrHjXv4LPBJbz8qe0XduSXKQ3tvAIK\nMkYrM8YkQ50EeLwNhkeOQQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "bp-768@bierpongturnier.iam.gserviceaccount.com",
  "client_id": "113399811597840719972",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bp-768%40bierpongturnier.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Definiere den Umfang der Berechtigungen für den Service Account
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Lese die Anmeldedaten aus dem Dictionary
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

# Authentifiziere und erhalte Zugriff auf Google Sheets
client = gspread.authorize(creds)

# Lade das Google Sheet
sheet = client.open("results_bierpong").results

def load_results():
    try:
        response = requests.get(RESULTS_URL)
        return response.json()  # Lade die JSON-Datei von GitHub
    except:
        return {}  # Rückfall, wenn keine Datei vorhanden ist

def save_results(results):
    with open('results.json', 'w') as file:
        json.dump(results, file)  # Speichere sie lokal auf Streamlit
    # Optional: Pushen der Datei zu GitHub

# Datei für gespeicherte Daten
RESULTS_URL = "https://raw.githubusercontent.com/Me37127/bierpong/main/results.json"
results_file = "results.json"  # Lokale Datei für die gespeicherten Ergebnisse

# Teams und Gruppen definieren - landet am Ende in der Tabelle
teams_group_a = ["Team 1", "Team 2", "Team 3", "Team 4"]
teams_group_b = ["Team 5", "Team 6", "Team 7", "Team 8"]

# Spielplan erstellen
spielplan = {
    "Group A": [
        {"Team 1": "Team 2", "Team 3": "Team 4"},
        {"Team 1": "Team 3", "Team 2": "Team 4"}
    ],
    "Group B": [
        {"Team 5": "Team 6", "Team 7": "Team 8"},
        {"Team 5": "Team 7", "Team 6": "Team 8"}
    ]
}

# Ergebnisse und Tabellen initialisieren
if "tables" not in st.session_state:
    # Falls keine Daten vorhanden sind, initialisiere Tabellen mit Siegen, Niederlagen und Becherdifferenz
    st.session_state.tables = {
        "Group A": {team: {"Siege": 0, "Niederlagen": 0, "Becherdifferenz": 0} for team in teams_group_a},
        "Group B": {team: {"Siege": 0, "Niederlagen": 0, "Becherdifferenz": 0} for team in teams_group_b}
    }

# Lade gespeicherte Ergebnisse aus der JSON-Datei, falls vorhanden
if Path(results_file).exists():
    st.session_state.tables = load_results()

# Titel der App
st.set_page_config(page_title="Bierpong Turnier", layout="centered")
st.title("🍻 Bierpong Turnier")

# **Abschnitt: Spielplan**
st.header("📅 Spielplan")
for group, matches in spielplan.items():
    st.subheader(group)
    for match in matches:
        for team1, team2 in match.items():
            st.write(f"- **{team1}** vs. **{team2}**")

# **Abschnitt: Ergebnisse eintragen**
st.header("✍️ Ergebnisse eintragen")
selected_group = st.selectbox("Gruppe auswählen", list(spielplan.keys()))
selected_match = st.selectbox(
    "Spiel auswählen",
    [(team1, team2) for match in spielplan[selected_group] for team1, team2 in match.items()],
    format_func=lambda match: f"{match[0]} vs. {match[1]}"
)
team1, team2 = selected_match

# SelectBox, um den Gewinner auszuwählen
winner = st.selectbox("Wähle den Gewinner", [team1, team2])

# Zahleneingabe für die Becher des Gewinner-Teams
becher_übrig = st.number_input(f"Wie viele Becher sind beim Verlierer-Team übrig?", min_value=1, max_value=10, value=1)

# Berechnung der Becher und Punkte
if winner == team1:
    score_team1 = becher_übrig
    score_team2 = -becher_übrig
else:
    score_team1 = becher_übrig
    score_team2 = -becher_übrig

submit_result = st.button("Ergebnis speichern")

# **Ergebnis speichern**
if submit_result:
    if score_team1 != score_team2:
        # Speichern der Spielstatistik
        result = {
            "Team 1": team1, "Score 1": score_team1,
            "Team 2": team2, "Score 2": score_team2
        }

        # Aktualisiere die Tabelle für die Gruppen
        group_table = st.session_state.tables[selected_group]

        if score_team1 > score_team2:
            group_table[team1]["Siege"] += 1
            group_table[team2]["Niederlagen"] += 1
            group_table[team1]["Becherdifferenz"] += score_team1
            group_table[team2]["Becherdifferenz"] += score_team2
        else:
            group_table[team2]["Siege"] += 1
            group_table[team1]["Niederlagen"] += 1
            group_table[team2]["Becherdifferenz"] += score_team2
            group_table[team1]["Becherdifferenz"] += score_team1

        # Ergebnisse speichern
        save_results(st.session_state.tables)

        st.success(f"Ergebnis für {team1} vs. {team2} gespeichert!")
    else:
        st.error("Es darf kein Unentschieden geben!")

# **Abschnitt: Gruppentabellen**
st.header("📊 Gruppentabellen")
for group, table in st.session_state.tables.items():
    st.subheader(group)
    sorted_table = pd.DataFrame(table).T
    st.table(sorted_table)

