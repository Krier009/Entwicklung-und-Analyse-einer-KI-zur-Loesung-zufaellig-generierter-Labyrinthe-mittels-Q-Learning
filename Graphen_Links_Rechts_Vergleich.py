import matplotlib.pyplot as plt  # Importiert Matplotlib für die Erstellung von Diagrammen.

# Datei einlesen und Werte für Links und Rechts extrahieren
dateipfad = r"datei_pfad"
# Definiert den Pfad zur Textdatei mit den Ergebnissen des KI-Trainings. 
# Der Dateipfad muss entsprechend angepasst werden, um korrekt zu funktionieren.

# Dateninitialisierung
episoden = []  # Liste zur Speicherung der Episodennummern.
bewegungen_links = []  # Liste zur Speicherung der Bewegungen mit der linken Wand-Technik.
bewegungen_rechts = []  # Liste zur Speicherung der Bewegungen mit der rechten Wand-Technik.

aktuelle_episode = 0  # Variable zur Zählung der Episoden.

# Datei verarbeiten
with open(dateipfad, 'r') as file:  # Öffnet die Datei im Lesemodus.
    for line in file:  # Iteriert durch jede Zeile in der Datei.
        line = line.strip()  # Entfernt Leerzeichen und Steuerzeichen am Anfang und Ende der Zeile.
        if "Links: Anzahl der Bewegungen" in line:  # Prüft auf Daten zur linken Wand-Technik.
            try:
                bewegungen_linke_wand = int(line.split("Anzahl der Bewegungen:")[1].split(",")[0].strip())
                # Extrahiert die Anzahl der Bewegungen für die linke Wand-Technik aus der Zeile.
                bewegungen_links.append(bewegungen_linke_wand)  # Fügt die extrahierten Bewegungen zur Liste hinzu.
            except (ValueError, IndexError) as e:
                # Behandelt mögliche Fehler bei der Verarbeitung der Zeile.
                print(f"Fehler beim Verarbeiten der Zeile (linke Wand): {line} | Fehler: {e}")
        elif "Rechts: Anzahl der Bewegungen" in line:  # Prüft auf Daten zur rechten Wand-Technik.
            try:
                bewegungen_rechte_wand = int(line.split("Anzahl der Bewegungen:")[1].split(",")[0].strip())
                # Extrahiert die Anzahl der Bewegungen für die rechte Wand-Technik aus der Zeile.
                bewegungen_rechts.append(bewegungen_rechte_wand)  # Fügt die extrahierten Bewegungen zur Liste hinzu.
                aktuelle_episode += 1  # Erhöht die Episodennummer um 1.
                episoden.append(aktuelle_episode)  # Fügt die aktuelle Episodennummer zur Liste hinzu.
            except (ValueError, IndexError) as e:
                # Behandelt mögliche Fehler bei der Verarbeitung der Zeile.
                print(f"Fehler beim Verarbeiten der Zeile (rechte Wand): {line} | Fehler: {e}")

# Sicherstellen, dass Daten extrahiert wurden
if not episoden or not bewegungen_links or not bewegungen_rechts:
    # Überprüft, ob Daten für den Vergleich extrahiert wurden.
    print("Fehler: Keine gültigen Daten für die linke oder rechte Wand-Technik gefunden!")
else:
    # Vergleich der Techniken plotten
    plt.figure(figsize=(12, 6))  # Erstellt ein neues Diagramm mit einer festen Größe.
    plt.plot(episoden, bewegungen_links, label="Bewegungen (Linke Wand)", color="blue", linewidth=1.5, linestyle='solid')
    # Zeichnet die Bewegungen mit der linken Wand-Technik gegen die Episodennummern.
    plt.plot(episoden, bewegungen_rechts, label="Bewegungen (Rechte Wand)", color="green", linewidth=1.5, linestyle='solid')
    # Zeichnet die Bewegungen mit der rechten Wand-Technik gegen die Episodennummern.
    plt.title("Vergleich der Techniken: Linke vs. Rechte Wand")  
    # Setzt den Titel des Diagramms.
    plt.xlabel("Episodennummer")  # Beschriftet die x-Achse.
    plt.ylabel("Anzahl der Bewegungen")  # Beschriftet die y-Achse.
    plt.legend()  # Zeigt die Legende an.
    plt.grid(True)  # Fügt ein Gitter hinzu, um die Lesbarkeit zu erhöhen.
    plt.show()  # Zeigt das Diagramm an.
