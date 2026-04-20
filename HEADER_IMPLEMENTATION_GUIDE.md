# 4 SEASONS - Responsive Mobile-First Header Implementation Guide

## Overview

This guide provides complete instructions for implementing a fully responsive, mobile-first header across all pages of the 4 Seasons website. The header is designed with:

- ✅ **Mobile-First Approach**: Hamburger menu on mobile, full navigation on desktop
- ✅ **Consistency**: CSS Variables ensure identical header dimensions across all pages
- ✅ **Performance**: Optimized with lazy loading, smooth animations, and efficient selectors
- ✅ **Accessibility**: ARIA labels, keyboard navigation, focus states, reduced-motion support
- ✅ **Branding**: Navy blue (#0d47a1) color scheme with professional styling
- ✅ **Responsive**: 3 breakpoints: Mobile (<768px), Tablet (768px-1023px), Desktop (1024px+)

---

## Files Provided

1. **`css/header.css`** - Complete responsive header stylesheet with CSS Variables
2. **`components/header.html`** - Reusable header component (copy to all pages)
3. **`js/main.js`** - Updated JavaScript for hamburger menu functionality (already in your project)

---

## Step 1: Link the Header CSS

Add this line to the `<head>` section of **EVERY page** (before your other stylesheets):

```html
<!-- In index.html -->
<link rel="stylesheet" href="css/header.css">

<!-- In pages/contact.html, pages/realisaties.html, etc. -->
<link rel="stylesheet" href="../css/header.css">
```

**Important**: The path depends on the page location:
- **Pages in root** (`index.html`): `href="css/header.css"`
- **Pages in `/pages/`**: `href="../css/header.css"`

---

## Step 2: Update Header HTML on All Pages

Replace the existing `<header>` element on each page with the new header component.

### Current Structure (OLD)
```html
<header class="nav">
    <div class="nav__inner">
        <a href="#" class="logo" aria-label="4 Seasons Cleaning">
            <!-- logo picture element -->
        </a>
        <button class="hamburger" id="menuToggle" aria-label="Menu openen" aria-expanded="false" aria-controls="navMenu">
            <span></span><span></span><span></span>
        </button>
        <ul class="nav-links" id="navMenu">
            <!-- navigation items -->
        </ul>
    </div>
</header>
```

### New Structure (NEW)
Copy the header from `components/header.html` to each page.

**Key Changes**:
- Logo link updated with proper URLs
- Improved ARIA labels in Dutch
- Optimized responsive image sizes
- Better semantic structure

---

## Step 3: Update Navigation Links on Each Page

The header component includes these links by default:

```html
<li><a href="#diensten">Diensten</a></li>
<li><a href="#waarom">Waarom ons</a></li>
<li><a href="#reviews">Reviews</a></li>
<li><a href="pages/realisaties.html">Realisaties</a></li>
<li><a href="pages/contact.html">Contact</a></li>
<li><a href="pages/contact.html" class="btn-nav">Offerte</a></li>
```

**Update href paths for each page**:

#### On `index.html` (root level):
```html
<li><a href="pages/realisaties.html">Realisaties</a></li>
<li><a href="pages/contact.html">Contact</a></li>
<li><a href="pages/contact.html" class="btn-nav">Offerte</a></li>
```

#### On `pages/contact.html` (subdirectory):
```html
<li><a href="../#diensten">Diensten</a></li>
<li><a href="../#waarom">Waarom ons</a></li>
<li><a href="../#reviews">Reviews</a></li>
<li><a href="realisaties.html">Realisaties</a></li>
<li><a href="contact.html">Contact</a></li>
<li><a href="contact.html" class="btn-nav">Offerte</a></li>
```

#### On `pages/realisaties.html` (subdirectory):
```html
<li><a href="../#diensten">Diensten</a></li>
<li><a href="../#waarom">Waarom ons</a></li>
<li><a href="../#reviews">Reviews</a></li>
<li><a href="realisaties.html">Realisaties</a></li>
<li><a href="contact.html">Contact</a></li>
<li><a href="contact.html" class="btn-nav">Offerte</a></li>
```

---

## Step 4: Ensure JavaScript Works

The hamburger menu functionality requires the existing `js/main.js` code. Verify this function exists:

```javascript
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

    // Close menu when a link is clicked
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', false);
        });
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (nav && !nav.contains(event.target) && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', false);
        }
    });
}
```

This should already be in your `js/main.js` and called in the `DOMContentLoaded` event.

---

## Step 5: Remove Old Header Styles

If you have old header/nav styles in `css/style.css` or `css/responsive.css`, remove or comment them out to avoid conflicts:

```css
/* REMOVE OR COMMENT OUT these old styles:
.nav { ... }
.nav__inner { ... }
.logo { ... }
.logo img { ... }
.nav-links { ... }
.hamburger { ... }
*/
```

**Better approach**: Leave them commented for reference, but the new `header.css` will override them.

---

## CSS Variables Reference

The header uses these CSS custom properties for consistency. You can override them in `css/style.css` if needed:

```css
:root {
    /* Header Dimensions */
    --header-height: 70px;              /* Mobile */
    --header-height-tablet: 75px;       /* Tablet */
    --header-height-desktop: 80px;      /* Desktop */
    
    /* Colors - Navy Blue Branding */
    --header-bg: #ffffff;
    --header-border: #e5e7eb;
    --header-text: #1f2937;
    --header-text-hover: #0d47a1;
    --button-primary: #0d47a1;
    --button-primary-hover: #0a3a7f;
    --button-primary-active: #081e47;
    
    /* Spacing */
    --header-padding-x: 1rem;           /* Mobile */
    --header-padding-x-tablet: 1.5rem;  /* Tablet */
    --header-padding-x-desktop: 2rem;   /* Desktop */
    --header-gap: 1rem;
    --header-gap-desktop: 2rem;
    
    /* Typography */
    --header-font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --header-font-size: 15px;           /* Mobile */
    --header-font-size-tablet: 15px;    /* Tablet */
    --header-font-size-desktop: 16px;   /* Desktop */
    --header-font-weight: 500;
    --header-font-weight-bold: 600;
    
    /* Effects */
    --header-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    --header-shadow-active: 0 4px 12px rgba(0, 0, 0, 0.12);
    --header-backdrop: saturate(180%) blur(12px);
    --header-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## Responsive Behavior

### Mobile (<768px)
- **Logo**: Responsive, scales from 90px to 100px
- **Hamburger Menu**: Visible, animated
- **Navigation**: Hidden, slides down when menu clicked
- **Header Height**: 70px
- **Padding**: 1rem left/right

### Tablet (768px - 1023px)
- **Logo**: Slightly larger (100px)
- **Hamburger Menu**: Hidden
- **Navigation**: Visible, key links shown
- **Header Height**: 75px
- **Padding**: 1.5rem left/right

### Desktop (1024px+)
- **Logo**: Full size (120px)
- **Hamburger Menu**: Hidden
- **Navigation**: Full layout with underline hover effect
- **Header Height**: 80px
- **Padding**: 2rem left/right
- **Spacing**: Better gaps between elements

---

## Accessibility Features

✅ **Keyboard Navigation**: Tab through all header elements
✅ **Screen Readers**: ARIA labels for hamburger and logo
✅ **Focus States**: Visible outline on all interactive elements
✅ **Reduced Motion**: Respects `prefers-reduced-motion` for accessibility
✅ **High Contrast**: Enhanced styles for `prefers-contrast: more`
✅ **Dark Mode**: Optional dark mode support via `prefers-color-scheme`

---

## Testing Checklist

### Mobile Testing (< 768px)
- [ ] Logo displays correctly
- [ ] Hamburger menu visible and clickable
- [ ] Hamburger animates when clicked (X shape)
- [ ] Menu slides down smoothly
- [ ] Menu closes when clicking a link
- [ ] Menu closes when clicking outside
- [ ] Menu closes when pressing Escape
- [ ] All links work correctly

### Tablet Testing (768px - 1024px)
- [ ] Logo larger than mobile
- [ ] Hamburger menu hidden
- [ ] Navigation links visible
- [ ] "Offerte" button visible
- [ ] All spacing consistent
- [ ] Sticky header works

### Desktop Testing (> 1024px)
- [ ] Full header layout visible
- [ ] Logo on far left
- [ ] Navigation centered
- [ ] "Offerte" button on far right
- [ ] Underline hover effect on links
- [ ] Button has hover shadow effect
- [ ] Header stays sticky while scrolling
- [ ] All links have proper focus states

### Cross-Browser Testing
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (macOS & iOS)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Customization Guide

### Change Header Height
```css
/* In css/style.css or override in root */
:root {
    --header-height: 80px;              /* Mobile - increase if needed */
    --header-height-tablet: 85px;       /* Tablet */
    --header-height-desktop: 90px;      /* Desktop */
}
```

### Change Colors
```css
:root {
    --header-text-hover: #ff6b35;       /* Your accent color */
    --button-primary: #ff6b35;          /* Change button color */
}
```

### Adjust Spacing
```css
:root {
    --header-gap: 0.5rem;               /* Tighter spacing */
    --header-gap-desktop: 1.5rem;       /* Adjust desktop gap */
}
```

### Remove Glass-Morphism Effect
```css
/* In css/header.css, comment out: */
/* backdrop-filter: var(--header-backdrop); */
/* -webkit-backdrop-filter: var(--header-backdrop); */
```

---

## Performance Optimization

The header is optimized for performance:

- ✅ **Minimal CSS**: Only what's needed (440 lines, well-organized)
- ✅ **No JavaScript animations**: Uses CSS transitions
- ✅ **Lazy-loaded logo**: Responsive images with WebP fallback
- ✅ **Efficient selectors**: Direct class targeting, no nested complexity
- ✅ **Hardware acceleration**: Uses `transform` for animations
- ✅ **Sticky positioning**: Native browser implementation

---

## Common Issues & Solutions

### Issue: Hamburger menu not working
**Solution**: Ensure `js/main.js` is loaded and `initMobileMenu()` is called. Check browser console for errors.

### Issue: Header height inconsistent across pages
**Solution**: Ensure `css/header.css` is linked on all pages with correct path (`css/header.css` vs `../css/header.css`).

### Issue: Logo image not displaying
**Solution**: Verify image paths are correct based on page location. Use `assets/images-optimized/logo-*.{webp,jpg}` files.

### Issue: Navigation links overlapping on mobile
**Solution**: The mobile menu uses `position: absolute`, so ensure no overflow hidden on parent. Check `z-index` conflicts.

### Issue: Hover effects not working on tablet
**Solution**: Tablets support `:hover`, so hover effects work. For touch devices, use `:active` instead via JavaScript if needed.

---

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+

**Note**: Uses CSS custom properties (CSS Variables), which are widely supported. For older browsers, you may need to add fallback values.

---

## Next Steps

1. Link `css/header.css` to all pages
2. Update header HTML with new component
3. Update navigation link paths for each page
4. Test on mobile, tablet, and desktop
5. Verify all links work correctly
6. Check accessibility with screen reader (NVDA, JAWS, or VoiceOver)
7. Deploy and verify live

---

## Support & Questions

If you encounter any issues:
1. Check browser console for JavaScript errors
2. Verify CSS file is loaded (check Network tab)
3. Ensure ARIA labels are correct
4. Test with browser DevTools Device Emulation
5. Check that hamburger menu listener is attached

---

**Last Updated**: April 2026
**Version**: 1.0
**Status**: Production Ready ✅
