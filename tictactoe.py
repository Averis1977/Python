import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("❌ Tic Tac Toe ⭕")
        self.spieler = "X"
        self.spielmodus = "KI"  # oder "2-Spieler"

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.felder = [["" for _ in range(3)] for _ in range(3)]

        self.info_label = tk.Label(master, text="Spieler: X", font=("Arial", 16))
        self.info_label.pack()

        self.feld = tk.Frame(master)
        self.feld.pack()

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.feld, text="", font=("Arial", 36), width=5, height=2,
                                command=lambda i=i, j=j: self.klick(i, j))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        self.restart_btn = tk.Button(master, text="🔁 Neustart", command=self.neustart, font=("Arial", 12))
        self.restart_btn.pack(pady=10)

    def klick(self, i, j):
        if self.felder[i][j] != "":
            return
        self.setze_zeichen(i, j, self.spieler)

        if self.check_sieg(self.spieler):
            self.zeige_animation(i, j)
            messagebox.showinfo("🎉 Spielende", f"{self.spieler} gewinnt!")
            self.deaktiviere_alle()
            return
        elif self.unentschieden():
            messagebox.showinfo("😐 Unentschieden", "Keiner hat gewonnen.")
            self.deaktiviere_alle()
            return

        self.spieler = "O" if self.spieler == "X" else "X"
        self.info_label.config(text=f"Spieler: {self.spieler}")

        if self.spielmodus == "KI" and self.spieler == "O":
            self.master.after(300, self.ki_zug)

    def setze_zeichen(self, i, j, sp):
        self.felder[i][j] = sp
        self.buttons[i][j].config(text=sp, state="disabled")

    def check_sieg(self, sp):
        for i in range(3):
            if all(self.felder[i][j] == sp for j in range(3)) or \
               all(self.felder[j][i] == sp for j in range(3)):
                return True
        if all(self.felder[i][i] == sp for i in range(3)) or \
           all(self.felder[i][2 - i] == sp for i in range(3)):
            return True
        return False

    def unentschieden(self):
        return all(self.felder[i][j] != "" for i in range(3) for j in range(3))

    def deaktiviere_alle(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

    def neustart(self):
        self.spieler = "X"
        self.info_label.config(text="Spieler: X")
        for i in range(3):
            for j in range(3):
                self.felder[i][j] = ""
                self.buttons[i][j].config(text="", state="normal", bg="SystemButtonFace")

    def zeige_animation(self, i, j):
        for row in self.buttons:
            for btn in row:
                btn.config(bg="lightgreen")
        self.master.after(600, lambda: [btn.config(bg="SystemButtonFace") for row in self.buttons for btn in row])

    def ki_zug(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.felder[i][j] == "":
                    self.felder[i][j] = "O"
                    score = self.minimax(0, False)
                    self.felder[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.klick(*best_move)

    def minimax(self, tiefe, ist_max):
        if self.check_sieg("O"):
            return 1
        elif self.check_sieg("X"):
            return -1
        elif self.unentschieden():
            return 0

        if ist_max:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.felder[i][j] == "":
                        self.felder[i][j] = "O"
                        score = self.minimax(tiefe + 1, False)
                        self.felder[i][j] = ""
                        best = max(score, best)
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.felder[i][j] == "":
                        self.felder[i][j] = "X"
                        score = self.minimax(tiefe + 1, True)
                        self.felder[i][j] = ""
                        best = min(score, best)
            return best

# Start
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
