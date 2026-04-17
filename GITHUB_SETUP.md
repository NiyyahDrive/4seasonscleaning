# GitHub Push Instructions

## Stap 1: Maak een nieuwe repository op GitHub

1. Ga naar https://github.com/new
2. Repository name: `4Seasons-Website` (of naar keuze)
3. Beschrijving: "4 Seasons Glazenwasser - Professional cleaning services website"
4. Kies: **Public** (zodat klant kan zien)
5. Klik "Create repository"

## Stap 2: Voeg remote toe en push

In de terminal van je project folder:

```bash
# Replace USERNAME met jouw GitHub username
git remote add origin https://github.com/USERNAME/4Seasons-Website.git

# Push naar main branch
git branch -M main
git push -u origin main
```

## Stap 3: Share met klant

Geef klant deze link: `https://github.com/USERNAME/4Seasons-Website`

Klant kan dan:
- ✅ Alle files bekijken
- ✅ De HTML/CSS/JS controleren
- ✅ Feedback geven via Issues (GitHub Issues tab)
- ✅ Changes voorstellen

## Stap 4: Updates na feedback

Na client feedback, maak wijzigingen en:

```bash
# Voeg wijzigingen toe
git add .

# Commit met beschrijving
git commit -m "Update: [beschrijving van wijziging]"

# Push naar GitHub
git push origin main
```

## Stap 5: Deploy naar webserver

Eenmaal klant tevreden is:

```bash
# Pull laatste versie
git pull origin main

# Upload naar webserver (via FTP/SSH/hosting control panel)
# Zorg dat ALL files gekopieerd zijn:
# - index.html
# - pages/ folder
# - css/ folder
# - js/ folder
# - assets/ folder (met images)
```

## Handige GitHub features

- **Issues**: Klant kan bugs/requests toevoegen
- **Discussions**: Team kan overleggen
- **Wiki**: Documentatie toevoegen
- **Releases**: Versies taggen

---

**Pro tip:** Als je SSH key setup hebt, vervang `https://` met `git@github.com:` voor makkelijker pushen zonder wachtwoord.
