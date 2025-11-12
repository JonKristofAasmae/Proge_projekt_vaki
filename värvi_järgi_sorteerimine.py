#Koodi kirjutas Jon Kristof Aasmäe
#Praegune lahendus võtab talle ette antud kausta ja sorteerib selle uude kausta.
#Uues kaustas on ta sorteeritud järgmistesse kaustadesse värvide järgi.
#Praegune kood on veel algeline ja pole veel nii täpne kui võiks olla.
import os
import shutil
import numpy as np
from PIL import Image

# Kaust, kus pildid asuvad
Lähtekaust = "Screenshots"
#Kaust, kuhu pildid sorteeritakse
Sihtkaust = "Sorteeritud_pildid"    
#Kontrollib kas kaust kuhu sorteerin on loodud ja kui ei ole siis teeb selle kausta
os.makedirs(Sihtkaust, exist_ok=True)

#Tagastab pildi keskmise RGB ja heleduse
def keskmine_varv(failitee):
    with Image.open(failitee) as img:
        img = img.convert("RGB")
        arr = np.array(img)
        keskmine = arr.mean(axis=(0, 1))
        r, g, b = keskmine
        heledus = (r + g + b) / 3
    return r, g, b, heledus

#Otsustab, mis värviga tegu on
def värvi_kategooria(r, g, b, heledus):
    if heledus < 60:
        return "must"
    elif heledus > 190:
        return "valge"
    elif abs(r - g) < 15 and abs(g - b) < 15:
        return "hall"
    elif r > g and r > b:
        return "punane"
    elif b > r and b > g:
        return "sinine"
    else:
        return "muu"
    
#Käib kõik kaustas olevad pildid läbi
for fail in os.listdir(Lähtekaust):
    if fail.lower().endswith((".jpg", ".jpeg", ".png")):
        tee = os.path.join(Lähtekaust, fail)
        r, g, b, heledus = keskmine_varv(tee)
        värv = värvi_kategooria(r, g, b, heledus)

        # Loob uue sihtkausta kui vaja
        siht = os.path.join(Sihtkaust, värv)
        os.makedirs(siht, exist_ok=True)

        # Kopeerib faili
        shutil.copy(tee, siht)
        print(f"{fail} on {värv} (RGB: {r:.0f}, {g:.0f}, {b:.0f}, heledus: {heledus:.0f})")

print("Kõik pildid on sorteeritud!")
 
