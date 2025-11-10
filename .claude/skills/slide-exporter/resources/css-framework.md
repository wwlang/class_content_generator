# CSS Framework for Slide Presentations

This document contains the complete CSS framework that should be inlined into every generated HTML presentation. Designed for **1024x768px (4:3 aspect ratio)** slides.

---

## Complete CSS Code

```css
/* ========================================
   CSS VARIABLES - Easy Theme Customization
   ======================================== */

:root {
  /* Colors */
  --color-primary: #7373b0;      /* Main text color (muted blue-purple) */
  --color-secondary: #475569;    /* Body text color (medium gray) */
  --color-accent: #7373b0;       /* Brand/accent color (muted blue-purple) */
  --color-muted: #64748b;        /* Muted text (light gray) */
  --color-background: #ffffff;   /* Slide background (white) */
  --color-stage: #e2e8f0;        /* Stage background (light gray) */
  --color-border: #e2e8f0;       /* Border color */
  --color-light-bg: #f8fafc;     /* Light background for boxes */

  /* Typography */
  --font-header: 'PT Serif', serif;
  --font-body: 'Roboto', sans-serif;

  /* Spacing */
  --slide-padding: 60px;
  --slide-width: 1024px;
  --slide-height: 768px;

  /* Effects */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --border-radius: 12px;
}

/* ========================================
   RESET & BASE STYLES
   ======================================== */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  font-family: var(--font-body);
  color: var(--color-primary);
  overflow: hidden;
}

/* ========================================
   PRESENTATION CONTAINER & STAGE
   ======================================== */

.presentation-container {
  width: 100vw;
  height: 100vh;
  background: var(--color-stage);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* ========================================
   SLIDE BASE STYLES
   ======================================== */

.slide {
  width: var(--slide-width);
  height: var(--slide-height);
  background: var(--color-background);
  box-shadow: var(--shadow-lg);
  border-radius: 8px;
  position: absolute;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
  display: none;
}

.slide.active {
  opacity: 1;
  display: block;
}

/* ========================================
   NAVIGATION CONTROLS
   ======================================== */

.nav-controls {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 20px;
  background: rgba(30, 41, 59, 0.9);
  padding: 12px 24px;
  border-radius: 30px;
  box-shadow: var(--shadow-lg);
  z-index: 1000;
}

.nav-controls button {
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 24px;
  font-weight: 700;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.nav-controls button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-controls button:active {
  background: rgba(255, 255, 255, 0.2);
}

#slide-counter {
  color: #ffffff;
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 500;
  min-width: 80px;
  text-align: center;
}

/* ========================================
   PROGRESS BAR
   ======================================== */

.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: rgba(30, 41, 59, 0.1);
  z-index: 1000;
}

.progress-fill {
  height: 100%;
  background: var(--color-accent);
  width: 0%;
  transition: width 0.3s ease;
}

/* ========================================
   TYPOGRAPHY - HEADERS & BODY
   ======================================== */

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-header);
  color: #1e293b;
  font-weight: 700;
  line-height: 1.2;
}

h1 {
  font-size: 70px;
  font-weight: 700;
}

h2 {
  font-size: 40px;
}

h3 {
  font-size: 36px;
}

h4 {
  font-size: 30px;
}

p, li {
  font-family: var(--font-body);
  font-size: 27px;
  line-height: 1.5;
  color: var(--color-secondary);
}

.slide-title {
  font-family: var(--font-header);
  font-size: 40px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 40px;
}

/* ========================================
   LAYOUT 1: TITLE SLIDE
   ======================================== */

.title-slide {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  text-align: left;
  padding: var(--slide-padding);
}

.title-content h1 {
  font-size: 70px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 36px;
  color: var(--color-secondary);
  margin-top: 20px;
}

.author {
  font-size: 27px;
  color: var(--color-muted);
  margin-top: 40px;
}

/* ========================================
   LAYOUT 2: SECTION BREAK SLIDE
   ======================================== */

.section-break-slide {
  background: var(--color-accent);
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: var(--slide-padding);
}

.section-title {
  font-family: var(--font-header);
  font-size: 50px;
  font-weight: 400;
  color: #ffffff;
  text-align: left;
}

/* ========================================
   LAYOUT 3: STANDARD CONTENT (Title + Bullets)
   ======================================== */

.content-slide {
  padding: var(--slide-padding);
}

.content-body ul {
  list-style-type: disc;
  list-style-position: outside;
  padding-left: 30px;
  margin-top: 0;
}

.content-body li {
  font-size: 27px;
  color: var(--color-secondary);
  line-height: 1.5;
  margin-bottom: 16px;
}

.content-body li:last-child {
  margin-bottom: 0;
}

/* Nested lists */
.content-body li ul {
  margin-top: 12px;
  padding-left: 30px;
}

.content-body li ul li {
  font-size: 24px;
  margin-bottom: 8px;
}

/* ========================================
   LAYOUT 4: SPLIT SCREEN (50/50 Text & Image)
   ======================================== */

.split-slide {
  padding: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.split-text-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--slide-padding);
}

.split-text-column h2 {
  margin-bottom: 24px;
}

.split-text-column p {
  margin-bottom: 16px;
}

.split-text-column ul {
  list-style-type: disc;
  padding-left: 30px;
}

.split-text-column li {
  margin-bottom: 12px;
}

.split-image-column {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-light-bg);
  border-left: 4px solid var(--color-accent);
}

.split-image-column img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
}

/* Legacy support for .split-content wrapper structure */
.split-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.text-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.text-column p {
  margin-bottom: 20px;
}

.text-column ul {
  list-style-type: disc;
  padding-left: 30px;
}

.text-column li {
  margin-bottom: 12px;
}

.image-column {
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-column img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-md);
}

/* ========================================
   LAYOUT 5: THREE-COLUMN / TILED LAYOUT
   ======================================== */

.tiled-slide {
  padding: var(--slide-padding);
}

.tiles-container {
  display: flex;
  gap: 40px;
}

.tile {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.icon-container {
  color: var(--color-accent);
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.lucide-icon {
  stroke: currentColor;
  fill: none;
}

.tile h3 {
  font-family: var(--font-header);
  font-size: 33px;
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 12px;
}

.tile p {
  font-size: 24px;
  color: var(--color-secondary);
  line-height: 1.5;
}

/* ========================================
   LAYOUT 6: BIG NUMBER SLIDE
   ======================================== */

.big-number-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--slide-padding);
}

.number-content {
  text-align: center;
}

.big-number {
  font-family: var(--font-header);
  font-size: 180px;
  font-weight: 700;
  color: var(--color-accent);
  line-height: 1;
  margin-bottom: 30px;
}

.number-explanation {
  font-size: 36px;
  color: var(--color-secondary);
  max-width: 700px;
  margin: 30px auto 0;
  line-height: 1.4;
}

/* ========================================
   LAYOUT 7: COMPARISON (This vs. That) SLIDE
   ======================================== */

.comparison-slide {
  padding: var(--slide-padding);
}

.comparison-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.comparison-box {
  background: var(--color-light-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  padding: 30px;
}

.comparison-box h3 {
  font-family: var(--font-header);
  font-size: 36px;
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 20px;
  text-align: center;
}

.comparison-box ul {
  list-style-type: disc;
  padding-left: 25px;
}

.comparison-box li {
  font-size: 24px;
  color: var(--color-secondary);
  margin-bottom: 12px;
  line-height: 1.4;
}

.comparison-box li:last-child {
  margin-bottom: 0;
}

/* ========================================
   LAYOUT 8: QUOTE SLIDE
   ======================================== */

.quote-slide {
  display: flex;
  align-items: center;
  padding: 80px;
}

.quote-content {
  max-width: 800px;
}

.main-quote {
  font-family: var(--font-body);
  font-size: 42px;
  font-weight: 400;
  font-style: italic;
  color: var(--color-primary);
  line-height: 1.6;
  border-left: 4px solid var(--color-accent);
  padding-left: 30px;
  margin: 0;
}

.quote-attribution {
  font-family: var(--font-body);
  font-size: 30px;
  font-weight: 500;
  color: var(--color-secondary);
  margin-top: 30px;
}

.quote-context {
  font-size: 24px;
  color: var(--color-muted);
  margin-top: 8px;
}

/* ========================================
   LAYOUT 9: TEAM / PROFILE SLIDE
   ======================================== */

.team-slide {
  padding: var(--slide-padding);
}

.profiles-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.profile-card {
  text-align: center;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 20px;
  border: 3px solid var(--color-border);
  display: block;
}

.profile-card h3 {
  font-family: var(--font-header);
  font-size: 30px;
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 8px;
}

.profile-role {
  font-size: 24px;
  font-weight: 500;
  color: var(--color-accent);
  margin-bottom: 8px;
}

.profile-detail {
  font-size: 21px;
  color: var(--color-muted);
}

/* ========================================
   LAYOUT 10: THANK YOU SLIDE
   ======================================== */

.thank-you-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--slide-padding);
  background: #fafafa;
}

.closing-content {
  text-align: center;
}

.thank-you-heading {
  font-family: var(--font-header);
  font-size: 60px;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 20px;
}

.closing-subtext {
  font-size: 36px;
  color: var(--color-secondary);
  margin-top: 20px;
  margin-bottom: 60px;
}

.contact-info {
  margin-top: 40px;
}

.contact-item {
  font-size: 27px;
  color: var(--color-secondary);
  margin-bottom: 12px;
}

/* ========================================
   UNIVERSAL COMPONENTS - CITATIONS
   ======================================== */

.slide-footer {
  position: absolute;
  bottom: 20px;
  left: 60px;
  right: 60px;
}

.citation {
  font-family: var(--font-body);
  font-size: 17px;
  color: var(--color-muted);
  line-height: 1.4;
  margin-bottom: 4px;
}

.citation:last-child {
  margin-bottom: 0;
}

/* ========================================
   UNIVERSAL COMPONENTS - SPEAKER NOTES
   ======================================== */

.speaker-notes {
  display: none;
  background: var(--color-light-bg);
  padding: 20px;
  margin-top: 20px;
  border-left: 3px solid var(--color-accent);
}

.speaker-notes h4 {
  font-family: var(--font-header);
  font-size: 21px;
  font-weight: 500;
  color: var(--color-primary);
  margin-bottom: 8px;
}

.speaker-notes p {
  font-family: var(--font-body);
  font-size: 18px;
  color: var(--color-secondary);
  line-height: 1.5;
}

/* ========================================
   IMAGE PLACEHOLDERS
   ======================================== */

.image-placeholder {
  width: 100%;
  height: 100%;
  background: var(--color-stage);
  border: 2px dashed #cbd5e1;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-placeholder svg {
  width: 100%;
  height: 100%;
}

.image-placeholder text {
  font-family: var(--font-body);
  font-size: 20px;
  fill: var(--color-muted);
}

/* ========================================
   ANIMATIONS & TRANSITIONS
   ======================================== */

.slide {
  transition: opacity 0.3s ease-in-out;
}

/* Fade in animation for active slide */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.slide.active {
  animation: fadeIn 0.3s ease-in-out;
}

/* ========================================
   PRINT STYLES
   ======================================== */

@media print {
  body {
    background: white;
  }

  .presentation-container {
    background: white;
    display: block;
    width: 100%;
    height: auto;
  }

  .slide {
    display: block !important;
    opacity: 1 !important;
    position: relative !important;
    page-break-after: always;
    page-break-inside: avoid;
    margin: 0 auto;
    box-shadow: none;
  }

  .nav-controls,
  .progress-bar {
    display: none !important;
  }

  .speaker-notes {
    display: block !important;
    margin-top: 20px;
    page-break-before: avoid;
  }

  /* Ensure images print properly */
  .image-column img,
  .profile-image {
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }
}

/* ========================================
   FULLSCREEN SUPPORT
   ======================================== */

.presentation-container:fullscreen {
  background: black;
}

.presentation-container:fullscreen .slide {
  box-shadow: none;
}

/* ========================================
   ACCESSIBILITY ENHANCEMENTS
   ======================================== */

/* Focus styles for keyboard navigation */
.nav-controls button:focus {
  outline: 2px solid #ffffff;
  outline-offset: 4px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --color-primary: #000000;
    --color-secondary: #1a1a1a;
    --color-accent: #0000ff;
    --color-border: #000000;
  }

  .slide {
    border: 2px solid black;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ========================================
   UTILITY CLASSES
   ======================================== */

.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mt-20 {
  margin-top: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}

.accent-color {
  color: var(--color-accent);
}

.muted-color {
  color: var(--color-muted);
}
```

