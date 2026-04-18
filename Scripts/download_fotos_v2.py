#!/usr/bin/env python3
"""
Image Scraper & Folder Architect (v2 - WordPress Optimized)
Scrapes all images from WordPress sites including lazy-loaded images
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

# ============================================================================
# CONFIGURATIE
# ============================================================================

BASE_URL = "https://4seasonscleaning.be"
TARGET_BASE_DIR = os.path.expanduser("~/documents/ai_projects/mojowebdesign/projects/4seasons/fotos")

# Pagina's om te scrapen (automatisch aangevuld met sitemap)
PAGES_TO_SCRAPE = [
    "/",
    "/over-ons/",
    "/diensten/",
    "/contact/",
]

# Ondersteunde afbeeldingsformaten
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif'}

# Headers voor requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
    folder_name = url_path.strip("/").replace("/", "_").replace("-", "_")
    return folder_name if folder_name else "home"

def is_valid_image_url(url):
    """Controleer of een URL naar een afbeelding verwijst"""
    try:
        if not url or not isinstance(url, str):
            return False
        parsed_url = url.lower().split('?')[0]  # Verwijder query params
        for ext in ALLOWED_EXTENSIONS:
            if parsed_url.endswith(ext):
                return True
        return False
    except:
        return False

def extract_images_from_page(page_url, output_dir):
    """Scrape ALLE afbeeldingen van een pagina (src, data-src, CSS backgrounds)"""
    full_url = urljoin(BASE_URL, page_url)
    downloaded_count = 0
    found_urls = set()  # Voorkomen van duplicaten

    try:
        print(f"\n📄 Verwerken: {full_url}")
        response = requests.get(full_url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # ─── METHOD 1: Gewone img src atributen ───
        img_tags = soup.find_all('img')
        print(f"   → Normale img tags: {len(img_tags)}")

        for img in img_tags:
            src = img.get('src')
            if src and is_valid_image_url(src):
                found_urls.add(urljoin(BASE_URL, src))

        # ─── METHOD 2: Lazy-loaded afbeeldingen (data-src) ───
        lazy_images = soup.find_all('img', {'data-src': True})
        print(f"   → Lazy-loaded (data-src): {len(lazy_images)}")

        for img in lazy_images:
            data_src = img.get('data-src')
            if data_src and is_valid_image_url(data_src):
                found_urls.add(urljoin(BASE_URL, data_src))

        # ─── METHOD 3: Picture elements (responsive images) ───
        picture_tags = soup.find_all('picture')
        print(f"   → Picture tags: {len(picture_tags)}")

        for picture in picture_tags:
            # Check source tags in picture
            sources = picture.find_all('source')
            for source in sources:
                srcset = source.get('srcset')
                if srcset:
                    # srcset kan meerdere URLs bevatten (bijv: "img1.jpg 1x, img2.jpg 2x")
                    urls = re.findall(r'(https?://[^\s,]+|/[^\s,]+\.(?:jpg|jpeg|png|webp|gif|svg))', srcset)
                    for url in urls:
                        url = url.split()[0]  # Verwijder size descriptors
                        if is_valid_image_url(url):
                            found_urls.add(urljoin(BASE_URL, url))

            # Check img in picture
            img = picture.find('img')
            if img:
                src = img.get('src')
                if src and is_valid_image_url(src):
                    found_urls.add(urljoin(BASE_URL, src))

        # ─── METHOD 4: Achtergrondafbeeldingen uit style atributen ───
        styled_elements = soup.find_all(style=re.compile(r'background.*url'))
        print(f"   → Elementen met background-image: {len(styled_elements)}")

        for element in styled_elements:
            style = element.get('style', '')
            # Zoek naar url(...) in style
            urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', style)
            for url in urls:
                if is_valid_image_url(url):
                    found_urls.add(urljoin(BASE_URL, url))

        # ─── METHOD 5: Srcset atributen (responsive images) ───
        responsive_imgs = soup.find_all('img', {'srcset': True})
        print(f"   → Responsive images (srcset): {len(responsive_imgs)}")

        for img in responsive_imgs:
            srcset = img.get('srcset')
            if srcset:
                # Parse srcset (formaat: "url1 1w, url2 2w, ...")
                urls = re.findall(r'(https?://[^\s,]+|/[^\s,]+\.(?:jpg|jpeg|png|webp|gif|svg))', srcset)
                for url in urls:
                    url = url.split()[0]
                    if is_valid_image_url(url):
                        found_urls.add(urljoin(BASE_URL, url))

        # ─── METHOD 6: iFrame en Video posters ───
        videos = soup.find_all(['video', 'source'])
        for video in videos:
            poster = video.get('poster')
            if poster and is_valid_image_url(poster):
                found_urls.add(urljoin(BASE_URL, poster))

        print(f"   → Totaal unieke afbeeldingen gevonden: {len(found_urls)}")

        # Download alle gevonden afbeeldingen
        for idx, img_url in enumerate(sorted(found_urls), 1):
            try:
                download_image(img_url, output_dir, idx)
                downloaded_count += 1
            except Exception as e:
                print(f"   ✗ Fout: {os.path.basename(img_url)} - {str(e)[:50]}")

    except requests.exceptions.Timeout:
        print(f"   ✗ Timeout - pagina laadt te langzaam")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Fout bij ophalen pagina: {str(e)[:80]}")
    except Exception as e:
        print(f"   ✗ Onverwachte fout: {str(e)[:80]}")

    return downloaded_count

def download_image(img_url, output_dir, counter):
    """Download een enkele afbeelding met timeout"""
    try:
        # Bepaal bestandsextensie
        img_path = img_url.split('?')[0]
        ext = os.path.splitext(img_path)[1].lower()

        if not ext or ext not in ALLOWED_EXTENSIONS:
            # Probeer uit content-type header te bepalen
            ext = '.jpg'

        # Maak unieke bestandsnaam
        filename = f"foto_{counter:04d}{ext}"
        filepath = os.path.join(output_dir, filename)

        # Voorkomen duplicaten
        counter_offset = counter
        while os.path.exists(filepath):
            counter_offset += 1000
            filename = f"foto_{counter_offset:04d}{ext}"
            filepath = os.path.join(output_dir, filename)

        # Download met timeout
        response = requests.get(img_url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # Schrijf bestand
        with open(filepath, 'wb') as f:
            f.write(response.content)

        # Controleer of bestand minimale grootte heeft (> 1KB)
        if os.path.getsize(filepath) > 1024:
            print(f"   ✓ {filename} ({len(response.content) // 1024}KB)")
        else:
            os.remove(filepath)
            print(f"   ⚠ {filename} te klein, verwijderd")

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        raise Exception(str(e))

def find_sitemap_pages():
    """Probeer aanvullende pagina's uit sitemap te vinden"""
    additional_pages = []
    try:
        sitemap_url = urljoin(BASE_URL, "/sitemap.xml")
        response = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            urls = soup.find_all('loc')
            for url in urls:
                loc = url.text
                if BASE_URL in loc:
                    path = loc.replace(BASE_URL, '')
                    if path and path != '/' and not path.endswith('.xml'):
                        additional_pages.append(path)
            print(f"✓ Sitemap gevonden: {len(additional_pages)} extra pagina's")
            return additional_pages[:20]  # Limit naar 20
    except:
        pass
    return []

