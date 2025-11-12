import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract

# Koodi vormistas Maarek Vettik, kasutamaks põhiprogrammis optilise tekstituvastuse funktsioonina.
# Hetkel on kood proovijärgus
# OCR tuvastusega tegeleb: https://github.com/UB-Mannheim/tesseract/wiki
# Pildi töötlemisega tegeleb: https://github.com/opencv/opencv
# Visualiseerimisega tegeleb: matplotlib
## Alaprogrammi käivitusjuhend:
# 1. Installida järgmised teegid: numpy, opencv-python, matplotlib, pytesseract teek
# 2. Lisaks oleks vaja installida ka tesseract ise, https://github.com/UB-Mannheim/tesseract/wiki lingil on leitav windows installer
# vaikimisi installikaust oleks 'C:\Program Files\Tesseract-OCR\', kui programm mujale paigutada, tuleks seda programmile öelda, sest vale aadress põhjustab katkestuse

# Soovitud pilt peaks (hetkeseisuga) asuma samas kaustas, kui programm. Pildi nimi sisestada koos laiendusega, näiteks pilt.jpg.


while True:
    pildi_nimi = str(input("Sisesta pilt: "))
    
    
    # Lõpetab tsükli, kui kasutaja ei sisesta midagi
    if pildi_nimi == "":
        break
    
    else:
        pilt = cv2.imread(pildi_nimi)
        pilt_rgb = cv2.cvtColor(pilt, cv2.COLOR_BGR2RGB)
        hall_ver = cv2.cvtColor(pilt, cv2.COLOR_BGR2GRAY)
        
        # Kui pytesseract.exe asub kaustas 'C:\Program Files\Tesseract-OCR\tesseract.exe'. Kui ei asu, tuleb seda muuta.
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            ocr_tekst = pytesseract.image_to_string(pilt_rgb)
        except:
            vastus = str(input("Tesseract.exe polnud vaikeaadressil leitav, palun täpsusta aadress: ")+"\\tesseract.exe")
            pytesseract.pytesseract.tesseract_cmd = vastus
            ocr_tekst = pytesseract.image_to_string(pilt_rgb)
        
        # Otsib (hetkel prooviks järgmisi) märksõmu optiliselt tuvastatud tekstist

        print("Leitud märksõnad:\n")
        
        if "Ubuntu25" in ocr_tekst:
            print("Ubuntu seade")
        if "maarek" in ocr_tekst:
            print("Eesnimi")
        if "vettik" in ocr_tekst:
            print("Perekonnanimi")
        if "VirtualBox" in ocr_tekst:
            print("Virtuaalmasin")
        
        ### Uurimaks, mida programm kindlal pildil vaatab (lõppversioonis puudub)
        andmed = pytesseract.image_to_data(pilt_rgb, output_type=pytesseract.Output.DICT)

        n_kasti = len(andmed['level'])
        for i in range(n_kasti):
            (x, y, w, h) = (andmed['left'][i], andmed['top'][i], andmed['width'][i], andmed['height'][i])
            cv2.rectangle(pilt_rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        plt.figure(figsize=(10, 6))
        plt.imshow(pilt_rgb)
        plt.title("Punase kastiga märgitud alad, mida programm kontrollib")
        plt.axis("off")
        plt.show()
        ###