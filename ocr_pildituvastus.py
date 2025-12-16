import cv2, pytesseract, os, shutil
import numpy as np
from transformers import pipeline
from tkinter import filedialog

# Koodi vormistas Maarek Vettik, kasutamaks põhiprogrammis optilise tekstituvastuse funktsioonina.
# OCR tuvastusega tegeleb: https://github.com/UB-Mannheim/tesseract/wiki
# Pildi töötlemisega tegeleb: https://github.com/opencv/opencv
# Kasutuses olev NLP mudel: https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli

## Alaprogrammi käivitusjuhend:
# 1. Installida järgmised teegid: numpy, opencv-python, pytesseract, transformers teek

# Soovitud pilt peaks asuma valitud kaustas
# Hetkeseisuga toimib kood teistmoodi olenevalt sellest, kas see on käivitatud kasutaja või teise programmi poolt

# Laeb NLP mudeli 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli', mis mõistab ka eesti keelt
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", framework="pt")

def tuvastus_nlp(kaust):

    
    # Defineeritud kategooriad, mida mudel tuvastaks
    siht_kategooriad = ["arvutitehnika", "isiklikud andmed", "õppematerjalid",
                        "veateated", "küsimus", "matemaatika", "virtuaalmasin", "operatsioonisüsteem"]

    for fail in os.listdir(kaust):
        if fail.lower().endswith((".jpg", ".jpeg", ".png")):
            pildi_tee = os.path.join(kaust, fail)
            # Otsib Tesseract-OCR kausta projektikaustast
            pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'

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

            # Faili liigutamine
            siht_kaust = os.path.join((kaust+"/Sorteeritud_pildid"), parim_vaste)
            os.makedirs(siht_kaust, exist_ok=True)
            shutil.copy(pildi_tee, os.path.join(siht_kaust, fail))


# Kui programm on käivitatud põhiprogrammina, mitte alaprogrammina
if __name__ == "__main__":
    valitud_kaust = filedialog.askdirectory()
    if valitud_kaust:
        tuvastus_nlp(valitud_kaust)
