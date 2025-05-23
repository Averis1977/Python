import tkinter as tk
from tkinter import messagebox

# Fahrzeug-Klasse
class Fahrzeug:
    def __init__(self, farbe, groesse, tueren, kraftstoff, fahrzeugtyp,
                 baujahr, hersteller, getriebeart, sitze, zulassung):
        self.farbe = farbe
        self.groesse = groesse
        self.tueren = tueren
        self.kraftstoff = kraftstoff
        self.fahrzeugtyp = fahrzeugtyp
        self.baujahr = baujahr
        self.hersteller = hersteller
        self.getriebeart = getriebeart
        self.sitze = sitze
        self.zulassung = zulassung

    def tausche_farbe_kraftstoff(self):
        self.farbe, self.kraftstoff = self.kraftstoff, self.farbe

    def daten_anzeigen(self):
        return (f"Farbe: {self.farbe}\n"
                f"Größe: {self.groesse}\n"
                f"Türen: {self.tueren}\n"
                f"Kraftstoff: {self.kraftstoff}\n"
                f"Typ: {self.fahrzeugtyp}\n"
                f"Baujahr: {self.baujahr}\n"
                f"Hersteller: {self.hersteller}\n"
                f"Getriebe: {self.getriebeart}\n"
                f"Sitze: {self.sitze}\n"
                f"Zulassung erlaubt: {self.zulassung}")

# GUI-Funktionen
def fahrzeug_erstellen():
    try:
        f = Fahrzeug(
            farbe_var.get(),
            groesse_var.get(),
            tueren_var.get(),
            kraftstoff_var.get(),
            typ_var.get(),
            int(baujahr_var.get()),
            hersteller_var.get(),
            getriebe_var.get(),
            int(sitze_var.get()),
            bool(zulassung_var.get())
        )
        global aktuelles_fahrzeug
        aktuelles_fahrzeug = f
        ausgabe_text.delete("1.0", tk.END)
        ausgabe_text.insert(tk.END, f.daten_anzeigen())
    except Exception as e:
        messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")

def tausche_werte():
    if aktuelles_fahrzeug:
        aktuelles_fahrzeug.tausche_farbe_kraftstoff()
        ausgabe_text.delete("1.0", tk.END)
        ausgabe_text.insert(tk.END, aktuelles_fahrzeug.daten_anzeigen())

# GUI-Fenster
root = tk.Tk()
root.title("Fahrzeug-Daten GUI")

# Variablen
farbe_var = tk.StringVar()
groesse_var = tk.StringVar()
tueren_var = tk.StringVar()
kraftstoff_var = tk.StringVar()
typ_var = tk.StringVar()
baujahr_var = tk.StringVar()
hersteller_var = tk.StringVar()
getriebe_var = tk.StringVar()
sitze_var = tk.StringVar()
zulassung_var = tk.IntVar()

aktuelles_fahrzeug = None

# Eingabefelder
felder = [
    ("Farbe", farbe_var),
    ("Größe", groesse_var),
    ("Türen", tueren_var),
    ("Kraftstoff", kraftstoff_var),
    ("Fahrzeugtyp", typ_var),
    ("Baujahr", baujahr_var),
    ("Hersteller", hersteller_var),
    ("Getriebeart", getriebe_var),
    ("Sitze", sitze_var),
]

for i, (label, var) in enumerate(felder):
    tk.Label(root, text=label).grid(row=i, column=0, sticky="w")
    tk.Entry(root, textvariable=var).grid(row=i, column=1)

tk.Checkbutton(root, text="Zulassung erlaubt", variable=zulassung_var).grid(row=len(felder), columnspan=2, pady=5)

# Buttons
tk.Button(root, text="Fahrzeug erstellen & anzeigen", command=fahrzeug_erstellen).grid(row=10, column=0, pady=10)
tk.Button(root, text="Farbe & Kraftstoff tauschen", command=tausche_werte).grid(row=10, column=1, pady=10)

# Ausgabe
ausgabe_text = tk.Text(root, height=10, width=40)
ausgabe_text.grid(row=11, columnspan=2, padx=5, pady=5)

root.mainloop()