def main():
    """Hoofdfunctie"""
    print("=" * 75)
    print("🖼️  IMAGE SCRAPER v2 - WordPress Optimized")
    print("=" * 75)
    print(f"Bron: {BASE_URL}")
    print(f"Doel: {TARGET_BASE_DIR}")
    print("=" * 75)

    # Maak basismap aan
    create_folder_structure(TARGET_BASE_DIR)

    # Probeer aanvullende pagina's uit sitemap te vinden
    print("\n🔍 Sitemap zoeken...")
    sitemap_pages = find_sitemap_pages()

    # Combineer pagina's
    pages = PAGES_TO_SCRAPE + sitemap_pages

    total_downloaded = 0

    # Scrape elke pagina
    for idx, page in enumerate(pages, 1):
        # Bepaal mapnaam
        folder_name = get_page_folder_name(page)
        page_dir = os.path.join(TARGET_BASE_DIR, folder_name)

        # Maak pagina-specifieke map aan
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)

        # Scrape pagina
        print(f"\n[{idx}/{len(pages)}]", end="")
        downloaded = extract_images_from_page(page, page_dir)
        total_downloaded += downloaded

        # Respectvolle delay
        time.sleep(0.5)

    # Afrondingsbericht
    print("\n" + "=" * 75)
    if total_downloaded > 0:
        print(f"✓ KLAAR! {total_downloaded} afbeeldingen gedownload.")
        print(f"📂 Opgeslagen in: {TARGET_BASE_DIR}")
    else:
        print(f"⚠️  Geen afbeeldingen gevonden.")
        print(f"   → Probeer manueel pagina's toe te voegen in PAGES_TO_SCRAPE")
    print("=" * 75)

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