---

## Usage Notes

### Inlining in HTML

This entire CSS block should be placed inside `<style>` tags in the `<head>` of the generated HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation Title</title>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

  <!-- Inline CSS -->
  <style>
    [PASTE COMPLETE CSS FROM ABOVE]
  </style>
</head>
<body>
  <!-- Presentation HTML -->
</body>
</html>
```

### Customizing Colors

To customize the color scheme, users can modify the CSS variables at the top:

```css
:root {
  --color-accent: #10b981;  /* Change to green */
  --color-primary: #0f172a;  /* Darker text */
}
```

All elements using these colors will automatically update.

### Adding Custom Layouts

To add a custom layout:

1. Create new CSS class (e.g., `.custom-layout-slide`)
2. Define dimensions and positioning
3. Add to HTML with that class
4. Ensure it respects 1024x768px container

### File Size Considerations

- Complete CSS: ~12KB uncompressed
- Minified: ~8KB
- Gzipped: ~3KB
- Negligible impact on overall HTML file size

---

## Testing Checklist

Before finalizing any presentation using this CSS:

- [ ] All 10 layouts render correctly at 1024x768px
- [ ] Text is readable at standard projection distances
- [ ] Images scale properly without distortion
- [ ] Icons display in accent color
- [ ] Navigation buttons work (arrow keys, buttons)
- [ ] Progress bar updates correctly
- [ ] Print view shows all slides + speaker notes
- [ ] Citations appear in footer
- [ ] Cross-browser compatible (Chrome, Firefox, Safari, Edge)
- [ ] Fullscreen mode works (F11)
- [ ] Accessibility features function (keyboard nav, high contrast)

---

*This CSS framework provides the complete styling system for all generated HTML presentations.*

---

## Educational Layout Styles (Layouts 11-25)

Complete CSS for all 15 educational-specific layouts added to the presentation system.

### Tier 1 Educational Layouts (11-15)

```css
/* Layout 11: Vocabulary Table (Bilingual) */
.vocab-table-slide {
  padding: 60px;
}

