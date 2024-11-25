#Provisorische MA

# Bibliotheken: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import pygame as pg
import random as rnd
import sys
import numpy as np
import os               # Import für Dateipfadüberprüfung
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Labyrinth ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sys.setrecursionlimit(3600) #vergrössert das Pop-out Fenster

# Konstanten
BREITE = HÖHE = 1000
SPALTEN = ZEILEN = 60
ZELLE_BREITE_HÖHE = BREITE // SPALTEN

# Bewegungsdelta und Nachbarinformation
delta_linien = {
    "l": [(0, 0), (0, ZELLE_BREITE_HÖHE)],
    "r": [(ZELLE_BREITE_HÖHE, 0), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)],
    "o": [(0, 0), (ZELLE_BREITE_HÖHE, 0)],
    "u": [(0, ZELLE_BREITE_HÖHE), (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)]
}
delta_nachbarn = {
    "l": (-ZELLE_BREITE_HÖHE, 0),
    "r": (ZELLE_BREITE_HÖHE, 0),
    "o": (0, -ZELLE_BREITE_HÖHE),
    "u": (0, ZELLE_BREITE_HÖHE)
}
richtung_invers = {"l": "r", "r": "l", "o": "u", "u": "o"}
richtung_rechts = {"l": "o", "o": "r", "r": "u", "u": "l"}
richtung_links = {"l": "u", "u": "r", "r": "o", "o": "l"}

# Pygame initialisieren
pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
farbe_hintergrund = pg.Color("Black")
farbe_linien = pg.Color("White")
farbe_weg = pg.Color("gold2")
farbe_figur_rechts = pg.Color("red")
farbe_figur_links = pg.Color("green")
farbe_ki = pg.Color("green")
farbe_besuchte = pg.Color("dodgerblue4")

# Uhr initialisieren
clock = pg.time.Clock()

def add_pos(pos1, pos2):
    return pos1[0] + pos2[0], pos1[1] + pos2[1]

