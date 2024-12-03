#Vollständige Maturaarbeit ohne Visualisierung

# Bibliotheken: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame as pg  # Bibliothek für grafische Benutzeroberflächen und Animationen.
import random as rnd  # Bibliothek für zufällige Zahlen und Operationen.
import sys  # Bietet Zugriff auf System-spezifische Parameter und Funktionen.
import numpy as np  # Leistungsstarke Bibliothek für numerische Berechnungen und Datenmanipulation.
import os  # Bietet Funktionen für die Arbeit mit dem Dateisystem.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Labyrinth: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sys.setrecursionlimit(3600)  # Erhöht die maximale Rekursionstiefe, um tief verschachtelte Labyrinth-Funktionen zu ermöglichen.

# Konstanten
BREITE = HÖHE = 1000  # Setzt die Breite und Höhe des Labyrinth-Fensters in Pixel.
SPALTEN = ZEILEN = 60  # Definiert die Anzahl der Spalten und Zeilen im Labyrinth.
ZELLE_BREITE_HÖHE = BREITE // SPALTEN  # Berechnet die Breite und Höhe einer einzelnen Zelle.

# Bewegungsdelta und Nachbarinformationen
delta_linien = {  # Definiert die Koordinaten für die Linienbewegungen (z. B. linke oder rechte Kante einer Zelle).
    "l": [(0, 0), (0, ZELLE_BREITE_HÖHE)],  # Linie für die linke Wand.
    "r": [(ZELLE_BREITE_HÖHE, 0), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)],  # Linie für die rechte Wand.
    "o": [(0, 0), (ZELLE_BREITE_HÖHE, 0)],  # Linie für die obere Wand.
    "u": [(0, ZELLE_BREITE_HÖHE), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)]  # Linie für die untere Wand.
}
delta_nachbarn = {  # Bewegungsdeltas zur Berechnung der Nachbarpositionen basierend auf der Richtung.
    "l": (-ZELLE_BREITE_HÖHE, 0),  # Nachbar links.
    "r": (ZELLE_BREITE_HÖHE, 0),  # Nachbar rechts.
    "o": (0, -ZELLE_BREITE_HÖHE),  # Nachbar oben.
    "u": (0, ZELLE_BREITE_HÖHE)  # Nachbar unten.
}
richtung_invers = {"l": "r", "r": "l", "o": "u", "u": "o"}  # Invertiert eine Bewegungsrichtung.
richtung_rechts = {"l": "o", "o": "r", "r": "u", "u": "l"}  # Berechnet die Richtung rechts von der aktuellen Richtung.
richtung_links = {"l": "u", "u": "r", "r": "o", "o": "l"}  # Berechnet die Richtung links von der aktuellen Richtung.

# Pygame initialisieren
pg.init()  # Initialisiert alle benötigten Pygame-Module.
screen = pg.display.set_mode([BREITE, HÖHE])  # Erstellt ein Fenster für die Labyrinth-Darstellung.
farbe_hintergrund = pg.Color("Black")  # Setzt die Hintergrundfarbe des Fensters auf Schwarz.

# Hilfsfunktionen
def add_pos(pos1, pos2):
    # Addiert zwei Positionen (Tupel) und gibt die neue Position zurück.
    return pos1[0] + pos2[0], pos1[1] + pos2[1]

