import cv2, pytesseract, os, time
import numpy as np
from matplotlib import pyplot as plt
from tkinter import filedialog

# Koodi vormistas Maarek Vettik, kasutamaks põhiprogrammis optilise tekstituvastuse funktsioonina.
# Hetkel on kood proovijärgus
# OCR tuvastusega tegeleb: https://github.com/UB-Mannheim/tesseract/wiki
# Pildi töötlemisega tegeleb: https://github.com/opencv/opencv
# Visualiseerimisega tegeleb: matplotlib
## Alaprogrammi käivitusjuhend:
# 1. Installida järgmised teegid: numpy, opencv-python, matplotlib, pytesseract teek

# Soovitud pilt peaks asuma valitud kaustas
# Hetkeseisuga toimib kood teistmoodi olenevalt sellest, kas see on käivitatud kasutaja või teise programmi poolt

def tuvastus(kaust):
    global märksõnad
    märksõnad = set()
    try:
        for fail in os.listdir(kaust):
            if fail.lower().endswith((".jpg", ".jpeg", ".png")):
                
                pildi_nimi = fail.lower()
                pildi_aadress = kaust+"/"+pildi_nimi
                
                pilt = cv2.imdecode(np.fromfile(pildi_aadress, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                pilt_rgb = cv2.cvtColor(pilt, cv2.COLOR_BGR2RGB)
            
                # Otsib Tesseract-OCR kausta projektikaustast
                pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'
                ocr_tekst = pytesseract.image_to_string(pilt_rgb)

                # Otsib (hetkel prooviks järgmisi) märksõmu optiliselt tuvastatud tekstist
                print("Leitud märksõnad:\n")
                
                if "Ubuntu25" in ocr_tekst:
                    märksõnad.add("Ubuntu seade")
                    print("Ubuntu seade")
                if "maarek" in ocr_tekst:
                    märksõnad.add("Eesnimi")
                    print("Eesnimi")
                if "vettik" in ocr_tekst:
                    märksõnad.add("Perekonnanimi")
                    print("Perekonnanimi")
                if "VirtualBox" in ocr_tekst:
                    märksõnad.add("Virtuaalmasin")
                    print("Virtuaalmasin")
                
                
                # Käivitub ainult, kui programm on otseselt jooksutatud, mitte teise programmi kaudu alustatud
                if __name__ == "__main__":    
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
    except KeyboardInterrupt:
        print("Programm lõpetati")
                
            
# Käivitub ainult, kui programm on otseselt jooksutatud, mitte teise programmi kaudu alustatud
if __name__ == "__main__":
    sisend_kaust = filedialog.askdirectory()
    tuvastus(sisend_kaust)