import cv2, pytesseract, os, shutil, sys
import numpy as np
from transformers import pipeline
from tkinter import filedialog, messagebox, Tk, Label


## Versioon mis muudab natuke paigutust, et oleks võimalik PyInstalleriga luua .exe versioon

# Koodi vormistas Maarek Vettik, kasutamaks põhiprogrammis optilise tekstituvastuse funktsioonina.
# OCR tuvastusega tegeleb: https://github.com/UB-Mannheim/tesseract/wiki
# Pildi töötlemisega tegeleb: https://github.com/opencv/opencv
# Kasutuses olev NLP mudel: https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli

## Alaprogrammi käivitusjuhend:
# 1. Installida järgmised teegid: numpy, opencv-python, pytesseract, transformers, torch teek

# Soovitud pilt peaks asuma valitud kaustas
# Hetkeseisuga toimib kood teistmoodi olenevalt sellest, kas see on käivitatud kasutaja või teise programmi poolt

## Abikood, mis suunab PyInstalleri poolt loodud temp kausta poole
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def tuvastus_nlp(kaust):
    if __name__ != "__main__":
        # Loob infoakna kasutaja jaoks, et anda teada tööst 
        splash = Tk()
        splash.title("Laadimine")
        splash.geometry("300x100")
        Label(splash, text="Palun oota, laen teeke ja NLP mudelit...", pady=20).pack()
        splash.update() # Displays the window immediately

    
    # Defineeritud kategooriad, mida mudel tuvastaks
    siht_kategooriad = ["arvutitehnika", "isiklikud andmed", "õppematerjalid",
                        "veateated", "küsimus", "matemaatika", "virtuaalmasin", "operatsioonisüsteem"]
    
    ## Aitab muuta tesseracti asukoha õigeks
    tesseract_dir = resource_path('Tesseract-OCR')
    pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_dir, 'tesseract.exe')
    
    ## Vajalik, et Tesseract leiaks TESSDATA infot
    os.environ['TESSDATA_PREFIX'] = os.path.join(tesseract_dir, 'tessdata')
    
    # Laeb NLP mudeli 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli' alla, mis mõistab ka eesti keelt
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", framework="pt")
    
    if __name__ != "__main__":
        # Sulgeb akna, kui mudel on laetud
        splash.destroy()

    for fail in os.listdir(kaust):
        if fail.lower().endswith((".jpg", ".jpeg", ".png")):
            pildi_tee = os.path.join(kaust, fail)

            pilt = cv2.imdecode(np.fromfile(pildi_tee, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            # Loeb teksti
            ocr_tekst = pytesseract.image_to_string(pilt).strip()

            if not ocr_tekst:
                print(f"Failis {fail} teksti ei leitud. Jätan vahele.")
                continue

            # Mudel võrdleb teksti antud kategooriatega
            tulemus = classifier(ocr_tekst, candidate_labels=siht_kategooriad)
            
            # Kõige suurema tõenäosusega kategooria
            parim_vaste = tulemus['labels'][0]
            tõenäosus = tulemus['scores'][0]

            print(f"Fail: {fail} | Kategooria: {parim_vaste} ({round(tõenäosus*100, 1)}%)")

            # Faili kopeerimine
            siht_kaust = os.path.join((kaust+"/Sorteeritud_pildid/Sisu järgi"), parim_vaste)
            os.makedirs(siht_kaust, exist_ok=True)
            shutil.copy(pildi_tee, os.path.join(siht_kaust, fail))
            
    print("Kõik pildid on sorteeritud!")
    
# Kui programm on käivitatud põhiprogrammina, mitte alaprogrammina
if __name__ == "__main__":
    valitud_kaust = filedialog.askdirectory()
    if valitud_kaust:
        tuvastus_nlp(valitud_kaust)