def pg_quit():
    # Überprüft, ob ein Quit-Event (Fenster schließen oder Escape-Taste) ausgelöst wurde.
    for ereignis in pg.event.get():  # Iteriert durch alle Pygame-Ereignisse.
        if ereignis.type == pg.QUIT or (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
            return True

def nachbarn_ermitteln(pos):
    # Bestimmt alle Nachbarn einer gegebenen Position.
    # Mischt die Reihenfolge der Nachbarn, um zufällige Bewegungen zu erzeugen.
    nachbarn = []
    for richtung, delta in delta_nachbarn.items():
        neue_pos = add_pos(pos, delta)  # Berechnet die Nachbarposition basierend auf der Delta-Werte.
        if neue_pos not in raster:  # Prüft, ob die Nachbarposition im Labyrinth definiert ist.
            continue
        nachbarn.append((richtung, neue_pos))  # Fügt die Richtung und die Position der Nachbarn zur Liste hinzu.
    rnd.shuffle(nachbarn)  # Mischt die Nachbarnliste, um zufällige Bewegungen zu erzeugen.
    return nachbarn

def mögliche_richtungen(pos):
    # Bestimmt alle möglichen Richtungen, in die sich von einer Position aus bewegt werden kann.
    richtungen = []
    for richtung, delta in delta_nachbarn.items():
        neue_pos = add_pos(pos, delta)  # Berechnet die neue Position für jede mögliche Richtung.
        if neue_pos not in raster:  # Prüft, ob die neue Position im Labyrinth definiert ist.
            continue
        if richtung in raster[pos]:  # Überprüft, ob die Richtung in den verbleibenden Wänden der aktuellen Zelle enthalten ist.
            continue
        richtungen.append(neue_pos)  # Fügt die gültige neue Position zur Liste hinzu.
    return richtungen

def labyrinth_erstellen(pos_aktuell, richtung_von):
    # Erstellt ein Labyrinth rekursiv mit Hilfe einer Tiefensuche.
    besucht.add(pos_aktuell)  # Markiert die aktuelle Position als besucht.
    if richtung_von is not None:
        raster[pos_aktuell].remove(richtung_von)  # Entfernt die Wand in der Richtung, aus der die Zelle betreten wurde.
    nachbarn = nachbarn_ermitteln(pos_aktuell)  # Bestimmt die Nachbarn der aktuellen Position.
    for richtung_nach, pos_neu in nachbarn:
        if pos_neu in besucht:  # Überspringt bereits besuchte Nachbarn.
            continue
        raster[pos_aktuell].remove(richtung_nach)  # Entfernt die Wand in Richtung des Nachbarn.
        labyrinth_erstellen(pos_neu, richtung_invers[richtung_nach])  # Rekursive Erstellung des Labyrinths.

# Ziel und Pfadberechnung
ziel = ((SPALTEN - 1) * ZELLE_BREITE_HÖHE, (ZEILEN - 1) * ZELLE_BREITE_HÖHE)  # Definiert die Zielposition des Labyrinths.
weg = []  # Speichert den kürzesten Pfad zum Ziel.
länge_kürzester_weg = 0  # Speichert die Länge des kürzesten Pfades.

def labyrinth_lösen(pos_aktuell):
    # Löst das Labyrinth rekursiv und bestimmt den kürzesten Weg zum Ziel.
    global länge_kürzester_weg
    besucht.append(pos_aktuell)  # Fügt die aktuelle Position zur Liste der besuchten Positionen hinzu.
    if pos_aktuell == ziel:  # Überprüft, ob das Ziel erreicht wurde.
        weg.append(pos_aktuell)  # Fügt die Zielposition zum Weg hinzu.
        länge_kürzester_weg += 1  # Erhöht die Länge des kürzesten Weges.
        return True
    for pos_neu in mögliche_richtungen(pos_aktuell):  # Iteriert durch alle möglichen Bewegungen.
        if pos_neu in besucht:  # Überspringt bereits besuchte Positionen.
            continue
        if labyrinth_lösen(pos_neu):  # Rekursive Suche nach dem Ziel.
            weg.append(pos_neu)  # Fügt die Position zum Weg hinzu, falls das Ziel erreicht wurde.
            länge_kürzester_weg += 1  # Erhöht die Länge des kürzesten Weges.
            return True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Speicherung der Ergebnisse: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~          
def speichere_resultate(durchlauf, episode, felder, bewegungen, kürzester_weg, bewegungen_links, felder_links, bewegungen_rechts, felder_rechts):
    # Speichert die Ergebnisse der aktuellen Episode und des Durchlaufs in einer Textdatei.
    dateiname = "episoden_resultate.txt"
    
    # Überprüft, ob die Datei existiert, und fügt den Header hinzu, falls nicht vorhanden.
    if not os.path.exists(dateiname):
        with open(dateiname, "w") as file:
            file.write(f"Länge des kürzesten Wegs: {kürzester_weg} Felder\n\n")
    
    # Öffnet die Datei im Anhängmodus, um die Ergebnisse der aktuellen Episode hinzuzufügen.
    with open(dateiname, "a") as file:
        file.write(f"Durchlauf {durchlauf}, Episode {episode}:\n")
        file.write(f"Länge des kürzesten Wegs: {kürzester_weg}\n")
        file.write(f"Links: Anzahl der Bewegungen: {bewegungen_links}, Unterschiedliche besuchte Felder: {felder_links}\n")
        file.write(f"Rechts: Anzahl der Bewegungen: {bewegungen_rechts}, Unterschiedliche besuchte Felder: {felder_rechts}\n")
        file.write(f"Die KI hat das Ziel erreicht und {felder} verschiedene Felder besucht.\n")
        file.write(f"Die KI hat insgesamt {bewegungen} Bewegungen gemacht.\n\n")

def leere_episoden_datei(dateiname):
    # Löscht oder leert die Datei vor Beginn des Trainings, falls sie existiert.
    if os.path.exists(dateiname):
        with open(dateiname, "w") as file:
            pass  # Überschreibt den Inhalt der Datei mit nichts (macht die Datei leer).

def ordner_erstellen_und_leeren(ordner_name):
    # Erstellt einen Ordner, falls dieser nicht existiert, und leert ihn, falls er bereits existiert.
    if os.path.exists(ordner_name):
        # Löscht alle Dateien und Unterordner im angegebenen Ordner.
        for datei in os.listdir(ordner_name):
            dateipfad = os.path.join(ordner_name, datei)
            if os.path.isfile(dateipfad):  # Überprüft, ob der Pfad zu einer Datei führt.
                os.remove(dateipfad)  # Löscht die Datei.
            else:
                os.rmdir(dateipfad)  # Löscht den Ordner (falls vorhanden).
    else:
        os.makedirs(ordner_name)  # Erstellt den Ordner, falls er noch nicht existiert.

def speichere_heatmap(ordner_name, durchlauf, episode, heatmap):
    # Speichert die aktuelle Heatmap der Episode in einer .npy-Datei.
    heatmap_dateiname = f"heatmap_durchlauf_{durchlauf + 1}_episode_{episode + 1}.npy"  # Erstellt den Dateinamen für die Heatmap.
    heatmap_pfad = os.path.join(ordner_name, heatmap_dateiname)  # Verbindet den Ordnerpfad mit dem Dateinamen.
    np.save(heatmap_pfad, heatmap)  # Speichert die Heatmap-Daten im .npy-Format.
    print(f"Heatmap für Durchlauf {durchlauf + 1}, Episode {episode + 1} gespeichert: {heatmap_pfad}")

# Heatmap-Variable zur Zählung der Besuche pro Zelle
heatmap = np.zeros((SPALTEN, ZEILEN), dtype=int)  # Erstellt eine 2D-Array-Heatmap mit allen Werten auf 0.

# Ordner für Heatmaps erstellen und zurücksetzen
heatmap_ordner = "heatmaps"  # Definiert den Ordnernamen für die Speicherung der Heatmaps.
ordner_erstellen_und_leeren(heatmap_ordner)  # Leert den Ordner zu Beginn oder erstellt ihn neu.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 
# Menschliche Vergleichsweisen: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def figur_bewegt_sich_rechts(pos_aktuell, richtung):
    # Berechnet die nächste Position und Richtung für eine Figur, die der rechten Wand folgt.
    rechts_richtung = richtung_rechts[richtung]  # Bestimmt die Richtung rechts der aktuellen Richtung.
    rechts_pos = add_pos(pos_aktuell, delta_nachbarn[rechts_richtung])  # Berechnet die Position nach rechts.
    if rechts_richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand rechts nicht existiert.
        return rechts_pos, rechts_richtung  # Bewegt sich nach rechts, wenn möglich.
    
    geradeaus_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])  # Berechnet die Position geradeaus.
    if richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand geradeaus nicht existiert.
        return geradeaus_pos, richtung  # Bewegt sich geradeaus, wenn möglich.
    
    links_richtung = richtung_links[richtung]  # Bestimmt die Richtung links der aktuellen Richtung.
    links_pos = add_pos(pos_aktuell, delta_nachbarn[links_richtung])  # Berechnet die Position nach links.
    if links_richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand links nicht existiert.
        return links_pos, links_richtung  # Bewegt sich nach links, wenn möglich.
    
    zurück_pos = add_pos(pos_aktuell, delta_nachbarn[richtung_invers[richtung]])  # Berechnet die Position rückwärts.
    return zurück_pos, richtung_invers[richtung]  # Bewegt sich rückwärts, wenn keine andere Richtung möglich ist.

