import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
import ocr_pildituvastus as ocr
import os
import threading, sys
import värvi_järgi_sorteerimine as vjs

raam = tk.Tk()

raam.geometry("400x400")
raam.title("Programm")

def failitee_valimine():
    global failitee
    failitee = filedialog.askdirectory()
    sisend_kast.config(text = failitee)
    
def lõim_sisu():
    global pilt_tk
    global failitee
    ocr.tuvastus_nlp(failitee)
    väljund_kast = tk.Label(raam, text="Väljund..", bg="#E0E0E0")
    väljund_kast.place(relx=0.5, rely=0.5, anchor="center")

def lõim_värv():
    global failitee
    vjs.tuvastus(failitee)
            
def lõim_kontroll(t):
    if not t.is_alive():
        progress.stop()
        sule_nupp.config(state=tk.NORMAL)
    else:
        ajasta_kontroll(t)
        

def ajasta_kontroll(t):
    raam.after(1000, lõim_kontroll, t)
    
def algus_sisu():
    progress.start()
    sule_nupp.config(state=tk.DISABLED)
    t = threading.Thread(target=lõim_sisu)
    t.start()
    ajasta_kontroll(t)
    
def algus_värv():
    progress.start()
    sule_nupp.config(state=tk.DISABLED)
    t = threading.Thread(target=lõim_värv)
    t.start()
    ajasta_kontroll(t)

def Sule():
    raam.destroy()

tk.Label(raam, text="Failitee").grid(row=0)

sisend_kast = tk.Label(raam, width=40, text="C:/", bg="#E0E0E0", anchor="w")
sisend_kast.grid(row=0, column=1)

tk.Button(raam, 
          text='Vali failitee', 
          command=failitee_valimine).grid(row=3, column=0,
                                          sticky="NSEW")
alusta_nupp_sisu = tk.Button(raam, 
          text='Alusta sorteerimist sisu järgi', 
          command=algus_sisu).grid(row=4, column=0,
                                          sticky="NSEW")
alusta_nupp_värv = tk.Button(raam, 
          text='Alusta sorteerimist värvi järgi', 
          command=algus_värv).grid(row=4, column=1,
                                          sticky="NSEW")

sule_nupp = tk.Button(raam, 
          text='Sulge', 
          command=Sule)
sule_nupp.grid(row=5, column=0,sticky="NSEW")

progress = tk.ttk.Progressbar(orient=tk.HORIZONTAL, length=160, mode="indeterminate")
progress.place(relx=0.5, rely=0.9, anchor="center")


raam.mainloop()

