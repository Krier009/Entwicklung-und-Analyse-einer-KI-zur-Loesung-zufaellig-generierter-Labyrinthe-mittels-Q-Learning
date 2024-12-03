#Visualisierung der Maturaarbeit
#Bei der Visualisierung der KI das Pygame Fenster geöffnet lasssen!

# Bibliotheken: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame as pg  # Bibliothek für grafische Benutzeroberflächen und Animationen.
import random as rnd  # Bibliothek für zufällige Zahlen und Operationen.
import sys  # Bietet Zugriff auf System-spezifische Parameter und Funktionen.
import numpy as np  # Leistungsstarke Bibliothek für numerische Berechnungen und Datenmanipulation.
import os  # Bietet Funktionen für die Arbeit mit dem Dateisystem.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Labyrinth: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sys.setrecursionlimit(3600)  # Erhöht die maximale Rekursionstiefe, um tief verschachtelte Funktionen, wie die Labyrinth-Erstellung, zu ermöglichen.

# Konstanten
BREITE = HÖHE = 1000  # Setzt die Breite und Höhe des Labyrinth-Fensters in Pixel.
SPALTEN = ZEILEN = 60  # Definiert die Anzahl der Spalten und Zeilen im Labyrinth.
ZELLE_BREITE_HÖHE = BREITE // SPALTEN  # Berechnet die Breite und Höhe einer einzelnen Zelle in Pixeln.

# Bewegungsdelta und Nachbarinformationen
delta_linien = {  # Definiert die Koordinaten für die Linienbewegungen, um Wände innerhalb einer Zelle zu zeichnen.
    "l": [(0, 0), (0, ZELLE_BREITE_HÖHE)],  # Start- und Endpunkte für die linke Wand.
    "r": [(ZELLE_BREITE_HÖHE, 0), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)],  # Start- und Endpunkte für die rechte Wand.
    "o": [(0, 0), (ZELLE_BREITE_HÖHE, 0)],  # Start- und Endpunkte für die obere Wand.
    "u": [(0, ZELLE_BREITE_HÖHE), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)]  # Start- und Endpunkte für die untere Wand.
}
delta_nachbarn = {  # Bewegungsdeltas zur Berechnung der Nachbarpositionen basierend auf der Richtung.
    "l": (-ZELLE_BREITE_HÖHE, 0),  # Verschiebung zur Nachbarzelle links.
    "r": (ZELLE_BREITE_HÖHE, 0),  # Verschiebung zur Nachbarzelle rechts.
    "o": (0, -ZELLE_BREITE_HÖHE),  # Verschiebung zur Nachbarzelle oben.
    "u": (0, ZELLE_BREITE_HÖHE)  # Verschiebung zur Nachbarzelle unten.
}
richtung_invers = {"l": "r", "r": "l", "o": "u", "u": "o"}  # Invertiert eine Bewegungsrichtung (für Rückbewegungen).
richtung_rechts = {"l": "o", "o": "r", "r": "u", "u": "l"}  # Berechnet die Richtung rechts von der aktuellen Richtung.
richtung_links = {"l": "u", "u": "r", "r": "o", "o": "l"}  # Berechnet die Richtung links von der aktuellen Richtung.

# Pygame initialisieren
pg.init()  # Initialisiert alle benötigten Module von Pygame.
screen = pg.display.set_mode([BREITE, HÖHE])  # Erstellt ein Fenster für die grafische Darstellung des Labyrinths.
farbe_hintergrund = pg.Color("Black")  # Setzt die Hintergrundfarbe des Fensters auf Schwarz.
farbe_linien = pg.Color("White")  # Farbe für die Wände des Labyrinths.
farbe_weg = pg.Color("gold2")  # Farbe für den kürzesten Weg.
farbe_figur_rechts = pg.Color("red")  # Farbe für die Figur, die der rechten Wand folgt.
farbe_figur_links = pg.Color("green")  # Farbe für die Figur, die der linken Wand folgt.
farbe_ki = pg.Color("green")  # Farbe für die KI.
farbe_besuchte = pg.Color("dodgerblue4")  # Farbe für besuchte Felder.

# Uhr initialisieren
clock = pg.time.Clock()  # Erstellt eine Clock-Instanz für die Steuerung der Frame-Rate.

