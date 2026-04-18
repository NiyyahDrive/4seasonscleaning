# 🖼️ Image Scraper & Folder Architect - Instructies

## Wat doet dit script?

Dit Python-script scrapet automatisch **alle afbeeldingen** van `https://4seasonscleaning.be/` en organiseert ze in een lokale mappenstructuur:

```
fotos/
├── home/
│   ├── foto_001.jpg
│   ├── foto_002.png
│   └── ...
├── over_ons/
│   ├── foto_001.jpg
│   └── ...
├── diensten/
│   └── ...
└── contact/
    └── ...
```

**Opgeslagen in:** `~/documents/ai_projects/mojowebdesign/4seasons/fotos`

---

## Voorbereiding

### 1. Python installeren
Zorg dat Python 3.6+ geïnstalleerd is:
- **macOS/Linux:** Meestal voorgeïnstalleerd. Check met: `python3 --version`
- **Windows:** Download van https://www.python.org/downloads/

### 2. Benodigde libraries installeren

Open je **Terminal** (macOS/Linux) of **Command Prompt** (Windows) en voer uit:

```bash
pip install requests beautifulsoup4
```

**Wat installeert dit:**
- `requests` - Download webpagina's
- `beautifulsoup4` - Parse HTML om afbeeldingen te vinden

---

## Hoe je het script uitvoert

### Stap 1: Script opslaan
1. Sla het bestand `download_fotos.py` op je computer op
2. Herinner je waar je het hebt opgeslagen

### Stap 2: Terminal openen
- **macOS:** `Applications → Utilities → Terminal`
- **Windows:** `Win + R` → type `cmd` → Enter
- **Linux:** Open je terminal emulator

### Stap 3: Naar de juiste folder navigeren

```bash
cd /pad/naar/jouw/folder
```

Bijvoorbeeld:
```bash
cd ~/Desktop    # als het op je bureaublad staat
```

### Stap 4: Script starten

```bash
python download_fotos.py
```

Of op macOS/Linux:
```bash
python3 download_fotos.py
```

---

## Wat gebeurt er dan?

Het script:

1. ✓ Controleert of de doelmap bestaat (zo niet, maakt deze aan)
2. ✓ Bezoekt elke pagina op de website
3. ✓ Vindt alle afbeeldingen (`.jpg`, `.png`, `.webp`, `.svg`)
4. ✓ Downloadt ze met duidelijke nummers (`foto_001.jpg`, `foto_002.jpg`, etc.)
5. ✓ Organiseert alles in submappen per pagina

**Output ziet er zo uit:**
```
📄 Verwerken: https://4seasonscleaning.be/
   → Gevonden: 12 afbeeldingen
   ✓ foto_001.jpg
   ✓ foto_002.png
   ✓ foto_003.webp
   ...
✓ KLAAR! 47 afbeeldingen gedownload.
```

---

## Aanpassingen maken

### Meer pagina's toevoegen
Open `download_fotos.py` en pas dit aan:

```python
PAGES_TO_SCRAPE = [
    "/",
    "/over-ons/",
    "/diensten/",
    "/contact/",
    "/blog/",
    "/portfolio/",  # Nieuwe pagina toevoegen
]
```

### Doelmap wijzigen
Pas dit aan in het script:

```python
TARGET_BASE_DIR = os.path.expanduser("~/mijn-eigen-pad/fotos")
```

### Andere bestandsformaten toevoegen
Pas dit aan:

```python
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif'}
```

---

## Probleemoplossing

### ❌ "ModuleNotFoundError: No module named 'requests'"
**Oplossing:** Libraries nog niet geïnstalleerd. Voer uit:
```bash
pip install requests beautifulsoup4
```

### ❌ Script lijkt vast te lopen
**Oplossing:** Wacht geduldig. Grote websites kunnen enkele minuten duren. Je ziet voortgang in je terminal.

### ❌ Geen afbeeldingen gedownload
**Mogelijke oorzaken:**
1. Website structuur is anders → Voeg pagina's handmatig toe in `PAGES_TO_SCRAPE`
2. Afbeeldingen laden dynamisch → Script ziet deze niet (JavaScript-afhankelijk)
3. Website blokkert downloads → Voeg delay toe in script

### ❌ Foutmelding over pad
**Oplossing:** Zorg dat het pad bestaat. Handmatig aanmaken:
```bash
mkdir -p ~/documents/ai_projects/mojowebdesign/4seasons/fotos
```

---

## Tips & Best Practices

✓ **Eerst testen:** Run script op één pagina als test  
✓ **Respecteer servers:** Script heeft pauzes ingebouwd (1 sec tussen pagina's)  
✓ **Grote downloads:** Voor sites met veel afbeeldingen → kan 5-10 minuten duren  
✓ **Duplicaten voorkomen:** Script voegt automatisch nummers toe  

---

## Licentie & Verantwoordelijkheid

Dit script is gemaakt voor persoonlijk gebruik. Zorg dat je:
- Het recht hebt om afbeeldingen te downloaden
- De afbeeldingen niet zonder toestemming commercieel gebruikt
- De website niet overbelast met requests

---

**Vragen?** Controleer het script of open het in een tekstverwerker voor meer uitleg!