def figur_bewegt_sich_links(pos_aktuell, richtung):
    # Berechnet die nächste Position und Richtung für eine Figur, die der linken Wand folgt.
    links_richtung = richtung_links[richtung]  # Bestimmt die Richtung links der aktuellen Richtung.
    links_pos = add_pos(pos_aktuell, delta_nachbarn[links_richtung])  # Berechnet die Position nach links.
    if links_richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand links nicht existiert.
        return links_pos, links_richtung  # Bewegt sich nach links, wenn möglich.
    
    geradeaus_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])  # Berechnet die Position geradeaus.
    if richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand geradeaus nicht existiert.
        return geradeaus_pos, richtung  # Bewegt sich geradeaus, wenn möglich.
    
    rechts_richtung = richtung_rechts[richtung]  # Bestimmt die Richtung rechts der aktuellen Richtung.
    rechts_pos = add_pos(pos_aktuell, delta_nachbarn[rechts_richtung])  # Berechnet die Position nach rechts.
    if rechts_richtung not in raster.get(pos_aktuell, set()):  # Prüft, ob die Wand rechts nicht existiert.
        return rechts_pos, rechts_richtung  # Bewegt sich nach rechts, wenn möglich.
    
    zurück_pos = add_pos(pos_aktuell, delta_nachbarn[richtung_invers[richtung]])  # Berechnet die Position rückwärts.
    return zurück_pos, richtung_invers[richtung]  # Bewegt sich rückwärts, wenn keine andere Richtung möglich ist.

