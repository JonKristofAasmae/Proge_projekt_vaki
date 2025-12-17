import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
import ocr_pildituvastus as ocr ## Impordib pildituvastaja alaprogrammina
import os, threading, sys 
import värvi_järgi_sorteerimine as vjs ## Impordib värvituvastaja alaprogrammina

raam = tk.Tk()

raam.geometry("400x400")
raam.title("Pildisorteerija")

# Funktsioon failitee/kausta valimiseks
def failitee_valimine():
    global failitee
    failitee = filedialog.askdirectory()
    sisend_kast.config(text = failitee)

# Sisu järgi sorteerimise lõim (thread)
def lõim_sisu():
    global pilt_tk
    global failitee
    ocr.tuvastus_nlp(failitee)
    väljund_kast.config(text = "Valmis")
    alusta_nupp_värv.config(state=tk.NORMAL)

# Värvi järgi sorteerimise lõim (thread)
def lõim_värv():
    global failitee
    vjs.tuvastus(failitee)
    väljund_kast.config(text = "Valmis")
    alusta_nupp_sisu.config(state=tk.NORMAL)

# Kontroll, kas lõim on aktiivne või mitte
def lõim_kontroll(t):
    if not t.is_alive():
        progress.stop()
        sule_nupp.config(state=tk.NORMAL)
    else:
        ajasta_kontroll(t)


def ajasta_kontroll(t):
    raam.after(1000, lõim_kontroll, t)

# Funktsioon, mis käivitub kui vajutada nuppu "Alusta sorteerimist sisu järgi"
def algus_sisu():
    progress.start()
    väljund_kast.config(text = "Töötamine..")
    sule_nupp.config(state=tk.DISABLED)
    alusta_nupp_värv.config(state=tk.DISABLED)
    t = threading.Thread(target=lõim_sisu)
    t.start()
    ajasta_kontroll(t)

# Funktsioon, mis käivitub kui vajutada nuppu "Alusta sorteerimist värvi järgi"
def algus_värv():
    progress.start()
    väljund_kast.config(text = "Töötamine..")
    sule_nupp.config(state=tk.DISABLED)
    alusta_nupp_sisu.config(state=tk.DISABLED)
    t = threading.Thread(target=lõim_värv)
    t.start()
    ajasta_kontroll(t)

# Funktsioon, mis käivitub, kui vajutada nuppu "Sulge"
def Sule():
    raam.destroy()

tk.Label(raam, text="Failitee").grid(row=0)

sisend_kast = tk.Label(raam, width=40, text="C:/", bg="#E0E0E0", anchor="w")
sisend_kast.grid(row=0, column=1)

tk.Button(raam, text='Vali failitee', command=failitee_valimine).grid(row=3, column=0,sticky="NSEW")

alusta_nupp_sisu = tk.Button(raam, text='Alusta sorteerimist sisu järgi', command=algus_sisu)
alusta_nupp_sisu.grid(row=4, column=0,sticky="NSEW")

alusta_nupp_värv = tk.Button(raam, text='Alusta sorteerimist värvi järgi', command=algus_värv)
alusta_nupp_värv.grid(row=4, column=1,sticky="NSEW")

sule_nupp = tk.Button(raam, text='Sulge', command=Sule)
sule_nupp.grid(row=5, column=0,sticky="NSEW")

väljund_kast = tk.Label(raam, text="...", bg="#E0E0E0")
väljund_kast.place(relx=0.5, rely=0.825, anchor="center")

# Progressiriba, mis liigub edasi-tagasi töö ajal näitamaks, et programm pole hangunud
progress = tk.ttk.Progressbar(orient=tk.HORIZONTAL, length=160, mode="indeterminate")
progress.place(relx=0.5, rely=0.9, anchor="center")


raam.mainloop()

