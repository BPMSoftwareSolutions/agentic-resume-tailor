# GitHub-Style Slideshow Update 🎨

## Overview

The slideshow generator has been updated with **GitHub-inspired styling** to make it more professional and developer-friendly! Perfect for presenting to technical audiences.

## What Changed

### 🎨 Visual Updates

#### GitHub Dark Theme Colors
- **Background:** GitHub's dark canvas (`#0d1117`)
- **Cards:** Subtle dark background (`#161b22`)
- **Borders:** GitHub's default borders (`#30363d`)
- **Text:** GitHub's light text (`#e6edf3`)

#### GitHub Color Palette
- **Primary (Blue):** `#2f81f7` - Links, movements, primary actions
- **Success (Green):** `#3fb950` - Metrics, success states, acceptance criteria
- **Warning (Orange):** `#d29922` - Beats, events, highlights
- **Purple:** `#a371f7` - Secondary accents, details
- **Danger (Red):** `#f85149` - Errors, alerts

### 📝 Code Styling

#### Inline Code
- GitHub-style code blocks with dark background
- Monospace font (JetBrains Mono)
- Border styling matching GitHub
- Proper padding and border-radius (6px)

#### Code Blocks with Syntax Highlighting
- **Highlight.js** integration with GitHub Dark theme
- Support for multiple languages:
  - Python
  - JavaScript/TypeScript
  - JSON
  - YAML
  - Bash
- Real syntax highlighting with proper token colors

### 🏷️ GitHub-Style Elements

#### Badges/Tags
- Monospace font for consistency
- GitHub-style rounded borders
- Color-coded by type:
  - **Policies:** Blue borders
  - **Metrics:** Green borders

#### Cards and Content Boxes
- Clean borders (1px solid)
- Subtle box shadows
- Consistent border-radius (6px)
- Left accent borders (3px) for emphasis
- Hover effects on interactive elements

#### GitHub-Style Alerts (Ready to use)
Three alert types available:
- **Note** (ℹ️) - Blue, informational
- **Tip** (💡) - Green, helpful hints
- **Warning** (⚠️) - Orange, cautions

### 🎯 Developer-Friendly Features

#### Typography
- **Inter** font for UI text (clean, modern)
- **JetBrains Mono** for all code (highly readable)
- Proper font weights (400, 500, 600, 700, 900)
- Consistent sizing hierarchy

#### Layout Improvements
- Card-based layouts with subtle shadows
- Hover states for better interactivity
- Consistent spacing and padding
- Better visual hierarchy

## Before & After

### Before (Original)
- Generic dark theme
- Basic blue/purple colors
- Simple borders
- No syntax highlighting

### After (GitHub-Inspired)
- ✅ GitHub Dark theme colors
- ✅ GitHub color palette
- ✅ GitHub-style borders and shadows
- ✅ Highlight.js syntax highlighting
- ✅ Monospace badges
- ✅ Hover effects
- ✅ Professional developer aesthetic

## File Size Impact

```
Before: ~75-86 KB
After:  ~80-91 KB
Increase: ~5 KB (CDN links for Highlight.js)
```

The slight increase is from adding Highlight.js for syntax highlighting - well worth it for the professional code display!

## What Developers Will Notice

### 1. Familiar Look & Feel
The slideshow now looks like GitHub, which developers use daily. This creates instant familiarity and comfort.

### 2. Better Code Readability
- Syntax highlighting makes code snippets clear
- Monospace fonts ensure proper alignment
- GitHub Dark theme is easy on the eyes

### 3. Professional Polish
- Subtle shadows and borders
- Consistent spacing
- Hover effects for interactivity
- Clean, modern aesthetic

### 4. Color-Coded Information
- Blue for primary info (movements, handlers)
- Green for success/metrics
- Orange for beats/events
- Purple for details

## Technical Details

### CSS Variables Used

```css
:root {
  /* GitHub colors */
  --gh-primary: #2f81f7;
  --gh-success: #3fb950;
  --gh-warning: #d29922;
  --gh-canvas-default: #0d1117;
  --gh-canvas-subtle: #161b22;
  --gh-border-default: #30363d;
  --gh-fg-default: #e6edf3;
  --gh-fg-muted: #7d8590;
}
```

### External Dependencies Added

```html
<!-- Syntax highlighting -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
```

### Supported Languages

All major development languages are supported:
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`)
- JSON (`.json`)
- YAML (`.yml`, `.yaml`)
- Bash (`.sh`)

## Usage

No changes to usage! Just regenerate your slideshows:

```bash
# Regenerate with new GitHub styling
python scripts/generate_sequence_slideshow.py sequences/*.sequence.json
```

All existing slideshows have been updated automatically.

## Examples

### Code Block Example
```python
def generate_resume(data: dict) -> str:
    """Generate a professional resume."""
    return render_template(data)
```

Now displays with:
- Syntax highlighting
- GitHub Dark colors
- Proper indentation
- Token-based coloring

### Badge Example
Tags now look like GitHub labels:
- `input-validation` (policy - blue)
- `success-rate` (metric - green)

### Card Example
Content boxes now have:
- Subtle shadows
- GitHub borders
- Clean corners (6px radius)
- Left accent bars (3px)

## Backward Compatibility

✅ All existing features preserved
✅ All navigation works the same
✅ All content displays correctly
✅ Just looks better!

## Future Enhancements

Possible additions:
- GitHub-style task lists with checkboxes
- GitHub-style blockquotes
- More alert types (important, caution)
- Dark/light theme toggle
- GitHub emoji support

## Migration Guide

### For Existing Slideshows

Simply regenerate:
```bash
python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json
```

Old slideshows will be overwritten with the new GitHub-styled versions.

### For Custom Styling

If you've customized colors, update to the new GitHub variables:

```css
/* Old */
--primary: #3b82f6;

/* New */
--gh-primary: #2f81f7;
--primary: var(--gh-primary);
```

## Summary

The slideshow generator now creates presentations that:
- ✅ Look professional and familiar to developers
- ✅ Have proper syntax highlighting
- ✅ Use GitHub's trusted color palette
- ✅ Display code beautifully
- ✅ Match developer tools and workflows

**Perfect for presenting to technical audiences!** 🎉