def figur_immer_rechts():
    # Bewegt die Figur durch das Labyrinth, indem sie immer der rechten Wand folgt.
    pos_figur = (0, 0)  # Startposition der Figur.
    richtung = "r"  # Startet in Richtung "rechts".
    anzahl_besuchte_felder_rechts = set()  # Set, um die besuchten Felder zu speichern.
    anzahl_bewegungen_rechts = 0  # Zählt die Anzahl der Bewegungen.

    while not pg_quit():  # Schleife läuft, bis ein Quit-Event ausgelöst wird.
        if pos_figur not in anzahl_besuchte_felder_rechts:
            anzahl_besuchte_felder_rechts.add(pos_figur)  # Markiert das aktuelle Feld als besucht.
        pos_figur, richtung = figur_bewegt_sich_rechts(pos_figur, richtung)  # Bewegt die Figur nach rechts.
        anzahl_bewegungen_rechts += 1  # Erhöht die Bewegungsanzahl.
        pg.display.flip()  # Aktualisiert die Anzeige.
        if pos_figur == ziel:  # Beendet die Schleife, wenn die Zielposition erreicht ist.
            break

    print(f"Rechts: Anzahl der Bewegungen: {anzahl_bewegungen_rechts}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_rechts)}")
    return anzahl_bewegungen_rechts, len(anzahl_besuchte_felder_rechts)

