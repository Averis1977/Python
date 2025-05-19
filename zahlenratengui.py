import tkinter as tk
import random

class ZahlenratenSpiel:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Zahlenratespiel")
        self.geheimzahl = random.randint(1, 100)
        self.versuche = 0

        self.label_info = tk.Label(master, text="Ich habe eine Zahl zwischen 1 und 100 gewählt.")
        self.label_info.pack(pady=10)

        self.label_status = tk.Label(master, text="Gib deinen Tipp ein:")
        self.label_status.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Tipp abgeben", command=self.pruefe_tipp)
        self.button.pack(pady=10)

        self.label_ergebnis = tk.Label(master, text="")
        self.label_ergebnis.pack(pady=5)

        self.button_neu = tk.Button(master, text="Neues Spiel starten", command=self.neues_spiel)
        self.button_neu.pack(pady=5)

    def pruefe_tipp(self):
        try:
            tipp = int(self.entry.get())
            self.versuche += 1
            if tipp < self.geheimzahl:
                self.label_ergebnis.config(text="Zu niedrig!")
            elif tipp > self.geheimzahl:
                self.label_ergebnis.config(text="Zu hoch!")
            else:
                self.label_ergebnis.config(
                    text=f"Richtig! Die Zahl war {self.geheimzahl}.\nVersuche: {self.versuche}")
        except ValueError:
            self.label_ergebnis.config(text="Bitte gib eine gültige Zahl ein.")

    def neues_spiel(self):
        self.geheimzahl = random.randint(1, 100)
        self.versuche = 0
        self.entry.delete(0, tk.END)
        self.label_ergebnis.config(text="Neues Spiel gestartet!")

# Fenster starten
root = tk.Tk()
spiel = ZahlenratenSpiel(root)
root.mainloop()