def pg_quit():
    for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT or (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
            return True

def nachbarn_ermitteln(pos):
    nachbarn = []
    for richtung, delta in delta_nachbarn.items():
        neue_pos = add_pos(pos, delta)
        if neue_pos not in raster: continue
        nachbarn.append((richtung, neue_pos))
    rnd.shuffle(nachbarn)
    return nachbarn

def mögliche_richtungen(pos):
    richtungen = []
    for richtung, delta in delta_nachbarn.items():
        neue_pos = add_pos(pos, delta)
        if neue_pos not in raster:
            continue
        if richtung in raster[pos]:
            continue
        richtungen.append(neue_pos)
    return richtungen

def zeichne_zelle(pos, wände):
    for wand in wände:
        delta_von, delta_bis = delta_linien[wand]
        von = add_pos(pos, delta_von)
        bis = add_pos(pos, delta_bis)
        pg.draw.line(screen, farbe_linien, von, bis, 2)

def labyrinth_unbekannt_machen():
    screen.fill(farbe_hintergrund)  # Bildschirm mit Hintergrundfarbe füllen

def aktualisiere_feld(pos, farbe):
    pg.draw.rect(screen, farbe, (pos, (ZELLE_BREITE_HÖHE, ZELLE_BREITE_HÖHE)))
    zeichne_zelle(pos, raster[pos])

def in_bounds(pos):
    x, y = pos
    return 0 <= x < SPALTEN * ZELLE_BREITE_HÖHE and 0 <= y < ZEILEN * ZELLE_BREITE_HÖHE

def labyrinth_erstellen(pos_aktuell, richtung_von):
    besucht.add(pos_aktuell)
    if richtung_von is not None:
        raster[pos_aktuell].remove(richtung_von)
    nachbarn = nachbarn_ermitteln(pos_aktuell)
    for richtung_nach, pos_neu in nachbarn:
        if pos_neu in besucht:
            continue
        raster[pos_aktuell].remove(richtung_nach)
        labyrinth_erstellen(pos_neu, richtung_invers[richtung_nach])


ziel = ((SPALTEN - 1) * ZELLE_BREITE_HÖHE, (ZEILEN - 1) * ZELLE_BREITE_HÖHE)
weg = []
länge_kürzester_weg = 0

def labyrinth_lösen(pos_aktuell):
    global länge_kürzester_weg
    besucht.append(pos_aktuell)
    if pos_aktuell == ziel:
        weg.append(pos_aktuell)
        länge_kürzester_weg += 1
        return True
    for pos_neu in mögliche_richtungen(pos_aktuell):
        if pos_neu in besucht:
            continue
        if labyrinth_lösen(pos_neu):
            weg.append(pos_neu)
            länge_kürzester_weg += 1
            return True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


 #Visualisierung des kürzesten Weges ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
def visualisiere_weg():
    # Visualisierung des kürzesten Wegs
    i = 0
    while i < len(weg) and not pg_quit():  # Stellen Sie sicher, dass i innerhalb der Grenzen bleibt
        clock.tick(150)
        x, y = weg[i]
        x, y = x + ZELLE_BREITE_HÖHE // 2, y + ZELLE_BREITE_HÖHE // 2
        pg.draw.circle(screen, farbe_weg, (x, y), ZELLE_BREITE_HÖHE // 6)
        for pos, wände in raster.items():
            zeichne_zelle(pos, wände)
        pg.display.flip()
        i += 1  # Inkrementieren Sie i, anstatt min zu verwenden
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 
#Menschliche Vergleichsweisen~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def figur_bewegt_sich_rechts(pos_aktuell, richtung):
    rechts_richtung = richtung_rechts[richtung]
    rechts_pos = add_pos(pos_aktuell, delta_nachbarn[rechts_richtung])
    if rechts_richtung not in raster.get(pos_aktuell, set()):
        return rechts_pos, rechts_richtung
    geradeaus_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])
    if richtung not in raster.get(pos_aktuell, set()):
        return geradeaus_pos, richtung
    links_richtung = richtung_links[richtung]
    links_pos = add_pos(pos_aktuell, delta_nachbarn[links_richtung])
    if links_richtung not in raster.get(pos_aktuell, set()):
        return links_pos, links_richtung
    zurück_pos = add_pos(pos_aktuell, delta_nachbarn[richtung_invers[richtung]])
    return zurück_pos, richtung_invers[richtung]

def figur_bewegt_sich_links(pos_aktuell, richtung):
    links_richtung = richtung_links[richtung]
    links_pos = add_pos(pos_aktuell, delta_nachbarn[links_richtung])
    if links_richtung not in raster.get(pos_aktuell, set()):
        return links_pos, links_richtung
    geradeaus_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])
    if richtung not in raster.get(pos_aktuell, set()):
        return geradeaus_pos, richtung
    rechts_richtung = richtung_rechts[richtung]
    rechts_pos = add_pos(pos_aktuell, delta_nachbarn[rechts_richtung])
    if rechts_richtung not in raster.get(pos_aktuell, set()):
        return rechts_pos, rechts_richtung
    zurück_pos = add_pos(pos_aktuell, delta_nachbarn[richtung_invers[richtung]])
    return zurück_pos, richtung_invers[richtung]


def figur_immer_rechts():
    pos_figur = (0, 0)
    richtung = "r"
    anzahl_besuchte_felder_rechts = set()
    anzahl_bewegungen_rechts = 0

    while not pg_quit():
        clock.tick(100)
        if pos_figur not in anzahl_besuchte_felder_rechts:
            anzahl_besuchte_felder_rechts.add(pos_figur)
            aktualisiere_feld(pos_figur, farbe_besuchte)
        alte_pos = pos_figur
        pos_figur, richtung = figur_bewegt_sich_rechts(pos_figur, richtung)
        anzahl_bewegungen_rechts += 1
        if in_bounds(pos_figur):
            aktualisiere_feld(pos_figur, farbe_figur_rechts)
        if alte_pos != pos_figur and in_bounds(alte_pos):
            aktualisiere_feld(alte_pos, farbe_besuchte)
        pg.display.flip()
        if pos_figur == ziel:
            break

    print(f"Rechts: Anzahl der Bewegungen: {anzahl_bewegungen_rechts}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_rechts)}")

    # Visualisiere den Weg nach der ersten Figur
    visualisiere_weg()


