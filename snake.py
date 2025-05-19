import tkinter as tk
import random
import winsound  

BREITE = 400
HOEHE = 400
GRÖSSE = 20

class SnakeSpiel:
    def __init__(self, master):
        self.master = master
        self.master.title("🐍 Snake Pro")
        self.canvas = tk.Canvas(master, width=BREITE, height=HOEHE, bg="black")
        self.canvas.pack()

        self.richtung = "Right"
        self.schlangen_teile = [(100, 100), (80, 100), (60, 100)]
        self.futter = ()
        self.punkte = 0
        self.speed = 150  

        self.text = self.canvas.create_text(10, 10, fill="white", text=f"Punkte: {self.punkte}", anchor="nw")

        self.master.bind("<Key>", self.steuerung)
        self.spiel_laeuft = True

        self.zeichne_schlange()
        self.erzeuge_futter()
        self.bewege()

    def zeichne_schlange(self):
        self.canvas.delete("snake")
        for x, y in self.schlangen_teile:
            self.canvas.create_rectangle(x, y, x + GRÖSSE, y + GRÖSSE, fill="lime", tags="snake")

    def erzeuge_futter(self):
        while True:
            x = random.randint(0, (BREITE - GRÖSSE) // GRÖSSE) * GRÖSSE
            y = random.randint(0, (HOEHE - GRÖSSE) // GRÖSSE) * GRÖSSE
            if (x, y) not in self.schlangen_teile:
                self.futter = (x, y)
                self.canvas.create_oval(x, y, x + GRÖSSE, y + GRÖSSE, fill="red", tags="futter")
                break

    def steuerung(self, event):
        tasten = {
            "Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right",
            "w": "Up", "s": "Down", "a": "Left", "d": "Right"
        }
        neue_richtung = tasten.get(event.keysym, self.richtung)
        gegenrichtung = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if neue_richtung != gegenrichtung.get(self.richtung):
            self.richtung = neue_richtung

    def bewege(self):
        if not self.spiel_laeuft:
            return

        x, y = self.schlangen_teile[0]
        if self.richtung == "Right":
            x += GRÖSSE
        elif self.richtung == "Left":
            x -= GRÖSSE
        elif self.richtung == "Up":
            y -= GRÖSSE
        elif self.richtung == "Down":
            y += GRÖSSE

        neuer_kopf = (x, y)

        
        if (
            x < 0 or x >= BREITE or y < 0 or y >= HOEHE or
            neuer_kopf in self.schlangen_teile
        ):
            self.game_over()
            return

        self.schlangen_teile.insert(0, neuer_kopf)

        
        if neuer_kopf == self.futter:
            self.punkte += 1
            self.canvas.itemconfig(self.text, text=f"Punkte: {self.punkte}")
            self.canvas.delete("futter")
            self.erzeuge_futter()
            self.plopp_sound()
            self.speed = max(50, self.speed - 5)  
        else:
            self.schlangen_teile.pop()

        self.zeichne_schlange()
        self.master.after(self.speed, self.bewege)

    def game_over(self):
        self.spiel_laeuft = False
        self.canvas.create_text(
            BREITE // 2, HOEHE // 2,
            fill="red", font=("Arial", 28, "bold"),
            text="💀 Game Over"
        )
        self.game_over_effect()
        self.game_over_sound()

    def game_over_effect(self):
        for i in range(3):
            self.master.after(i * 200, lambda: self.canvas.config(bg="darkred" if i % 2 == 0 else "black"))

    def plopp_sound(self):
        winsound.Beep(800, 150)  

    def game_over_sound(self):
        winsound.Beep(300, 400)


root = tk.Tk()
spiel = SnakeSpiel(root)
root.mainloop()
