import matplotlib.pyplot as plt  # Importiert die Bibliothek Matplotlib, die für die Erstellung von Diagrammen und Graphen verwendet wird.

# Datei einlesen
file_path = r"datei_pfad"  
# Definiert den Dateipfad der Textdatei, die die Ergebnisse der KI-Trainings enthält. 
# Hinweis: Dieser Pfad muss entsprechend angepasst werden, um auf deinem System zu funktionieren.

# Dateninitialisierung
episoden_nummern = []  # Liste, um die Nummern der Episoden zu speichern.
einzigartige_felder = []  # Liste, um die Anzahl der von der KI besuchten Felder zu speichern.
kürzeste_wege = []  # Liste, um die Länge des kürzesten Weges zu speichern.

aktuelle_episode = 0  # Variable, die die aktuelle Episodennummer zählt.

# Öffnen der Datei und Verarbeitung Zeile für Zeile
with open(file_path, 'r', encoding='utf-8') as file:  # Öffnet die Datei im Lesemodus mit UTF-8-Encoding.
    for line in file:  # Iteriert durch jede Zeile der Datei.
        line = line.strip()  # Entfernt führende und nachfolgende Leerzeichen aus der Zeile.
        if "Die KI hat das Ziel erreicht und" in line:  
            # Prüft, ob die Zeile Informationen über besuchte Felder enthält.
            try:
                # Unterschiedliche besuchte Felder extrahieren
                felder = int(line.split("verschiedene Felder besucht.")[0].split()[-1])  
                # Zerlegt die Zeile, um die Anzahl der unterschiedlichen besuchten Felder zu extrahieren.
                aktuelle_episode += 1  # Erhöht die Episodennummer um 1.
                episoden_nummern.append(aktuelle_episode)  # Fügt die aktuelle Episode zur Liste hinzu.
                einzigartige_felder.append(felder)  # Fügt die Anzahl der besuchten Felder zur Liste hinzu.

                # Beende nach 5000 Episoden
                if aktuelle_episode >= 5000:
                    break  # Bricht die Schleife ab, wenn 5000 Episoden erreicht wurden.
            except (ValueError, IndexError) as e:
                # Fängt Fehler beim Verarbeiten der Zeile ab und gibt eine Fehlermeldung aus.
                print(f"Fehler beim Verarbeiten der Zeile für besuchte Felder: {line} | Fehler: {e}")
        elif "Länge des kürzesten Wegs:" in line:
            # Prüft, ob die Zeile Informationen über den kürzesten Weg enthält.
            try:
                # Kürzesten Weg extrahieren
                kürzester_weg = int(line.split("Länge des kürzesten Wegs:")[1].strip())  
                # Extrahiert die Länge des kürzesten Weges aus der Zeile.
                kürzeste_wege.append(kürzester_weg)  # Fügt die Weglänge zur Liste hinzu.
            except (ValueError, IndexError) as e:
                # Fängt Fehler beim Verarbeiten der Zeile ab und gibt eine Fehlermeldung aus.
                print(f"Fehler beim Verarbeiten der Zeile für kürzesten Weg: {line} | Fehler: {e}")

# Sicherstellen, dass die Datenlängen übereinstimmen
minimale_länge = min(len(episoden_nummern), len(einzigartige_felder), len(kürzeste_wege))
# Ermittelt die kürzeste Liste, um sicherzustellen, dass alle Listen dieselbe Länge haben.
episoden_nummern = episoden_nummern[:minimale_länge]  # Kürzt die Episodenliste auf die minimale Länge.
einzigartige_felder = einzigartige_felder[:minimale_länge]  # Kürzt die Liste der einzigartigen Felder.
kürzeste_wege = kürzeste_wege[:minimale_länge]  # Kürzt die Liste der kürzesten Wege.

# Graph erstellen
if episoden_nummern and einzigartige_felder and kürzeste_wege:
    # Prüft, ob die Listen nicht leer sind, bevor ein Graph erstellt wird.
    plt.figure(figsize=(10, 6))  # Erstellt ein neues Diagramm mit einer festen Größe.
    plt.plot(
        episoden_nummern, einzigartige_felder,
        label="Besuchte Felder der KI", color="blue"
    )
    # Zeichnet die Anzahl der besuchten Felder gegen die Episodennummern.
    plt.plot(
        episoden_nummern, kürzeste_wege,
        label="Länge des kürzesten Wegs", color="red", linestyle='--'
    )
    # Zeichnet die Länge des kürzesten Weges gegen die Episodennummern.
    plt.title("Vergleich: Besuchte Felder der KI vs. Kürzester Weg")
    # Setzt den Titel des Graphen.
    plt.xlabel("Episodennummer")  # Beschriftet die x-Achse.
    plt.ylabel("Anzahl Felder / Weglänge")  # Beschriftet die y-Achse.
    plt.legend()  # Zeigt die Legende für den Graphen an.
    plt.grid(True)  # Fügt ein Gitter hinzu, um die Lesbarkeit zu erhöhen.
    plt.show()  # Zeigt den Graphen an.
else:
    # Gibt eine Fehlermeldung aus, wenn keine Daten zum Plotten vorhanden sind.
    print("Keine gültigen Daten für den Graphen gefunden.")