def figur_immer_links():
    pos_figur = (0, 0)
    richtung = "r"
    anzahl_besuchte_felder_links = set()
    anzahl_bewegungen_links = 0

    while not pg_quit():
        clock.tick(100)
        if pos_figur not in anzahl_besuchte_felder_links:
            anzahl_besuchte_felder_links.add(pos_figur)
            aktualisiere_feld(pos_figur, farbe_besuchte)
        alte_pos = pos_figur
        pos_figur, richtung = figur_bewegt_sich_links(pos_figur, richtung)
        anzahl_bewegungen_links += 1
        if in_bounds(pos_figur):
            aktualisiere_feld(pos_figur, farbe_figur_links)
        if alte_pos != pos_figur and in_bounds(alte_pos):
            aktualisiere_feld(alte_pos, farbe_besuchte)
        pg.display.flip()
        if pos_figur == ziel:
            break

    print(f"Links: Anzahl der Bewegungen: {anzahl_bewegungen_links}, Unterschiedliche besuchte Felder: {len(anzahl_besuchte_felder_links)}")

    # Visualisiere den Weg nach der ersten Figur
    visualisiere_weg()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#Künstliche Intelligenz ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Q-Learning Variablen
q_table = np.zeros((SPALTEN, ZEILEN, 4))  # 4 Aktionen: l, r, o, u
action_map = {"l": 0, "r": 1, "o": 2, "u": 3}
learning_rate = 0.2
discount_factor = 0.99
epsilon = 1
epsilon_decay = 0.999
episodes = 100  # Anzahl der Episoden
durchlaeufe = 100

# Variablen für die KI
pos_ki = (0, 0)
unterschiedliche_besuchte_felder_ki = []
anzahl_besuchte_felder_ki = 1
anzahl_bewegungen_ki = 0
gesamte_episoden = 0

# Q-Learning Variablen
q_table_path = "q_table.npy"  # Pfad zur Speicherdatei der Q-Tabelle


def lade_q_table(dateipfad):
    if os.path.exists(dateipfad):
        print(f"Q-Tabelle wurde gefunden: {dateipfad}")
        return np.load(dateipfad)
    else:
        print(f"Keine gespeicherte Q-Tabelle gefunden unter: {dateipfad}")
        return np.zeros((SPALTEN, ZEILEN, 4))  # Leere Q-Tabelle, falls keine Datei existiert