def figur_immer_links():
    # Bewegt die Figur durch das Labyrinth, indem sie immer der linken Wand folgt.
    pos_figur = (0, 0)  # Startposition der Figur.
    richtung = "r"  # Startet in Richtung "rechts".
    anzahl_besuchte_felder_links = set()  # Set, um die besuchten Felder zu speichern.
    anzahl_bewegungen_links = 0  # Zählt die Anzahl der Bewegungen.

    while not pg_quit():  # Schleife läuft, bis ein Quit-Event ausgelöst wird.
        if pos_figur not in anzahl_besuchte_felder_links:
            anzahl_besuchte_felder_links.add(pos_figur)  # Markiert das aktuelle Feld als besucht.
        pos_figur, richtung = figur_bewegt_sich_links(pos_figur, richtung)  # Bewegt die Figur nach links.
        anzahl_bewegungen_links += 1  # Erhöht die Bewegungsanzahl.
        pg.display.flip()  # Aktualisiert die Anzeige.
        if pos_figur == ziel:  # Beendet die Schleife, wenn die Zielposition erreicht ist.
            break

    print(f"Links: Anzahl der Bewegungen: {anzahl_bewegungen_links}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_links)}")
    return anzahl_bewegungen_links, len(anzahl_besuchte_felder_links)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Künstliche Intelligenz: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Q-Learning Variablen
q_table = np.zeros((SPALTEN, ZEILEN, 4))  # Erstellt eine Q-Tabelle mit einer Dimension für jede Zelle und vier möglichen Aktionen (l, r, o, u).
action_map = {"l": 0, "r": 1, "o": 2, "u": 3}  # Mapped Bewegungsrichtungen auf Aktionen.
learning_rate = 0.2  # Lernrate (Alpha), die bestimmt, wie stark neue Informationen alte überschreiben.
discount_factor = 0.99  # Diskontierungsfaktor (Gamma), um zukünftige Belohnungen zu gewichten.
epsilon = 1  # Startwert für die Epsilon-Greedy-Strategie.
epsilon_decay = 0.999  # Faktor, um den Epsilon-Wert nach jeder Episode zu verringern.
episodes = 50  # Anzahl der Episoden pro Durchlauf.
durchlaeufe = 100  # Anzahl der Durchläufe (Trainingsiterationen).

# Variablen für die KI
pos_ki = (0, 0)  # Startposition der KI.
unterschiedliche_besuchte_felder_ki = []  # Liste der von der KI besuchten einzigartigen Felder.
anzahl_besuchte_felder_ki = 1  # Zählt die Anzahl der besuchten Felder.
anzahl_bewegungen_ki = 0  # Zählt die Bewegungen der KI.
gesamte_episoden = 0  # Gesamtzahl der durchgeführten Episoden.

