# 4Seasons Project - Autonomous Senior Architect Instructions

**Mode**: Autonomous Senior Architect  
**Project**: 4Seasons Window Cleaning Website  
**Tech Stack**: HTML, CSS, JavaScript (Vanilla)
**Parent Guide**: See `AUTONOMOUS_ARCHITECT_TEMPLATE.md` in parent directory  
**Established**: April 2026  

---

## Defaults for This Project

### Backup Strategy
- **Format**: Summary checklist (concise, efficient)
- **Git Strategy**: Feature branches for grouped multi-file changes
- Example:
  ```bash
  git checkout -b fix/navigation-consistency
  # make changes to multiple pages
  git commit -m "Standardize navigation across all pages"
  ```

### Verification Depth
- **Verification Method**: Use `grep` to count instances, then spot-check key files manually
- **Mobile Testing**: Check hamburger menu on all pages (critical)
- **Responsive**: Verify at 860px breakpoint (mobile/desktop threshold)

### Strictness Levels
1. **STRICT** (Never deviate):
   - Navigation/header structure across all 6 pages
   - CSS selectors in `style.css` and `responsive.css`
   - Hamburger menu behavior on mobile

2. **FLEXIBLE** (Context-dependent):
   - Hero section text
   - FAQ content
   - Form field ordering

---

## 1. Core Philosophy & Autonomy (4Seasons-Specific)

### Self-Verification Protocol
- Before marking a task complete, verify:
  - Navigation is consistent across ALL 6 pages: `index.html`, `contact.html`, `realisaties.html`, `over-ons.html`, `privacy.html`, `terms.html`
  - CSS selectors (`.nav`, `.nav-links`, `.hamburger`, `.btn-nav`) exist and match in all HTML files
  - JavaScript function `initMobileMenu()` is called on all pages that have a hamburger
  - No duplicate "4 Seasons" branding text (logo only)
  - Relative paths in `/pages/` use `../` correctly

### Global Consistency Mandate
- **The homepage (index.html) is the source of truth** for all UI patterns
- Every HTML page in `/pages/` must have identical:
  - Header structure with `.nav` class
  - Navigation menu with `.nav-links` class
  - Hamburger toggle button with `id="menuToggle"`
  - Breadcrumb navigation (except homepage)

### Contextual Awareness
- Brand integrity: Single logo (no duplicate text)
- All pages responsive at 860px breakpoint
- Language: Dutch for UX, English for code comments

---

## 2. Quality Standards (4Seasons-Specific)

### Code Integrity
- HTML: Semantic markup, ARIA labels on interactive elements
- CSS: Centralized in `/css/style.css` (main) and `/css/responsive.css` (media queries)
- JavaScript: All page functionality in `/js/main.js`
- No inline styles (use classes instead)
- No duplicate CSS rules across files

### UI/UX Persistence

#### Navigation Structure (STRICT - All 6 Pages)
```html
<header class="nav">
  <div class="nav__inner">
    <a href="index.html" class="logo" aria-label="4 Seasons Cleaning">
      <img src="assets/images/logo.png" alt="4 Seasons Window Cleaning Logo">
    </a>
    <button class="hamburger" id="menuToggle" aria-label="Menu openen" 
            aria-expanded="false" aria-controls="navMenu">
      <span></span><span></span><span></span>
    </button>
    <ul class="nav-links" id="navMenu">
      <li><a href="index.html#diensten">Diensten</a></li>
      <li><a href="index.html#waarom">Waarom ons</a></li>
      <li><a href="index.html#reviews">Reviews</a></li>
      <li><a href="realisaties.html">Realisaties</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="contact.html" class="btn-nav">Offerte</a></li>
    </ul>
  </div>
</header>
```

#### Hamburger Menu Behavior (STRICT - JavaScript)
- Controlled by `/js/main.js` `initMobileMenu()` function
- Toggles `.active` class on both `.hamburger` and `.nav-links`
- Closes on: link click, outside click, resize to desktop (860px+)

#### CSS Classes (Reference)
| Class | Purpose | File(s) |
|-------|---------|---------|
| `.nav` | Sticky header container | style.css |
| `.nav__inner` | Flexbox layout | style.css |
| `.nav-links` | Menu list (hidden on mobile) | style.css |
| `.hamburger` | Menu toggle button | style.css |
| `.hamburger.active` | Animated X icon | style.css |
| `.btn-nav` | CTA button styling | style.css |

### Error Prevention (4Seasons Common Issues)

1. **Duplicate Content**: Check for repeated "4 Seasons" text
   - Logo only (no `.logo__text` needed)
   - Verify: `grep "4 Seasons" pages/*.html` should find only in meta tags

2. **Path Errors**: Files in `/pages/` use relative paths
   - ✓ `href="../index.html"`
   - ✓ `src="../assets/images/logo.png"`
   - ✓ `href="../css/style.css"`
   - ✗ Do NOT use: `href="index.html"` or `src="assets/images/logo.png"`