.vocab-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.vocab-table thead {
  background: #7373b0;
  color: white;
}

.vocab-table th {
  padding: 16px;
  text-align: left;
  font-family: 'PT Serif';
  font-size: 24px;
  font-weight: 400;
}

.vocab-table tbody tr {
  border-bottom: 1px solid #e2e8f0;
  transition: background 0.2s ease;
}

.vocab-table tbody tr:last-child {
  border-bottom: none;
}

.vocab-table tbody tr:hover {
  background: #f8fafc;
}

.vocab-table td {
  padding: 16px;
  font-size: 22px;
  vertical-align: top;
  color: #475569;
  line-height: 1.5;
}

.vocab-table td:first-child {
  font-weight: 600;
  color: #1e293b;
}

.vocab-table td:nth-child(2) {
  font-style: italic;
  color: #7373b0;
}

/* Layout 12: Think-Pair-Share / Activity Instructions */
.activity-slide {
  padding: 60px;
}

.activity-header {
  background: linear-gradient(135deg, #7373b0 0%, #8b87c7 100%);
  color: white;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 30px;
  text-align: center;
}

.activity-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.activity-title {
  font-family: 'PT Serif';
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 12px;
}

.activity-description {
  font-size: 26px;
  line-height: 1.5;
  opacity: 0.95;
}

.activity-phases {
  display: flex;
  gap: 24px;
  margin-bottom: 30px;
}

.phase {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.phase:hover {
  box-shadow: 0 8px 20px rgba(115, 115, 176, 0.2);
  transform: translateY(-4px);
}

.phase-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #7373b0;
  color: white;
  font-family: 'PT Serif';
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 16px;
}

.phase.think .phase-number { background: #3b82f6; }
.phase.pair .phase-number { background: #10b981; }
.phase.share .phase-number { background: #8b5cf6; }

.phase h3 {
  font-family: 'PT Serif';
  font-size: 30px;
  color: #7373b0;
  margin-bottom: 8px;
}

.phase.think h3 { color: #3b82f6; }
.phase.pair h3 { color: #10b981; }
.phase.share h3 { color: #8b5cf6; }

.phase-time {
  font-size: 22px;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 12px;
  display: block;
}

.phase p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
  margin-bottom: 12px;
}

.phase ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.phase li {
  font-size: 22px;
  color: #475569;
  padding: 6px 0;
  padding-left: 28px;
  position: relative;
  line-height: 1.4;
}

.phase li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #7373b0;
  font-weight: 700;
}

.phase.think li::before { color: #3b82f6; }
.phase.pair li::before { color: #10b981; }
.phase.share li::before { color: #8b5cf6; }

.activity-reminder {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #78350f;
  text-align: center;
}

.activity-reminder strong {
  color: #92400e;
  font-weight: 700;
}

/* Layout 13: Rubric Preview */
.rubric-preview-slide {
  padding: 60px;
}

.rubric-intro {
  background: #7373b0;
  color: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  text-align: center;
}

.rubric-intro p {
  font-size: 28px;
  margin: 0;
  line-height: 1.5;
}

.rubric-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.rubric-table thead tr {
  background: #7373b0;
  color: white;
}

.rubric-table th {
  padding: 16px;
  text-align: left;
  font-family: 'PT Serif';
  font-size: 24px;
  font-weight: 400;
}

.rubric-table th.criterion-column {
  width: 30%;
  background: #5a5a8f;
}

.rubric-table tbody tr {
  border-bottom: 1px solid #e2e8f0;
}

.rubric-table tbody tr:last-child {
  border-bottom: none;
}

.rubric-table td {
  padding: 16px;
  font-size: 22px;
  vertical-align: top;
  line-height: 1.5;
}

.criterion-cell {
  background: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

.excellent-cell {
  background: rgba(16, 185, 129, 0.1);
  color: #065f46;
}

.good-cell {
  background: rgba(59, 130, 246, 0.1);
  color: #1e40af;
}

.satisfactory-cell {
  background: rgba(245, 158, 11, 0.1);
  color: #92400e;
}

.rubric-note {
  background: #f8fafc;
  border-left: 4px solid #7373b0;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #475569;
  margin-top: 20px;
  text-align: center;
}

.rubric-note strong {
  color: #7373b0;
  font-weight: 700;
}

/* Layout 14: Concept Map / Mind Map */
.concept-map-slide {
  padding: 60px;
}

.concept-map-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 40px 0;
}

.central-concept {
  background: linear-gradient(135deg, #7373b0 0%, #8b87c7 100%);
  color: white;
  padding: 30px 40px;
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(115, 115, 176, 0.3);
  margin-bottom: 60px;
  text-align: center;
  position: relative;
  z-index: 10;
}

.central-concept h3 {
  font-family: 'PT Serif';
  font-size: 42px;
  font-weight: 700;
  margin: 0;
}

.concept-branches {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  width: 100%;
}

.branch {
  background: white;
  border: 3px solid #7373b0;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
}

.branch:hover {
  border-color: #5a5a8f;
  box-shadow: 0 8px 20px rgba(115, 115, 176, 0.2);
  transform: translateY(-4px);
}

.branch::before {
  content: "";
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 40px;
  background: linear-gradient(180deg, #7373b0 0%, rgba(115, 115, 176, 0) 100%);
}

.branch-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 12px;
  color: #7373b0;
}

.branch h4 {
  font-family: 'PT Serif';
  font-size: 26px;
  color: #7373b0;
  margin-bottom: 8px;
}

.branch p {
  font-size: 22px;
  color: #475569;
  line-height: 1.4;
  margin: 0;
}

/* Layout 15: Worked Example */
.worked-example-slide {
  padding: 60px;
}

.example-header {
  background: linear-gradient(135deg, #7373b0 0%, #8b87c7 100%);
  color: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.example-type {
  font-size: 20px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  margin-bottom: 8px;
  opacity: 0.9;
}

.example-title {
  font-family: 'PT Serif';
  font-size: 36px;
  font-weight: 700;
  margin: 0;
}

.problem-statement {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.problem-statement h3 {
  font-family: 'PT Serif';
  font-size: 28px;
  color: #92400e;
  margin-bottom: 12px;
}

.problem-statement p {
  font-size: 26px;
  color: #78350f;
  line-height: 1.5;
  margin: 0;
}

.solution-steps {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.solution-steps h3 {
  font-family: 'PT Serif';
  font-size: 30px;
  color: #7373b0;
  margin-bottom: 20px;
}

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
}

.step:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.step-number {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #7373b0;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'PT Serif';
  font-size: 28px;
  font-weight: 700;
}

.step-content h4 {
  font-family: 'PT Serif';
  font-size: 26px;
  color: #475569;
  margin-bottom: 8px;
}

.step-content p {
  font-size: 24px;
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

.step-formula {
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 22px;
  color: #7373b0;
  margin-top: 8px;
}

.final-answer {
  background: #d1fae5;
  border-left: 4px solid #10b981;
  padding: 24px;
  border-radius: 12px;
}

.final-answer h3 {
  font-family: 'PT Serif';
  font-size: 30px;
  color: #065f46;
  margin-bottom: 12px;
}

.final-answer p {
  font-size: 28px;
  color: #065f46;
  font-weight: 600;
  margin: 0;
}
```

### Tier 2 Educational Layouts (16-20)

```css
/* Layout 16: Timeline / Process Flow */
.timeline-slide {
  padding: 60px;
}

.timeline-container {
  position: relative;
  padding: 60px 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

.timeline-line {
  position: absolute;
  top: 90px;
  left: 5%;
  right: 5%;
  height: 4px;
  background: linear-gradient(90deg, #c7d2fe 0%, #7373b0 100%);
  z-index: 0;
}

.timeline-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.timeline-marker {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #7373b0;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  margin-bottom: 24px;
}

.timeline-marker.active {
  width: 32px;
  height: 32px;
  background: #ef4444;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 15px rgba(239, 68, 68, 0);
  }
}

.timeline-content {
  text-align: center;
}

.timeline-year {
  font-family: 'PT Serif';
  font-size: 30px;
  font-weight: 700;
  color: #7373b0;
  margin-bottom: 12px;
}

.timeline-title {
  font-family: 'PT Serif';
  font-size: 26px;
  font-weight: 400;
  color: #475569;
  margin-bottom: 8px;
}

.timeline-content p {
  font-size: 22px;
  color: #64748b;
  line-height: 1.4;
}

/* Layout 17: Case Study Layout */
.case-study-slide {
  padding: 60px;
}

.case-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 30px;
}

.case-section {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
  border-left: 4px solid #7373b0;
}

.case-section.challenge {
  border-left-color: #f59e0b;
}

.case-section.solution {
  border-left-color: #10b981;
}

.case-section.result {
  border-left-color: #7373b0;
}

.case-icon {
  flex-shrink: 0;
  color: #7373b0;
}

.case-section.challenge .case-icon {
  color: #f59e0b;
}

.case-section.solution .case-icon {
  color: #10b981;
}

.case-text h3 {
  font-family: 'PT Serif';
  font-size: 30px;
  color: #475569;
  margin-bottom: 12px;
}

.case-text p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
}

.case-question {
  background: #7373b0;
  color: white;
  padding: 24px;
  border-radius: 12px;
  font-size: 26px;
  text-align: center;
}

.case-question strong {
  font-weight: 700;
}

/* Layout 18: Learning Objectives Preview */
.objectives-slide {
  padding: 60px;
}

.objectives-intro {
  font-size: 30px;
  color: #475569;
  margin-bottom: 30px;
  font-weight: 500;
}

.objectives-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.objective-item {
  display: flex;
  gap: 20px;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.objective-item:hover {
  border-color: #7373b0;
  box-shadow: 0 4px 12px rgba(115, 115, 176, 0.15);
}

.objective-icon {
  flex-shrink: 0;
  color: #7373b0;
}

.objective-item[data-level="understand"] .objective-icon { color: #3b82f6; }
.objective-item[data-level="apply"] .objective-icon { color: #10b981; }
.objective-item[data-level="analyze"] .objective-icon { color: #f59e0b; }
.objective-item[data-level="create"] .objective-icon { color: #8b5cf6; }

.objective-content {
  flex: 1;
}

.bloom-level {
  display: inline-block;
  font-size: 20px;
  font-weight: 700;
  color: #7373b0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.objective-item[data-level="understand"] .bloom-level { color: #3b82f6; }
.objective-item[data-level="apply"] .bloom-level { color: #10b981; }
.objective-item[data-level="analyze"] .bloom-level { color: #f59e0b; }
.objective-item[data-level="create"] .bloom-level { color: #8b5cf6; }

.objective-content p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
}

.objective-check {
  font-size: 48px;
  color: #cbd5e1;
  flex-shrink: 0;
}

.assessment-link {
  background: #7373b0;
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.assessment-link p {
  font-size: 26px;
  margin: 0;
}

/* Layout 19: Discussion Prompt / Debate Setup */
.discussion-slide {
  padding: 60px;
}

.central-question {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: linear-gradient(135deg, #7373b0 0%, #8b87c7 100%);
  color: white;
  padding: 40px;
  border-radius: 16px;
  margin-bottom: 30px;
  box-shadow: 0 8px 20px rgba(115, 115, 176, 0.25);
}

.question-icon {
  color: white;
  opacity: 0.9;
}

.main-question {
  font-family: 'PT Serif';
  font-size: 34px;
  font-weight: 700;
  text-align: center;
  line-height: 1.4;
  margin: 0;
}

.debate-sides {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.side {
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
}

.side.position-for {
  border-left: 6px solid #10b981;
}

.side.position-against {
  border-left: 6px solid #ef4444;
}

.side h3 {
  font-family: 'PT Serif';
  font-size: 28px;
  color: #475569;
  margin-bottom: 16px;
  text-align: center;
}

.side ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side li {
  font-size: 24px;
  color: #475569;
  padding: 10px 0;
  padding-left: 32px;
  position: relative;
}

.side.position-for li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 700;
  font-size: 28px;
}

.side.position-against li::before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #ef4444;
  font-weight: 700;
  font-size: 28px;
}

.discussion-format {
  background: #475569;
  color: white;
  padding: 24px;
  border-radius: 12px;
}

.discussion-format h4 {
  font-family: 'PT Serif';
  font-size: 26px;
  margin-bottom: 16px;
  text-align: center;
}

.format-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.step {
  background: rgba(255,255,255,0.1);
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 22px;
  font-weight: 500;
}

.arrow {
  font-size: 32px;
  font-weight: 700;
}

/* Layout 20: Resource List / Further Reading */
.resources-slide {
  padding: 60px;
}

.resources-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.resource-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.resource-card:hover {
  border-color: #7373b0;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  transform: translateY(-4px);
}

.resource-card.essential {
  border-color: #7373b0;
  border-width: 3px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.resource-icon {
  color: #7373b0;
}

.resource-badge {
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 6px 12px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
}

.resource-card.essential .resource-badge {
  background: #7373b0;
  color: white;
}

.resource-card.recommended .resource-badge {
  background: #10b981;
  color: white;
}

.resource-card.optional .resource-badge {
  background: #64748b;
  color: white;
}

.resource-card.practice .resource-badge {
  background: #f59e0b;
  color: white;
}

.resource-card h3 {
  font-family: 'PT Serif';
  font-size: 26px;
  color: #475569;
  margin-bottom: 12px;
  line-height: 1.3;
}

.resource-description {
  font-size: 22px;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
}

.resource-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.meta-type,
.meta-length {
  font-size: 20px;
  color: #94a3b8;
}

.resource-link {
  font-size: 22px;
  color: #7373b0;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.resource-link:hover {
  color: #5a5a8f;
  text-decoration: underline;
}
```

### Tier 3 Educational Layouts (21-25)

```css
/* Layout 21: Research Findings / Study Results */
.research-slide {
  padding: 60px;
}

.research-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.research-metadata {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #7373b0;
}

.meta-item {
  font-size: 22px;
  color: #475569;
}

.meta-item strong {
  color: #1e293b;
  font-weight: 600;
}

.research-findings h3 {
  font-family: 'PT Serif';
  font-size: 32px;
  color: #7373b0;
  margin-bottom: 20px;
}

.finding-item {
  display: flex;
  gap: 24px;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  margin-bottom: 16px;
}

.finding-item.primary {
  border-color: #7373b0;
  border-width: 3px;
}

.finding-stat {
  font-family: 'PT Serif';
  font-size: 72px;
  font-weight: 700;
  color: #7373b0;
  flex-shrink: 0;
  min-width: 160px;
  text-align: center;
}

.finding-item.secondary .finding-stat {
  font-size: 60px;
  color: #64748b;
}

.finding-desc {
  flex: 1;
}

.finding-desc p {
  font-size: 26px;
  color: #475569;
  margin-bottom: 8px;
  line-height: 1.4;
}

.stat-note {
  font-size: 20px;
  color: #64748b;
  font-style: italic;
}

.research-implications {
  background: #7373b0;
  color: white;
  padding: 24px;
  border-radius: 12px;
}

.research-implications h4 {
  font-family: 'PT Serif';
  font-size: 28px;
  margin-bottom: 16px;
}

.research-implications ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.research-implications li {
  font-size: 24px;
  padding: 8px 0;
  padding-left: 32px;
  position: relative;
  line-height: 1.5;
}

.research-implications li::before {
  content: "→";
  position: absolute;
  left: 0;
  font-weight: 700;
  font-size: 28px;
}

/* Layout 22: Framework Application Matrix */
.framework-matrix-slide {
  padding: 60px;
}

.matrix-intro {
  font-size: 26px;
  color: #475569;
  margin-bottom: 24px;
  font-style: italic;
}

.framework-matrix {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.framework-matrix thead {
  background: #7373b0;
  color: white;
}

.framework-matrix th {
  padding: 20px 16px;
  text-align: left;
  font-family: 'PT Serif';
  font-size: 24px;
  font-weight: 400;
}

.framework-column {
  width: 20%;
  background: #5a5a8f;
}

.case-column {
  width: 26.67%;
  font-size: 22px;
  line-height: 1.4;
}

.case-result {
  display: block;
  font-size: 20px;
  font-weight: 700;
  margin-top: 8px;
  font-family: 'Roboto';
}

.case-result.success { color: #d1fae5; }
.case-result.failure { color: #fee2e2; }
.case-result.mixed { color: #fef3c7; }

.framework-matrix tbody tr {
  border-bottom: 1px solid #e2e8f0;
}

.framework-matrix tbody tr:last-child {
  border-bottom: none;
}

.framework-matrix tbody tr:hover {
  background: #f8fafc;
}

.framework-label {
  font-family: 'PT Serif';
  font-size: 24px;
  font-weight: 600;
  color: #7373b0;
  padding: 16px;
  background: #f8fafc;
}

.case-cell {
  padding: 16px;
  font-size: 21px;
  color: #475569;
  line-height: 1.5;
  vertical-align: top;
}

.matrix-insight {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #78350f;
}

.matrix-insight strong {
  color: #92400e;
  font-weight: 700;
}

/* Layout 23: Reflection / Journal Prompt */
.reflection-slide {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 60px;
}

.reflection-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.reflection-icon {
  color: #7373b0;
  opacity: 0.6;
  margin-bottom: 20px;
}

.reflection-prompt {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  border-left: 4px solid #7373b0;
}

.prompt-intro {
  font-size: 26px;
  color: #475569;
  font-style: italic;
  margin: 0;
}

.reflection-questions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.reflection-question {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.3s ease;
}

.reflection-question:hover {
  box-shadow: 0 6px 16px rgba(115, 115, 176, 0.2);
  transform: translateX(8px);
}

.question-number {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #7373b0;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'PT Serif';
  font-size: 28px;
  font-weight: 700;
}

.question-content {
  flex: 1;
}

.question-content h3 {
  font-family: 'PT Serif';
  font-size: 26px;
  color: #7373b0;
  margin-bottom: 8px;
  font-weight: 600;
}

.question-content p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
  margin: 0;
}

.reflection-footer {
  background: #7373b0;
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.reflection-footer p {
  font-size: 24px;
  margin: 0;
}

/* Layout 24: Group Assignment Brief */
.group-assignment-slide {
  padding: 60px;
}

.assignment-overview {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
}

.overview-section {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  color: #475569;
}

.icon-badge {
  font-size: 36px;
}

.scenario-box {
  background: linear-gradient(135deg, #7373b0 0%, #8b87c7 100%);
  color: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.scenario-box h3 {
  font-family: 'PT Serif';
  font-size: 32px;
  margin-bottom: 12px;
}

.scenario-box p {
  font-size: 26px;
  line-height: 1.5;
  margin: 0;
}

.roles-timeline {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.roles-section,
.timeline-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
}

.roles-section h3,
.timeline-section h3 {
  font-family: 'PT Serif';
  font-size: 28px;
  color: #7373b0;
  margin-bottom: 16px;
}

.roles-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.roles-list li {
  font-size: 22px;
  color: #475569;
  padding: 8px 0;
  line-height: 1.4;
}

.roles-list strong {
  color: #7373b0;
  font-weight: 600;
}

.timeline-step {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.time-badge {
  flex-shrink: 0;
  background: #7373b0;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: 700;
  font-family: 'PT Serif';
  min-width: 100px;
  text-align: center;
}

.step-desc {
  font-size: 22px;
  color: #475569;
  line-height: 1.4;
}

.success-criteria {
  background: #d1fae5;
  border-left: 4px solid #10b981;
  padding: 24px;
  border-radius: 12px;
}

.success-criteria h3 {
  font-family: 'PT Serif';
  font-size: 28px;
  color: #065f46;
  margin-bottom: 16px;
}

.success-criteria ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.success-criteria li {
  font-size: 22px;
  color: #065f46;
  font-weight: 500;
}

/* Layout 25: Assessment Checklist / Success Criteria */
.assessment-checklist-slide {
  padding: 60px;
}

.assessment-header {
  display: flex;
  gap: 30px;
  background: #7373b0;
  color: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  justify-content: space-around;
}

.header-item {
  font-size: 24px;
}

.header-item strong {
  font-weight: 700;
}

.checklist-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 24px;
}

.checklist-category {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  color: white;
}

.category-header.excellent { background: #10b981; }
.category-header.good { background: #3b82f6; }
.category-header.satisfactory { background: #f59e0b; }
.category-header.basic { background: #64748b; }

.category-header h3 {
  font-family: 'PT Serif';
  font-size: 28px;
  margin: 0;
}

.points {
  font-size: 22px;
  font-weight: 700;
  font-family: 'Roboto';
}

.checklist-items {
  list-style: none;
  padding: 20px 24px;
  margin: 0;
}

.checklist-items li {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 12px 0;
  font-size: 23px;
  color: #475569;
  line-height: 1.5;
  border-bottom: 1px solid #f1f5f9;
}

.checklist-items li:last-child {
  border-bottom: none;
}

.check-box {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  margin-top: 4px;
  cursor: pointer;
  accent-color: #7373b0;
}

.checklist-items strong {
  color: #1e293b;
  font-weight: 600;
}

.final-reminder {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #78350f;
}

.final-reminder strong {
  font-weight: 700;
  color: #92400e;
}
```

---

## Implementation Notes

### Using Educational Layouts

**Layout Selection Logic:**
1. Check content for educational markers (keywords, structure patterns)
2. Match to most specific layout first (e.g., vocab table before standard content)
3. Fall back to base layouts if no educational match
4. Consider combining layouts (e.g., case study followed by discussion prompt)

**Best Practices:**
- Use Tier 1 layouts for core pedagogical needs (vocabulary, activities, rubrics)
- Use Tier 2 layouts for process/analysis work (timelines, cases, objectives)
- Use Tier 3 layouts for advanced pedagogy (research, frameworks, reflection, group work)
- Maintain consistency within a presentation (don't overuse variety)
- Always connect educational layouts to assessments when relevant

**Accessibility Reminders:**
- All color-coded elements have redundant cues (icons, text labels, patterns)
- Tables include proper semantic HTML (thead, tbody, th, td)
- Interactive elements (checkboxes) have proper cursor and hover states
- Text contrast ratios exceed WCAG AA standards throughout
- Font sizes appropriate for projection viewing (minimum 22px for body text)