def ki_bewege_sich(pos_aktuell):
    global anzahl_bewegungen_ki
    anzahl_bewegungen_ki += 1

    # Entscheidung treffen (Exploration oder Exploitation)
    if rnd.uniform(0, 1) < epsilon:
        action = rnd.choice(range(4))
    else:
        action = np.argmax(q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE])

    richtung = list(action_map.keys())[action]
    neue_pos = add_pos(pos_aktuell, delta_nachbarn[richtung])

    # Bewegung validieren
    if neue_pos in raster and richtung not in raster[pos_aktuell]: 
        if neue_pos not in unterschiedliche_besuchte_felder_ki:
            unterschiedliche_besuchte_felder_ki.append(neue_pos)
            reward = +5  # Belohnung für Besuch eines neuen Feldes
        else:
            reward = -1  # Strafe für Wiederbesuch
    else:
        neue_pos = pos_aktuell
        reward = -1  # Strafe für ungültige Bewegung

    if neue_pos == ziel:
        reward = 1000

    # Q-Update
    old_value = q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE, action]
    future_reward = np.max(q_table[neue_pos[0] // ZELLE_BREITE_HÖHE, neue_pos[1] // ZELLE_BREITE_HÖHE])
    q_table[pos_aktuell[0] // ZELLE_BREITE_HÖHE, pos_aktuell[1] // ZELLE_BREITE_HÖHE, action] = old_value + learning_rate * (reward + discount_factor * future_reward - old_value)

    return neue_pos
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Abfrage vom Benutzer
q_table = None
while True:
    antwort = input("Möchten Sie eine vorhandene Q-Tabelle laden? (ja/nein): ").strip().lower()
    if antwort == "ja":
        q_table = lade_q_table(q_table_path)
        break
    elif antwort == "nein":
        break
    else:
        print("Ungültige Eingabe. Bitte geben Sie 'ja' oder 'nein' ein.")

raster = {}  # Leeren des Rasters vor jeder neuen Episode
for i in range(SPALTEN * ZEILEN):
    pos = (i % SPALTEN * ZELLE_BREITE_HÖHE, i // SPALTEN * ZELLE_BREITE_HÖHE)
    raster[pos] = {"l", "r", "o", "u"}  # Alle Wände hinzufügen
länge_kürzester_weg = 0

besucht = set()
labyrinth_erstellen((0, 0), "l")  # Labyrinth generieren
besucht = []  # Zurücksetzen der besuchten Felder
labyrinth_lösen((0, 0))  # Kürzesten Weg bestimmen
print(f"Länge des kürzesten Wegs: {länge_kürzester_weg} Felder")
figur_immer_links()

# Variable, die anzeigt, ob ESC gedrückt wurde
esc_gedrückt = False

# Warte auf ESC-Taste
while True:
    for ereignis in pg.event.get():
        if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
            esc_gedrückt = True
            break
        if ereignis.type == pg.QUIT:
            pg.quit()
            sys.exit()
    # Beende die Schleife, wenn ESC gedrückt wurde
    if esc_gedrückt:
        break

labyrinth_unbekannt_machen()
figur_immer_rechts()

# Variable, die anzeigt, ob ESC gedrückt wurde
esc_gedrückt = False

# Warte auf ESC-Taste
while True:
    for ereignis in pg.event.get():
        if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
            esc_gedrückt = True
            break
        if ereignis.type == pg.QUIT:
            pg.quit()
            sys.exit()
    # Beende die Schleife, wenn ESC gedrückt wurde
    if esc_gedrückt:
        break

labyrinth_unbekannt_machen()

#KI bewegt sich durch das Labyrinth
pos_ki = (0, 0)
unterschiedliche_besuchte_felder_ki.clear()
anzahl_besuchte_felder_ki = 0
anzahl_bewegungen_ki = 0
besucht = set()
besucht.add(pos_ki)

while True:
    neue_pos = ki_bewege_sich(pos_ki)  # KI-Logik einfügen

    # Aktualisiere die Anzeige
    for feld in unterschiedliche_besuchte_felder_ki:
        if feld in raster:  # Überprüfen, ob die Position im Raster existiert
            aktualisiere_feld(feld, farbe_besuchte)

    # Jetzt die Figur auf der neuen Position zeichnen
    if neue_pos in raster:  # Überprüfen, ob die neue Position im Raster existiert
        aktualisiere_feld(neue_pos, farbe_ki)

    pg.display.flip()
    clock.tick(100)  # Hier die Framerate einstellen

    if neue_pos == ziel:
        # Visualisiere den Weg nach der ersten Figur
        visualisiere_weg()
        print(f"Die KI hat das Ziel erreicht und {len(unterschiedliche_besuchte_felder_ki)} verschiedene Felder besucht.")
        print(f"Die KI hat insgesamt {anzahl_bewegungen_ki} Bewegungen gemacht.")
        print(f"Epsilon beträgt aktuell {epsilon}")
        break

    pos_ki = neue_pos

# Setze esc_gedrückt zurück, bevor figur_immer_links() ausgeführt wird
esc_gedrückt = False

# Schließe das Fenster, wenn ESC gedrückt wurde
if esc_gedrückt:
    pg.quit()
    sys.exit()

# Andernfalls bleibt das Fenster geöffnet
while not pg_quit():
    pg.display.flip()
    clock.tick(30)