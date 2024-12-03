import matplotlib.pyplot as plt  # Importiert die Matplotlib-Bibliothek, um Diagramme zu erstellen.

# Datei einlesen
dateipfad = r"C:\Users\colin_d05zgj6\Maturaarbeit\Episoden_resultate_Run 2.txt"
# Definiert den Pfad zur Datei, die die Ergebnisdaten enthält. Passe diesen Pfad an dein System an.

# Dateninitialisierung
episoden = []  # Liste, um die Episodennummern zu speichern.
bewegungen_ki = []  # Liste, um die Anzahl der Bewegungen der KI zu speichern.
bewegungen_links = []  # Liste, um die Anzahl der Bewegungen mit der linken Wand-Technik zu speichern.
bewegungen_rechts = []  # Liste, um die Anzahl der Bewegungen mit der rechten Wand-Technik zu speichern.
besuchte_felder_ki = []  # Liste, um die von der KI besuchten Felder zu speichern.
besuchte_felder_links = []  # Liste, um die von der linken Wand-Technik besuchten Felder zu speichern.
besuchte_felder_rechts = []  # Liste, um die von der rechten Wand-Technik besuchten Felder zu speichern.

aktuelle_episode = 0  # Zähler für die aktuelle Episodennummer.

# Datei verarbeiten
with open(dateipfad, 'r', encoding='utf-8') as file:  
    # Öffnet die Datei im Lesemodus mit UTF-8-Encoding, um sicherzustellen, dass alle Zeichen korrekt gelesen werden.
    for line in file:  # Iteriert durch jede Zeile der Datei.
        line = line.strip()  # Entfernt Leerzeichen und Steuerzeichen am Anfang und Ende der Zeile.
        if "Die KI hat das Ziel erreicht und" in line:  
            # Identifiziert Zeilen, die Informationen über die von der KI besuchten Felder enthalten.
            try:
                # Extrahiert die Anzahl der von der KI besuchten Felder.
                felder_ki = int(line.split("verschiedene Felder besucht.")[0].split()[-1])  
                # Zerlegt die Zeile, um den Wert zu finden, der die Anzahl der besuchten Felder beschreibt.
                besuchte_felder_ki.append(felder_ki)  # Fügt den extrahierten Wert der entsprechenden Liste hinzu.
            except (ValueError, IndexError) as e:
                # Gibt eine Fehlermeldung aus, wenn die Zeile nicht korrekt verarbeitet werden kann.
                print(f"Fehler beim Verarbeiten der Zeile (besuchte Felder KI): {line} | Fehler: {e}")
        elif "Die KI hat insgesamt" in line:  
            # Identifiziert Zeilen, die Informationen über die Bewegungen der KI enthalten.
            try:
                # Extrahiert die Anzahl der Bewegungen der KI.
                bewegungen = int(line.split("Bewegungen gemacht")[0].split()[-1])  
                # Zerlegt die Zeile, um die Bewegungsanzahl zu finden.
                bewegungen_ki.append(bewegungen)  # Fügt den extrahierten Wert der entsprechenden Liste hinzu.
            except (ValueError, IndexError) as e:
                # Gibt eine Fehlermeldung aus, wenn die Zeile nicht korrekt verarbeitet werden kann.
                print(f"Fehler beim Verarbeiten der Zeile (Bewegungen KI): {line} | Fehler: {e}")
        elif "Links: Anzahl der Bewegungen" in line:  
            # Identifiziert Zeilen, die Informationen über die linke Wand-Technik enthalten.
            try:
                # Extrahiert die Anzahl der Bewegungen und besuchten Felder der linken Wand-Technik.
                bewegungen_linke_wand = int(line.split("Anzahl der Bewegungen:")[1].split(",")[0].strip())
                felder_links = int(line.split("Unterschiedliche besuchte Felder:")[1].strip())
                bewegungen_links.append(bewegungen_linke_wand)  # Fügt die Bewegungen zur entsprechenden Liste hinzu.
                besuchte_felder_links.append(felder_links)  # Fügt die besuchten Felder zur entsprechenden Liste hinzu.
            except (ValueError, IndexError) as e:
                # Gibt eine Fehlermeldung aus, wenn die Zeile nicht korrekt verarbeitet werden kann.
                print(f"Fehler beim Verarbeiten der Zeile (linke Wand): {line} | Fehler: {e}")
        elif "Rechts: Anzahl der Bewegungen" in line:  
            # Identifiziert Zeilen, die Informationen über die rechte Wand-Technik enthalten.
            try:
                # Extrahiert die Anzahl der Bewegungen und besuchten Felder der rechten Wand-Technik.
                bewegungen_rechte_wand = int(line.split("Anzahl der Bewegungen:")[1].split(",")[0].strip())
                felder_rechts = int(line.split("Unterschiedliche besuchte Felder:")[1].strip())
                bewegungen_rechts.append(bewegungen_rechte_wand)  # Fügt die Bewegungen zur entsprechenden Liste hinzu.
                besuchte_felder_rechts.append(felder_rechts)  # Fügt die besuchten Felder zur entsprechenden Liste hinzu.
                aktuelle_episode += 1  # Erhöht die Episodennummer um 1.
                episoden.append(aktuelle_episode)  # Fügt die aktuelle Episodennummer der Liste hinzu.
            except (ValueError, IndexError) as e:
                # Gibt eine Fehlermeldung aus, wenn die Zeile nicht korrekt verarbeitet werden kann.
                print(f"Fehler beim Verarbeiten der Zeile (rechte Wand): {line} | Fehler: {e}")