def ki_bewege_sich(pos_aktuell):
    # Führt eine Bewegung der KI durch, basierend auf der Epsilon-Greedy-Strategie und der Q-Tabelle.
    global anzahl_bewegungen_ki
    anzahl_bewegungen_ki += 1  # Erhöht die Bewegunganzahl.

    # Entscheidung treffen: Exploration oder Exploitation
    if rnd.uniform(0, 1) < epsilon:  # Zufällige Bewegung (Exploration).
        action = rnd.choice(range(4))  # Wählt zufällig eine der vier Aktionen.
    else:  # Bewegung basierend auf Q-Tabelle (Exploitation).
        action = np.argmax(q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE])

    richtung = list(action_map.keys())[action]  # Wandelt die Aktion in eine Bewegungsrichtung um.
    neue_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])  # Berechnet die neue Position basierend auf der Richtung.

    # Bewegung validieren
    if neue_pos in raster and richtung not in raster[pos_aktuell]: 
        # Wenn die Bewegung gültig ist:
        if neue_pos not in unterschiedliche_besuchte_felder_ki:  # Prüft, ob das Feld neu ist.
            unterschiedliche_besuchte_felder_ki.append(neue_pos)
            reward = +5  # Belohnung für das Besuchen eines neuen Feldes.
        else:
            reward = -1  # Strafe für das Wiederbesuchen eines Feldes.
    else:
        neue_pos = pos_aktuell  # Bleibt an der aktuellen Position, wenn die Bewegung ungültig ist.
        reward = -1  # Strafe für ungültige Bewegung.

    if neue_pos == ziel:  # Wenn die Zielposition erreicht wurde:
        reward = 1000  # Große Belohnung für das Erreichen des Ziels.

    # Q-Wert aktualisieren
    old_value = q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE, action]
    future_reward = np.max(q_table[neue_pos[0] // ZELLE_BREITE_HÖHE, neue_pos[1] // ZELLE_BREITE_HÖHE])
    q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE, action] = old_value + learning_rate * (reward + discount_factor * future_reward - old_value)

    # Heatmap aktualisieren
    heatmap[neue_pos[0] // ZELLE_BREITE_HÖHE, neue_pos[1] // ZELLE_BREITE_HÖHE] += 1  # Erhöht die Besuchszahl für das Feld.

    return neue_pos  # Gibt die neue Position zurück.

# Training der KI

# Name der Datei für Episodenresultate
episoden_datei_name = "episoden_resultate.txt"

# Datei leeren
leere_episoden_datei(episoden_datei_name)

for durchlauf in range(durchlaeufe):  # Schleife über alle Trainingsdurchläufe.
    global raster, besucht  # Macht raster und besucht global zugänglich.
    raster = {}  # Leert das Raster vor jedem neuen Durchlauf.
    for i in range(SPALTEN * ZEILEN):  # Initialisiert das Raster mit allen Zellen und Wänden.
        pos = (i % SPALTEN * ZELLE_BREITE_HÖHE, i // SPALTEN * ZELLE_BREITE_HÖHE)
        raster[pos] = {"l", "r", "o", "u"}  # Fügt alle Wände zu jeder Zelle hinzu.

    weg.clear()  # Löscht den Weg des kürzesten Pfades.
    länge_kürzester_weg = 0  # Setzt die Länge des kürzesten Pfades zurück.

    besucht = set()  # Set der besuchten Felder leeren.
    labyrinth_erstellen((0, 0), "l")  # Generiert das Labyrinth.
    besucht = []  # Zurücksetzen der besuchten Felder für die Lösung.
    labyrinth_lösen((0, 0))  # Bestimmt den kürzesten Weg.
    print(f"Länge des kürzesten Wegs: {länge_kürzester_weg} Felder")

    for episode in range(episodes):  # Schleife über alle Episoden.
        # Ergebnisse der Bewegungsmethoden erfassen
        bewegungen_links, felder_links = figur_immer_links()
        bewegungen_rechts, felder_rechts = figur_immer_rechts()

        # KI bewegt sich durch das Labyrinth
        pos_ki = (0, 0)  # Startposition der KI.
        unterschiedliche_besuchte_felder_ki.clear()  # Zurücksetzen der Liste besuchter Felder.
        anzahl_bewegungen_ki = 0  # Zurücksetzen der Bewegungsanzahl.
        besucht = set()  # Zurücksetzen der besuchten Felder.
        besucht.add(pos_ki)  # Markiert die Startposition als besucht.

        heatmap.fill(0)  # Setzt die Heatmap für die neue Episode zurück.

        while True:  # KI-Schleife bis das Ziel erreicht ist.
            neue_pos = ki_bewege_sich(pos_ki)  # Führt eine Bewegung der KI aus.

            if neue_pos == ziel:  # Wenn das Ziel erreicht wurde:
                print(f"Durchgang {durchlauf + 1}; Episode {episode + 1}: Die KI hat das Ziel erreicht und {len(unterschiedliche_besuchte_felder_ki)} verschiedene Felder besucht.")
                print(f"Die KI hat insgesamt {anzahl_bewegungen_ki} Bewegungen gemacht.")
                print(f"Epsilon beträgt aktuell {epsilon}")

                # Heatmap speichern
                speichere_heatmap(heatmap_ordner, durchlauf, episode, heatmap)
                break

            pos_ki = neue_pos  # Aktualisiert die Position der KI.

        # Ergebnisse speichern
        speichere_resultate(
            durchlauf + 1, 
            episode + 1,
            len(unterschiedliche_besuchte_felder_ki), 
            anzahl_bewegungen_ki, 
            länge_kürzester_weg,
            bewegungen_links,
            felder_links,
            bewegungen_rechts,
            felder_rechts
        )

        # Epsilon-Wert anpassen
        epsilon = epsilon * epsilon_decay  # Verringert den Epsilon-Wert für zukünftige Episoden.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pg.quit()