# Hilfsfunktionen
def add_pos(pos1, pos2):
    # Addiert zwei Positionen (Tupel) und gibt die neue Position zurück.
    return pos1[0] + pos2[0], pos1[1] + pos2[1]

def pg_quit():
    # Überprüft, ob ein Quit-Event (Fenster schließen oder ESC-Taste) ausgelöst wurde.
    for ereignis in pg.event.get():  # Iteriert durch alle Ereignisse in der Ereigniswarteschlange.
        if ereignis.type == pg.QUIT or (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
            return True

def nachbarn_ermitteln(pos):
    # Bestimmt alle Nachbarn einer gegebenen Position.
    # Mischt die Reihenfolge der Nachbarn, um zufällige Bewegungen zu ermöglichen.
    nachbarn = []
    for richtung, delta in delta_nachbarn.items():  # Iteriert durch alle möglichen Bewegungsrichtungen.
        neue_pos = add_pos(pos, delta)  # Berechnet die Nachbarposition basierend auf dem Delta-Wert.
        if neue_pos not in raster:  # Prüft, ob die Nachbarposition innerhalb des Labyrinth-Rasters liegt.
            continue
        nachbarn.append((richtung, neue_pos))  # Fügt die Richtung und die Position zur Nachbarnliste hinzu.
    rnd.shuffle(nachbarn)  # Mischt die Nachbarnliste, um zufällige Bewegungen zu erzeugen.
    return nachbarn

def mögliche_richtungen(pos):
    # Bestimmt alle möglichen Richtungen, in die sich von einer Position aus bewegt werden kann.
    richtungen = []
    for richtung, delta in delta_nachbarn.items():  # Iteriert durch alle möglichen Bewegungsrichtungen.
        neue_pos = add_pos(pos, delta)  # Berechnet die neue Position.
        if neue_pos not in raster:  # Überspringt Positionen, die außerhalb des Labyrinths liegen.
            continue
        if richtung in raster[pos]:  # Überspringt Positionen, deren Richtung durch eine Wand blockiert ist.
            continue
        richtungen.append(neue_pos)  # Fügt die gültige neue Position zur Liste hinzu.
    return richtungen

def zeichne_zelle(pos, wände):
    # Zeichnet die Wände einer Zelle basierend auf deren Position und den vorhandenen Wänden.
    for wand in wände:  # Iteriert durch alle vorhandenen Wände der Zelle.
        delta_von, delta_bis = delta_linien[wand]  # Bestimmt die Start- und Endpunkte der Wand.
        von = add_pos(pos, delta_von)  # Berechnet die Startposition der Linie.
        bis = add_pos(pos, delta_bis)  # Berechnet die Endposition der Linie.
        pg.draw.line(screen, farbe_linien, von, bis, 2)  # Zeichnet die Linie auf dem Bildschirm.

def labyrinth_unbekannt_machen():
    # Setzt das Labyrinth zurück, indem der Bildschirm mit der Hintergrundfarbe gefüllt wird.
    screen.fill(farbe_hintergrund)

def aktualisiere_feld(pos, farbe):
    # Aktualisiert die Anzeige für ein bestimmtes Feld, indem es mit der angegebenen Farbe gefüllt wird.
    pg.draw.rect(screen, farbe, (pos, (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)))  # Zeichnet ein gefülltes Rechteck.
    zeichne_zelle(pos, raster[pos])  # Zeichnet die Wände der Zelle erneut.

def in_bounds(pos):
    # Überprüft, ob eine gegebene Position innerhalb der Grenzen des Labyrinths liegt.
    x, y = pos
    return 0 <= x < SPALTEN * ZELLE_BREITE_HÖHE and 0 <= y < ZEILEN * ZELLE_BREITE_HÖHE

def labyrinth_erstellen(pos_aktuell, richtung_von):
    # Erstellt ein Labyrinth rekursiv mit Hilfe einer Tiefensuche.
    besucht.add(pos_aktuell)  # Markiert die aktuelle Position als besucht.
    if richtung_von is not None:  # Wenn die Zelle aus einer bestimmten Richtung betreten wurde:
        raster[pos_aktuell].remove(richtung_von)  # Entfernt die Wand in dieser Richtung.
    nachbarn = nachbarn_ermitteln(pos_aktuell)  # Bestimmt die Nachbarn der aktuellen Position.
    for richtung_nach, pos_neu in nachbarn:  # Iteriert durch alle Nachbarn.
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


# Visualisierung des kürzesten Weges: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
def visualisiere_weg():
    # Visualisiert den kürzesten Weg durch das Labyrinth.
    i = 0  # Startindex für den Weg.
    while i < len(weg) and not pg_quit():  # Schleife, die den gesamten Weg durchläuft, solange das Programm nicht beendet wird.
        clock.tick(150)  # Begrenzt die Frame-Rate auf 150 Frames pro Sekunde.
        
        # Koordinaten des aktuellen Wegpunktes berechnen.
        x, y = weg[i]
        x, y = x + ZELLE_BREITE_HÖHE // 2, y + ZELLE_BREITE_HÖHE // 2  # Verschiebt die Koordinaten zum Mittelpunkt der Zelle.
        
        # Zeichnet einen Kreis für den aktuellen Wegpunkt.
        pg.draw.circle(screen, farbe_weg, (x, y), ZELLE_BREITE_HÖHE // 6)
        
        # Zeichnet die Wände des gesamten Labyrinths erneut, um sicherzustellen, dass der Weg korrekt visualisiert wird.
        for pos, wände in raster.items():
            zeichne_zelle(pos, wände)
        
        pg.display.flip()  # Aktualisiert die Anzeige.
        i += 1  # Erhöht den Index, um den nächsten Wegpunkt zu verarbeiten.
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
        clock.tick(100)  # Begrenzt die Frame-Rate auf 100 Frames pro Sekunde.
        if pos_figur not in anzahl_besuchte_felder_rechts:
            anzahl_besuchte_felder_rechts.add(pos_figur)  # Markiert das aktuelle Feld als besucht.
            aktualisiere_feld(pos_figur, farbe_besuchte)  # Aktualisiert die Anzeige des besuchten Feldes.
        alte_pos = pos_figur
        pos_figur, richtung = figur_bewegt_sich_rechts(pos_figur, richtung)  # Bewegt die Figur nach rechts.
        anzahl_bewegungen_rechts += 1  # Erhöht die Bewegungsanzahl.
        if in_bounds(pos_figur):  # Überprüft, ob die neue Position innerhalb der Labyrinth-Grenzen liegt.
            aktualisiere_feld(pos_figur, farbe_figur_rechts)  # Aktualisiert die Anzeige für die Figur.
        if alte_pos != pos_figur and in_bounds(alte_pos):  # Überprüft, ob die alte Position innerhalb der Grenzen liegt.
            aktualisiere_feld(alte_pos, farbe_besuchte)  # Markiert die alte Position als besucht.
        pg.display.flip()  # Aktualisiert die Anzeige.
        if pos_figur == ziel:  # Beendet die Schleife, wenn die Zielposition erreicht ist.
            break

    print(f"Rechts: Anzahl der Bewegungen: {anzahl_bewegungen_rechts}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_rechts)}")
    visualisiere_weg()  # Visualisiert den kürzesten Weg.

def figur_immer_links():
    # Bewegt die Figur durch das Labyrinth, indem sie immer der linken Wand folgt.
    pos_figur = (0, 0)  # Startposition der Figur.
    richtung = "r"  # Startet in Richtung "rechts".
    anzahl_besuchte_felder_links = set()  # Set, um die besuchten Felder zu speichern.
    anzahl_bewegungen_links = 0  # Zählt die Anzahl der Bewegungen.

    while not pg_quit():  # Schleife läuft, bis ein Quit-Event ausgelöst wird.
        clock.tick(100)  # Begrenzt die Frame-Rate auf 100 Frames pro Sekunde.
        if pos_figur not in anzahl_besuchte_felder_links:
            anzahl_besuchte_felder_links.add(pos_figur)  # Markiert das aktuelle Feld als besucht.
            aktualisiere_feld(pos_figur, farbe_besuchte)  # Aktualisiert die Anzeige des besuchten Feldes.
        alte_pos = pos_figur
        pos_figur, richtung = figur_bewegt_sich_links(pos_figur, richtung)  # Bewegt die Figur nach links.
        anzahl_bewegungen_links += 1  # Erhöht die Bewegungsanzahl.
        if in_bounds(pos_figur):  # Überprüft, ob die neue Position innerhalb der Labyrinth-Grenzen liegt.
            aktualisiere_feld(pos_figur, farbe_figur_links)  # Aktualisiert die Anzeige für die Figur.
        if alte_pos != pos_figur and in_bounds(alte_pos):  # Überprüft, ob die alte Position innerhalb der Grenzen liegt.
            aktualisiere_feld(alte_pos, farbe_besuchte)  # Markiert die alte Position als besucht.
        pg.display.flip()  # Aktualisiert die Anzeige.
        if pos_figur == ziel:  # Beendet die Schleife, wenn die Zielposition erreicht ist.
            break

    print(f"Links: Anzahl der Bewegungen: {anzahl_bewegungen_links}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_links)}")
    visualisiere_weg()  # Visualisiert den kürzesten Weg.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Künstliche Intelligenz ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Q-Learning Variablen
q_table = np.zeros((SPALTEN, ZEILEN, 4))  # Erstellt eine Q-Tabelle mit einer Dimension für jede Zelle und vier möglichen Aktionen (l, r, o, u).
action_map = {"l": 0, "r": 1, "o": 2, "u": 3}  # Mapped Bewegungsrichtungen auf Aktionen.
learning_rate = 0.2  # Lernrate (Alpha), die bestimmt, wie stark neue Informationen alte überschreiben.
discount_factor = 0.99  # Diskontierungsfaktor (Gamma), um zukünftige Belohnungen zu gewichten.
epsilon = 1  # Startwert für die Epsilon-Greedy-Strategie.
epsilon_decay = 0.999  # Faktor, um den Epsilon-Wert nach jeder Episode zu verringern.
q_table_path = "q_table.npy"  # Pfad zur Speicherdatei der Q-Tabelle.

# Variablen für die KI
pos_ki = (0, 0)  # Startposition der KI.
unterschiedliche_besuchte_felder_ki = []  # Liste der von der KI besuchten einzigartigen Felder.
anzahl_besuchte_felder_ki = 0  # Zählt die Anzahl der besuchten Felder.
anzahl_bewegungen_ki = 0  # Zählt die Bewegungen der KI.

def lade_q_table(dateipfad):
    # Lädt eine gespeicherte Q-Tabelle aus einer Datei.
    if os.path.exists(dateipfad):
        print(f"Q-Tabelle wurde gefunden: {dateipfad}")  # Gibt aus, dass die Datei gefunden wurde.
        return np.load(dateipfad)  # Lädt die gespeicherten Daten.
    else:
        print(f"Keine gespeicherte Q-Tabelle gefunden unter: {dateipfad}")  # Gibt aus, dass die Datei fehlt.
        return np.zeros((SPALTEN, ZEILEN, 4))  # Gibt eine leere Q-Tabelle zurück, falls keine Datei existiert.

def ki_bewege_sich(pos_aktuell):
    # Führt eine Bewegung der KI durch, basierend auf der Q-Tabelle.
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
        if neue_pos not in unterschiedliche_besuchte_felder_ki:  # Prüft, ob das Feld neu ist.
            unterschiedliche_besuchte_felder_ki.append(neue_pos)
            reward = +5  # Belohnung für das Besuchen eines neuen Feldes.
            aktualisiere_feld(neue_pos, farbe_besuchte)  # Aktualisiert die Anzeige für das neue Feld.
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

    return neue_pos  # Gibt die neue Position zurück.



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Abfrage vom Benutzer: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
q_table = None  # Initialisiert die Q-Tabelle.
while True:
    antwort = input("Möchten Sie eine vorhandene Q-Tabelle laden? (ja/nein): ").strip().lower()
    if antwort == "ja":
        q_table = lade_q_table(q_table_path)  # Lädt die Q-Tabelle.
        break
    elif antwort == "nein":
        q_table = np.zeros((SPALTEN, ZEILEN, 4))  # Erstellt eine leere Q-Tabelle.
        break
    else:
        print("Ungültige Eingabe. Bitte geben Sie 'ja' oder 'nein' ein.")  # Fordert gültige Eingabe an.

# Labyrinth-Initialisierung
raster = {}  # Initialisiert ein leeres Raster für das Labyrinth.
for i in range(SPALTEN * ZEILEN):  # Iteriert durch alle Zellen des Labyrinths.
    pos = (i % SPALTEN * ZELLE_BREITE_HÖHE, i // SPALTEN * ZELLE_BREITE_HÖHE)  # Berechnet die Position der Zelle.
    raster[pos] = {"l", "r", "o", "u"}  # Fügt alle vier Wände zu jeder Zelle hinzu.

länge_kürzester_weg = 0  # Setzt die Länge des kürzesten Weges auf 0 zurück.

# Labyrinth-Erstellung und Lösung
besucht = set()  # Initialisiert ein Set für besuchte Zellen.
labyrinth_erstellen((0, 0), "l")  # Erstellt ein zufälliges Labyrinth.
besucht = []  # Setzt die Liste der besuchten Felder zurück.
labyrinth_lösen((0, 0))  # Berechnet den kürzesten Weg zum Ziel.
print(f"Länge des kürzesten Wegs: {länge_kürzester_weg} Felder")  # Gibt die Länge des kürzesten Weges aus.

# Simulation: Menschliche Strategie - Links folgen
figur_immer_links()

# Abfrage: Warten auf ESC-Taste
esc_gedrückt = False
while True:
    # Überprüft auf Ereignisse wie ESC-Tastendruck oder Fenster schließen.
    for ereignis in pg.event.get():
        if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
            esc_gedrückt = True
            break
        if ereignis.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if esc_gedrückt:  # Beendet die Schleife, wenn ESC gedrückt wurde.
        break

# Simulation: Menschliche Strategie - Rechts folgen
labyrinth_unbekannt_machen()  # Setzt die Darstellung zurück.
figur_immer_rechts()

# Abfrage: Warten auf ESC-Taste
esc_gedrückt = False
while True:
    # Überprüft erneut auf ESC-Tastendruck oder Fenster schließen.
    for ereignis in pg.event.get():
        if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
            esc_gedrückt = True
            break
        if ereignis.type == pg.QUIT:
            pg.quit()
            sys.exit()
    if esc_gedrückt:  # Beendet die Schleife, wenn ESC gedrückt wurde.
        break

# Simulation: KI-Navigation
labyrinth_unbekannt_machen()  # Setzt die Darstellung zurück.

# Initialisierung der KI-Variablen
pos_ki = (0, 0)  # Startposition der KI.
unterschiedliche_besuchte_felder_ki.clear()  # Löscht die Liste der besuchten Felder.
anzahl_besuchte_felder_ki = 0  # Setzt die Anzahl der besuchten Felder zurück.
anzahl_bewegungen_ki = 0  # Setzt die Bewegungsanzahl zurück.
besucht = set()  # Setzt die besuchten Felder zurück.
besucht.add(pos_ki)  # Markiert die Startposition als besucht.

while True:
    # KI führt eine Bewegung aus.
    neue_pos = ki_bewege_sich(pos_ki)

    # Aktualisiert die Anzeige für besuchte Felder.
    for feld in unterschiedliche_besuchte_felder_ki:
        if feld in raster:  # Überprüft, ob das Feld existiert.
            aktualisiere_feld(feld, farbe_besuchte)

    # Zeichnet die KI-Figur auf der neuen Position.
    if neue_pos in raster:  # Überprüft, ob die neue Position gültig ist.
        aktualisiere_feld(neue_pos, farbe_ki)

    pg.display.flip()  # Aktualisiert die Anzeige.
    clock.tick(100)  # Begrenzt die Frame-Rate auf 100 Frames pro Sekunde.

    if neue_pos == ziel:  # Überprüft, ob die Zielposition erreicht wurde.
        visualisiere_weg()  # Visualisiert den Weg nach dem Erreichen des Ziels.
        print(f"Die KI hat das Ziel erreicht und {len(unterschiedliche_besuchte_felder_ki)} verschiedene Felder besucht.")
        print(f"Die KI hat insgesamt {anzahl_bewegungen_ki} Bewegungen gemacht.")
        print(f"Epsilon beträgt aktuell {epsilon}")
        break

    pos_ki = neue_pos  # Aktualisiert die Position der KI.

# Schließen des Programms, wenn ESC gedrückt wird.
esc_gedrückt = False
if esc_gedrückt:
    pg.quit()
    sys.exit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Hauptschleife: Anzeige bleibt geöffnet, bis das Programm beendet wird.
while not pg_quit():
    pg.display.flip()
    clock.tick(30)  # Begrenzt die Frame-Rate auf 30 Frames pro Sekunde.