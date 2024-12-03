import matplotlib.pyplot as plt  # Importiert die Matplotlib-Bibliothek zum Erstellen von Graphen.
import matplotlib.ticker as mticker  # Importiert Matplotlib-Ticker, um die Achsenbeschriftungen anzupassen.

# Datei einlesen
dateipfad = r"datei_pfad"  
# Definiert den Pfad zur Textdatei mit den Ergebnissen des KI-Trainings. 
# Der Dateipfad muss entsprechend angepasst werden, um auf deinem System zu funktionieren.

# Dateninitialisierung
episoden_nummern = []  # Liste zur Speicherung der Episodennummern.
bewegungs_anzahlen = []  # Liste zur Speicherung der Anzahl der Bewegungen der KI.

aktuelle_episode = 0  # Variable, um die aktuelle Episodennummer zu zählen.

# Öffnen der Datei und Verarbeitung der Zeilen
with open(dateipfad, 'r') as file:  # Öffnet die Datei im Lesemodus.
    for line in file:  # Iteriert durch jede Zeile der Datei.
        line = line.strip()  # Entfernt Leerzeichen und Steuerzeichen am Anfang und Ende der Zeile.
        if "Die KI hat insgesamt" in line:  
            # Prüft, ob die Zeile Informationen über die Anzahl der Bewegungen enthält.
            try:
                # Bewegungszahlen extrahieren (bereits in Millionen)
                bewegungen = int(line.split("Bewegungen gemacht")[0].split()[-1])  
                # Zerlegt die Zeile, um die Anzahl der Bewegungen zu extrahieren.
                aktuelle_episode += 1  # Erhöht die Episodennummer um 1.
                episoden_nummern.append(aktuelle_episode)  # Fügt die aktuelle Episodennummer zur Liste hinzu.
                bewegungs_anzahlen.append(bewegungen)  # Fügt die Bewegungszahl zur Liste hinzu.

                # Beende nach 5000 Episoden
                if aktuelle_episode >= 5000:
                    break  # Bricht die Schleife ab, wenn 5000 Episoden erreicht wurden.
            except (ValueError, IndexError) as e:
                # Behandelt Fehler beim Verarbeiten der Zeile und gibt eine Fehlermeldung aus.
                print(f"Fehler beim Verarbeiten der Zeile: {line} | Fehler: {e}")

# Graph erstellen
if episoden_nummern and bewegungs_anzahlen:
    # Prüft, ob die Listen nicht leer sind, bevor ein Graph erstellt wird.
    plt.figure(figsize=(10, 6))  # Erstellt ein neues Diagramm mit fester Größe.
    plt.plot(episoden_nummern, bewegungs_anzahlen, label="Bewegungen der KI", color="blue")  
    # Zeichnet die Anzahl der Bewegungen gegen die Episodennummern.
    plt.title("Anzahl der Bewegungen pro Episode (1-5000)")  
    # Setzt den Titel des Graphen.
    plt.xlabel("Episodennummer")  # Beschriftet die x-Achse.
    plt.ylabel("Anzahl der Bewegungen (in Millionen)")  # Beschriftet die y-Achse.
    plt.legend()  # Zeigt die Legende an.
    plt.grid(True)  # Fügt ein Gitter hinzu, um die Lesbarkeit zu erhöhen.

    # Formatierung der Y-Achse
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1e6)}M'))
    # Passt die y-Achse an, um die Werte in Millionen anzuzeigen.

    plt.show()  # Zeigt den Graphen an.
else:
    # Gibt eine Fehlermeldung aus, wenn keine Daten zum Plotten vorhanden sind.
    print("Keine gültigen Daten für den Graphen gefunden.")

