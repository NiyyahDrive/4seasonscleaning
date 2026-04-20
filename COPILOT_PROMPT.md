# Copilot-prompt: 4Seasons hamburger-menu fix + nav-consistentie

> Plak de inhoud hieronder letterlijk in de Copilot Chat in je IDE, met de repo `4Seasons` geopend.
> Lees de prompt eerst zelf door voor je Copilot laat beginnen.

---

## ROL

Je bent een Senior Frontend Developer. Je werkt in de lokale Git-repo `4Seasons` (statische site, HTML/CSS/JS, GitHub Pages). Je voert een exact gedefinieerde reeks wijzigingen uit. Je **interpreteert niet**, je **improviseert niet**, je **voegt niets extra toe**. Je bevestigt per stap voordat je verder gaat.

## WERKREGELS

1. Werk op een nieuwe branch: `fix/nav-hamburger-consistency`.
2. Na elke stap: toon `git status` en `git diff --stat` en wacht op "OK".
3. Verander **niets** buiten de hieronder genoemde bestanden en regels.
4. Gebruik geen `git add -A` of `git add .` — alleen expliciete bestandspaden.
5. Push pas nadat ik expliciet "push" zeg.
6. Pre-commit-hooks niet skippen (`--no-verify` verboden).

## DOEL

De hamburger-menu werkt niet op subpagina's. Oorzaak: drie duplicate CSS-definities (`style.css` + `responsive.css`), ontbrekend `main.js` op één pagina, en inconsistente nav-markup. Alles rechttrekken zonder bestaande layout elders te breken.

---

## STAP 0 — Pre-flight

Voer uit en toon de output:

```bash
git status
git branch --show-current
git checkout -b fix/nav-hamburger-consistency
```

Stop hier. Wacht op "OK".

---

## STAP 1 — Verwijder duplicate nav-CSS in `css/style.css`

Zoek in `css/style.css` het block dat begint met:

```
/* Simple nav structure */
nav {
```

Dit block loopt door tot vlak vóór:

```
/* ================================================
   BREADCRUMB
   ================================================ */
```

Verwijder het volledige block tussen die twee markers. Het bevat deze selectors die verwijderd moeten worden:
- `nav { ... }` (zonder class)
- `nav .logo { ... }` en `nav .logo img { ... }`
- `.nav-links` (de tweede, oudere versie)
- `.nav-links li`, `.nav-links a`, `.nav-links a:hover`
- `.hamburger`, `.hamburger span`, `.hamburger.active span:nth-child(1/2/3)` (de tweede versie)
- `.mobile-menu-toggle` en `.mobile-menu-toggle span`

**Laat het eerste block op regel ~148 (`/* ================================================ NAVIGATION... */`) intact.** Dat is de correcte moderne versie.

Na bewerking: toon `git diff --stat css/style.css`. Verwacht ongeveer `-104 regels`. Stop. Wacht op "OK".

---

## STAP 2 — Verwijder duplicate hamburger-CSS in `css/responsive.css`

Zoek in `css/responsive.css` het block `/* ===== HAMBURGER MENU STYLES ===== */`.

Verwijder het volledige block vanaf die comment tot het punt vóór de volgende niet-nav-gerelateerde sectie. Concreet: alle CSS die `.hamburger`, `nav.active`, `.navbar-menu.active` definieert met `!important`-flags.

Laat andere responsive breakpoints (hero, grids, form-styling) onaangeroerd.

Na bewerking: `git diff --stat css/responsive.css` tonen (~160 regels verwijderd). Stop. Wacht op "OK".

---

## STAP 3 — Voeg `main.js` toe aan `pages/realisaties.html`

In `pages/realisaties.html`, zoek de regel:

```html
    <script src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"></script>
```

Voeg DIRECT DAARBOVEN één nieuwe regel toe:

```html
    <script src="../js/main.js"></script>
```

Controleer dat `main.js` daarna slechts één keer voorkomt in dit bestand:

```bash
grep -c "main.js" pages/realisaties.html
```

Moet `1` opleveren. Zo niet: dubbele verwijderen. Stop. Wacht op "OK".

---

## STAP 4 — Uniformeer nav-markup op subpagina's

Op `pages/over-ons.html`, `pages/privacy.html`, `pages/terms.html`, `pages/contact.html`:

Vervang de volledige `<nav>...</nav>` (of bestaande `<header class="nav">...</header>`) block direct na `<body>` met **exact** deze markup:

```html
<header class="nav">
    <div class="nav__inner">
        <a href="../index.html" class="logo" aria-label="4 Seasons Cleaning">
            <img src="../assets/images/logo.png" alt="4 Seasons Window Cleaning Logo">
        </a>
        <button class="hamburger" id="menuToggle" aria-label="Menu openen" aria-expanded="false" aria-controls="navMenu">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-links" id="navMenu">
            <li><a href="../index.html#diensten">Diensten</a></li>
            <li><a href="../index.html#waarom">Waarom ons</a></li>
            <li><a href="../index.html#reviews">Reviews</a></li>
            <li><a href="realisaties.html">Realisaties</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="contact.html" class="btn-nav">Offerte</a></li>
        </ul>
    </div>
</header>
```

Bevestig dat elke pagina daarna `../js/main.js` laadt in een `<script>`-tag vóór `</body>`. Als ontbrekend: toevoegen.

Na bewerking per bestand: `git diff --stat pages/<bestand>.html`. Stop na alle vier. Wacht op "OK".

---

## STAP 5 — Upgrade `js/main.js` (functie `initMobileMenu`)

In `js/main.js`, vervang de volledige functie `initMobileMenu()` door:

```js
function initMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    const nav = document.querySelector('.nav');

    if (!menuToggle || !navMenu) return;

    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = navMenu.classList.toggle('active');
        menuToggle.classList.toggle('active', isOpen);
        menuToggle.setAttribute('aria-expanded', isOpen);
    });

    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', false);
        });
    });

    document.addEventListener('click', function(event) {
        if (nav && !nav.contains(event.target) && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', false);
        }
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 860) {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', false);
        }
    });
}
```

Raak de rest van `main.js` (seasonal theme, contactForm, smoothScroll, scrollAnimations, tracking) **niet** aan.

Toon `git diff js/main.js`. Stop. Wacht op "OK".

---

## STAP 6 — Breid `.gitignore` uit

Voeg aan het einde van `.gitignore` toe:

```
*.bak
assets/images-backup/
Scripts/li-salaam-2026/
```

Stop. Wacht op "OK".

---

## STAP 7 — Lokale test voordat we committen

1. Open `pages/realisaties.html` in de browser.
2. Verklein venster tot < 860 px breed.
3. Verifieer: hamburger-icoon zichtbaar rechtsboven, klik opent/sluit menu, klik op link navigeert en sluit menu.
4. Herhaal voor `pages/contact.html`, `pages/over-ons.html`, `pages/privacy.html`, `pages/terms.html`, `index.html`.
5. Desktop-breedte > 860 px: hamburger onzichtbaar, horizontale nav zichtbaar.

Rapporteer resultaat per pagina (OK / niet-OK). Als niet-OK: STOP, escaleer naar mij, niet zelf fixen.

---

## STAP 8 — Commit-strategie (gegroepeerd)

Voer pas uit na "GO" van mij:

```bash
# Commit 1: code-fix
git add css/style.css css/responsive.css js/main.js \
        pages/realisaties.html pages/contact.html pages/over-ons.html \
        pages/privacy.html pages/terms.html .gitignore
git commit -m "Fix: hamburger-menu werkt op alle paginas + nav-consistentie

- Verwijder 3 duplicate hamburger CSS-blocks (style.css + responsive.css)
- Uniformeer nav-markup naar <header class='nav'> op alle subpaginas
- Voeg main.js toe aan realisaties.html
- Moderniseer initMobileMenu: aria-expanded, resize-handler, klik-buiten
- Gitignore: *.bak, images-backup, li-salaam-2026"

# Commit 2: geoptimaliseerde afbeeldingen (grote payload, apart)
git add assets/images-optimized/
git commit -m "Assets: add optimized responsive images (avif/webp/jpg, 160-380w)"
```

Toon `git log --oneline -5`. Stop. Wacht op "PUSH".

---

## STAP 9 — Push

```bash
git push -u origin fix/nav-hamburger-consistency
```

Toon de output inclusief PR-URL als die verschijnt. **Niet** automatisch een PR aanmaken — dat doe ik zelf.

---

## WAT NIET TE DOEN

- `index.html` in deze PR **niet** wijzigen (aparte designkeuze over logo-tekst).
- `instructions.md` niet committen zonder mijn OK.
- Geen nieuwe dependencies, geen build-tools, geen frameworks.
- Geen "while I'm here" refactors van andere CSS/HTML.
- Geen auto-formatting van hele bestanden (whitespace-only diffs vertroebelen de review).

## ROLLBACK (als iets stuk gaat)

```bash
git checkout main
git branch -D fix/nav-hamburger-consistency
# niets gepusht = niets verloren
```

---

**Bevestig dat je deze instructies begrijpt. Start dan bij STAP 0 en wacht na elke stap op "OK".**