# Bewegungen auf Werte unter 200.000 beschränken
bewegungen_ki_gefiltert = [bewegung if bewegung < 200000 else 200000 for bewegung in bewegungen_ki]
# Limitiert die Bewegungen der KI auf maximal 200.000, um Extremwerte besser darzustellen.

# Graph erstellen
if episoden and bewegungen_ki_gefiltert and bewegungen_links and bewegungen_rechts:  
    # Überprüft, ob genügend Daten vorhanden sind, um den Graphen zu erstellen.
    plt.figure(figsize=(12, 8))  # Erstellt eine Diagrammfläche mit den angegebenen Abmessungen.

    # Bewegungen vergleichen
    plt.subplot(2, 1, 1)  # Erstes Unterdiagramm: Vergleich der Bewegungen.
    plt.plot(episoden, bewegungen_ki_gefiltert[:len(episoden)], label="KI Bewegungen (Gefiltert)", color="blue")
    # Zeichnet die Bewegungen der KI gegen die Episodennummern.
    plt.plot(episoden, bewegungen_links, label="Bewegungen (Linke Wand)", color="green")
    # Zeichnet die Bewegungen der linken Wand-Technik.
    plt.plot(episoden, bewegungen_rechts, label="Bewegungen (Rechte Wand)", color="orange")
    # Zeichnet die Bewegungen der rechten Wand-Technik.
    plt.title("Vergleich der Bewegungen: KI vs. Mensch")  # Setzt den Titel für das Diagramm.
    plt.xlabel("Episodennummer")  # Beschriftet die x-Achse.
    plt.ylabel("Anzahl der Bewegungen")  # Beschriftet die y-Achse.
    plt.legend(loc="upper right")  # Positioniert die Legende oben rechts.
    plt.grid(True)  # Fügt ein Gitter hinzu, um die Lesbarkeit zu erhöhen.

    # Besuchte Felder vergleichen
    plt.subplot(2, 1, 2)  # Zweites Unterdiagramm: Vergleich der besuchten Felder.
    plt.plot(episoden, besuchte_felder_ki[:len(episoden)], color="blue", linestyle="--", label="Besuchte Felder (KI)")
    plt.plot(episoden, besuchte_felder_links, color="green", linestyle="--", label="Besuchte Felder (Linke Wand)")
    plt.plot(episoden, besuchte_felder_rechts, color="orange", linestyle="--", label="Besuchte Felder (Rechte Wand)")
    plt.title("Vergleich der besuchten Felder: KI vs. Mensch")  # Setzt den Titel für das Diagramm.
    plt.xlabel("Episodennummer")  # Beschriftet die x-Achse.
    plt.ylabel("Anzahl der besuchten Felder")  # Beschriftet die y-Achse.
    plt.legend(loc="upper right")  # Positioniert die Legende oben rechts.
    plt.grid(True)  # Fügt ein Gitter hinzu.

    plt.tight_layout()  # Passt die Abstände zwischen den Diagrammen an, um Überlappungen zu vermeiden.
    plt.show()  # Zeigt die erstellten Diagramme an.
else:
    print("Fehler: Nicht genügend Daten für den Graphen gefunden!")
    # Gibt eine Fehlermeldung aus, wenn keine ausreichenden Daten für die Diagrammerstellung vorliegen.
