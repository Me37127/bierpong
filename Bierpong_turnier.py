import json
import pandas as pd
import streamlit as st
from pathlib import Path

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
results_file = "https://github.com/Me37127/bierpong/blob/main/results.json"

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
    st.session_state.tables = load_results(results_file)

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
        save_results(st.session_state.tables, results_file)

        st.success(f"Ergebnis für {team1} vs. {team2} gespeichert!")
    else:
        st.error("Es darf kein Unentschieden geben!")

# **Abschnitt: Gruppentabellen**

st.header("📊 Gruppentabellen")
for group, table in st.session_state.tables.items():
    st.subheader(group)
    sorted_table = pd.DataFrame(table).T#.sort_values(by=["Siege", "Becherdifferenz"], ascending=False)
    st.table(sorted_table)