3. **Menu Structure**: Hamburger not working
   - Verify `.nav` class exists in HTML
   - Check that `#menuToggle` and `#navMenu` IDs match JavaScript
   - Confirm `initMobileMenu()` is called on page load

4. **Responsive Breakdown**: Menu visible when it shouldn't be
   - Media query breakpoint: `860px`
   - Above 860px: hamburger hidden, nav-links visible
   - Below 860px: hamburger visible, nav-links hidden until clicked

---

## 3. Safety & Backup Protocol (4Seasons-Specific)

### Multi-File Change Template
```
AFFECTED FILES (Summary):
✓ /index.html
✓ /pages/contact.html
✓ /pages/realisaties.html
✓ /pages/over-ons.html
✓ /pages/privacy.html
✓ /pages/terms.html
✓ /css/style.css

TOTAL INSTANCES FOUND: 6 pages (grep verified)
GIT STRATEGY: git checkout -b fix/[description]
```

### Rollback Strategy
- All changes are atomic (one logical unit per commit)
- CSS changes are in external files (easy to revert)
- JavaScript is modular (individual functions)
- HTML follows consistent structure (diffs are clear)

---

## 4. Communication & Completion (4Seasons)

### Verification Report Template
```
✅ VERIFICATION REPORT - 4Seasons
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task: [Description]
Files Modified: [List and count]

Grep Results (Consistency Check):
  $ grep -r "className" pages/ css/ js/
  → [Number] instances found
  ✓ All instances updated
  ✓ No orphaned selectors

Cross-Page Testing:
  ✓ Homepage: [status]
  ✓ Contact page: [status]
  ✓ Realisaties page: [status]
  ✓ Over-ons page: [status]
  ✓ Privacy page: [status]
  ✓ Terms page: [status]

Responsive Check (860px breakpoint):
  ✓ Menu collapses correctly
  ✓ Hamburger appears/disappears
  ✓ Links styled properly

Status: ✅ Complete
```

---

## 5. Project-Specific Conventions (4Seasons)

### File Organization
```
4Seasons/
├── index.html (homepage - SOURCE OF TRUTH)
├── pages/
│   ├── contact.html
│   ├── realisaties.html
│   ├── over-ons.html
│   ├── privacy.html
│   └── terms.html
├── css/
│   ├── style.css (main styles)
│   └── responsive.css (media queries)
├── js/
│   └── main.js (all functionality)
├── assets/
│   ├── images/ (original)
│   ├── images-optimized/ (AVIF)
│   ├── fonts/
│   └── icons/
└── instructions.md
```

### Naming Conventions
- **CSS Classes**: kebab-case (`.nav-links`, `.btn-nav`, `.contact-form`)
- **HTML IDs**: camelCase (`menuToggle`, `contactForm`, `navMenu`)
- **Data Attributes**: kebab-case (`data-season`, `data-section`)
- **Files**: kebab-case for multi-word names (`contact-form.js`)

### Language Rules
- **User Interface**: Dutch (nl_NL)
- **Code Comments**: English
- **HTML Meta**: Dutch descriptions
- **lang Attribute**: Always `lang="nl"`

### Typography & Spacing
- **Font**: Inter (from Google Fonts)
- **Design Tokens**: Defined in `:root` in `style.css`
- **Breakpoints**: 
  - Mobile: < 640px
  - Tablet: 640px - 859px  
  - Desktop: 860px+
- **Color Palette**: See `:root` variables in `style.css`

---

## 6. Testing Checklist (Before Marking Complete)

- [ ] All 6 pages have identical `.nav` structure
- [ ] Hamburger menu works on all pages (toggle + close behavior)
- [ ] Responsive test: 860px breakpoint working
- [ ] No duplicate "4 Seasons" text (logo only)
- [ ] Relative paths correct in `/pages/` files (use `../`)
- [ ] CSS selectors verified with grep
- [ ] No console errors (check browser dev tools)
- [ ] Mobile: hamburger appears and functions
- [ ] Desktop: hamburger hidden, menu visible
- [ ] All links functional (relative paths work)

---

## 7. Example Prompts to Test This Mode

1. **"Add a favicon to all pages"**
   - Expected: Update all 6 HTML files + verification that favicon link appears in head

2. **"Fix the contact form submit button color"**
   - Expected: CSS update + verification across all pages, no half-measures

3. **"Create a new page `/pages/faq.html`"**
   - Expected: Complete HTML with correct header, menu, breadcrumb, relative paths

4. **"Check if navigation is consistent"**
   - Expected: Grep report showing status of all 6 pages, any mismatches identified

---

## 8. Success Metrics (4Seasons)

- ✅ Navigation identical across all 6 pages (verified by grep)
- ✅ Mobile hamburger menu works everywhere
- ✅ No duplicate branding text
- ✅ Relative paths all correct
- ✅ Responsive design maintained
- ✅ Tasks include verification reports with grep results
- ✅ Zero incomplete solutions

