#!/usr/bin/env python3
"""
Image Scraper & Folder Architect
Scrapes all images from https://4seasonscleaning.be/ and organizes them locally
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
import time

# ============================================================================
# CONFIGURATIE
# ============================================================================

BASE_URL = "https://4seasonscleaning.be"
TARGET_BASE_DIR = os.path.expanduser("~/documents/ai_projects/mojowebdesign/4seasons/fotos")

# Pagina's om te scrapen (voeg meer toe als nodig)
PAGES_TO_SCRAPE = [
    "/",
    "/over-ons/",
    "/diensten/",
    "/contact/",
    "/blog/",
]

# Ondersteunde afbeeldingsformaten
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg'}

# Headers voor requests (om problemen met user-agent te voorkomen)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ============================================================================
# HELPER FUNCTIES
# ============================================================================

def create_folder_structure(base_dir):
    """Maak het basispad aan als het niet bestaat"""
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"✓ Basismap aangemaakt: {base_dir}")

def get_page_folder_name(url_path):
    """Zet een URL-path om naar een mapnaam"""
    if url_path == "/" or url_path == "":
        return "home"
    # Verwijder leading en trailing slashes
    folder_name = url_path.strip("/").replace("/", "_")
    return folder_name if folder_name else "home"

def is_valid_image_url(url):
    """Controleer of een URL naar een afbeelding verwijst"""
    try:
        parsed_url = url.lower()
        for ext in ALLOWED_EXTENSIONS:
            if parsed_url.endswith(ext):
                return True
        return False
    except:
        return False

def scrape_images_from_page(page_url, output_dir):
    """Scrape alle afbeeldingen van een pagina en download ze"""
    full_url = urljoin(BASE_URL, page_url)
    downloaded_count = 0

    try:
        print(f"\n📄 Verwerken: {full_url}")
        response = requests.get(full_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Vind alle img tags
        img_tags = soup.find_all('img')

        if not img_tags:
            print(f"   → Geen afbeeldingen gevonden")
            return downloaded_count

        print(f"   → Gevonden: {len(img_tags)} afbeeldingen")

        # Download afbeeldingen
        for idx, img in enumerate(img_tags, 1):
            img_url = img.get('src') or img.get('data-src')

            if not img_url:
                continue

            # Converteer relatieve URLs naar absolute URLs
            img_url = urljoin(BASE_URL, img_url)

            # Controleer of het een geldige afbeelding is
            if not is_valid_image_url(img_url):
                continue

            try:
                # Download de afbeelding
                download_image(img_url, output_dir, idx)
                downloaded_count += 1
            except Exception as e:
                print(f"   ✗ Fout bij download {img_url}: {str(e)}")
                continue

    except requests.exceptions.RequestException as e:
        print(f"   ✗ Fout bij ophalen pagina: {str(e)}")
    except Exception as e:
        print(f"   ✗ Onverwachte fout: {str(e)}")

    return downloaded_count

def download_image(img_url, output_dir, counter):
    """Download een enkele afbeelding"""
    try:
        # Bepaal bestandsextensie
        img_path = img_url.split('?')[0]  # Verwijder query parameters
        ext = os.path.splitext(img_path)[1].lower()

        # Fallback als extensie niet duidelijk is
        if not ext or ext not in ALLOWED_EXTENSIONS:
            ext = '.jpg'

        # Maak unieke bestandsnaam
        filename = f"foto_{counter:03d}{ext}"
        filepath = os.path.join(output_dir, filename)

        # Controleer of bestand al bestaat
        counter_offset = counter
        while os.path.exists(filepath):
            counter_offset += 1000
            filename = f"foto_{counter_offset:03d}{ext}"
            filepath = os.path.join(output_dir, filename)

        # Download afbeelding
        urlretrieve(img_url, filepath)
        print(f"   ✓ {filename}")

    except Exception as e:
        raise Exception(f"Download mislukt: {str(e)}")

def main():
    """Hoofdfunctie"""
    print("=" * 70)
    print("🖼️  IMAGE SCRAPER & FOLDER ARCHITECT")
    print("=" * 70)
    print(f"Bron: {BASE_URL}")
    print(f"Doel: {TARGET_BASE_DIR}")
    print("=" * 70)

    # Maak basismap aan
    create_folder_structure(TARGET_BASE_DIR)

    total_downloaded = 0

    # Scrape elke pagina
    for page in PAGES_TO_SCRAPE:
        # Bepaal mapnaam
        folder_name = get_page_folder_name(page)
        page_dir = os.path.join(TARGET_BASE_DIR, folder_name)

        # Maak pagina-specifieke map aan
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)

        # Scrape pagina
        downloaded = scrape_images_from_page(page, page_dir)
        total_downloaded += downloaded

        # Kleine delay tussen verzoeken (respect for server)
        time.sleep(1)

    # Afrondingsbericht
    print("\n" + "=" * 70)
    print(f"✓ KLAAR! {total_downloaded} afbeeldingen gedownload.")
    print(f"📂 Alle bestanden opgeslagen in:")
    print(f"   {TARGET_BASE_DIR}")
    print("=" * 70)

# ============================================================================
# UITVOERING
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Script gestopt door gebruiker.")
    except Exception as e:
        print(f"\n\n✗ Kritieke fout: {str(e)}")
