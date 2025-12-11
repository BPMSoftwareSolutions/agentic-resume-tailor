# Acceptance Criteria - GitHub-Style Update 🎨

## Overview

The acceptance criteria sections have been completely redesigned to match GitHub's modern card/table style for a cleaner, more professional developer experience.

## What Changed

### Before (Original Design)
```
┌─────────────────────────────────────────┐
│ Green translucent background            │
│ • Left border accent (4px green)        │
│ • Round corners (12px)                  │
│ • Checkmarks floating in padding        │
│ • Loose spacing                         │
│ • Text fades to dimmed color            │
└─────────────────────────────────────────┘
```

### After (GitHub Card Style)
```
┌──────────────────────────────────────────┐
│ GIVEN                   │ Dark header    │
├──────────────────────────────────────────┤
│ ✓ Condition 1           │ List items     │
│ ✓ Condition 2           │ with borders   │
├──────────────────────────────────────────┤
│ WHEN                    │ Section header │
├──────────────────────────────────────────┤
│ ✓ Action taken          │                │
├──────────────────────────────────────────┤
│ THEN                    │ Section header │
├──────────────────────────────────────────┤
│ ✓ Expected outcome 1    │                │
│ ✓ Expected outcome 2    │                │
└──────────────────────────────────────────┘
```

## Design Improvements

### 1. **Card Container**
- Clean bordered card with rounded corners (6px)
- Single border (`1px solid #30363d`)
- No padding on container (content fills to edges)
- Overflow hidden for clean borders

### 2. **Section Headers (Given/When/Then/And)**
- Dark background (`#010409`) like GitHub code blocks
- Uppercase labels with letter-spacing (1.5px)
- Green color (`#3fb950`) for visibility
- Top border separator for sections
- Compact padding (0.75rem vertical)

### 3. **List Items**
- Individual borders between items (`#21262d`)
- Full-width clickable feel
- Left-aligned checkmarks (1.25rem from edge)
- Proper line-height (1.6) for readability
- Last item has no bottom border

### 4. **Checkmarks**
- Larger size (1.3em)
- Green color (`#3fb950`)
- Fixed position from left
- Bold weight

### 5. **Scenario Headers** (for multiple scenarios)
- Dark background like section headers
- Thicker top border (2px) for separation
- Medium font weight (600)
- Clear visual break between scenarios

## Visual Hierarchy

```
Slide Title (h2)
  ↓
Beat Name (h3, dimmed)
  ↓
┌─ Criteria Card ────────────┐
│ GIVEN (header)             │
│ ├─ Item 1                  │
│ ├─ Item 2                  │
│ └─ Item 3                  │
│ WHEN (header)              │
│ ├─ Item 1                  │
│ THEN (header)              │
│ ├─ Item 1                  │
│ ├─ Item 2                  │
│ └─ Item 3                  │
└────────────────────────────┘
```

## CSS Breakdown

### Container
```css
.criteria-section {
  background: #161b22;           /* GitHub subtle canvas */
  border: 1px solid #30363d;     /* GitHub default border */
  border-radius: 6px;            /* GitHub standard radius */
  padding: 0;                     /* No padding, full bleed */
  overflow: hidden;               /* Clean corners */
}
```

### Section Labels
```css
.criteria-label {
  background: #010409;           /* Darker inset background */
  padding: 0.75rem 1.25rem;      /* Compact but breathable */
  font-weight: 600;              /* Semi-bold */
  color: #3fb950;                /* GitHub success green */
  font-size: 0.75em;             /* Smaller, uppercase */
  text-transform: uppercase;
  letter-spacing: 1.5px;         /* Spaced for readability */
  border-bottom: 1px solid #30363d;
}
```

### List Items
```css
.criteria-list li {
  padding: 0.75rem 1.25rem 0.75rem 3rem;  /* Room for checkmark */
  font-size: 0.75em;                      /* Readable size */
  color: #e6edf3;                         /* Full brightness */
  border-bottom: 1px solid #21262d;       /* Muted separator */
  line-height: 1.6;                       /* Comfortable reading */
}

.criteria-list li::before {
  content: "✓";
  left: 1.25rem;             /* Fixed from edge */
  color: #3fb950;            /* Green checkmark */
  font-size: 1.3em;          /* Prominent */
}
```

## Comparison Examples

### Example: Beat 1 Acceptance Criteria

**Before:**
- Floating green box
- Dimmed text
- Loose checkmarks
- Less structured

**After:**
- Clean card with borders
- Bright text on dark background
- Organized sections with headers
- Table-like structure
- Professional GitHub feel

### Multiple Scenarios

When there are multiple scenarios, the new design adds scenario headers:

```
┌───────────────────────────────────────────┐
│ Scenario 1                │ Header         │
├───────────────────────────────────────────┤
│ GIVEN                     │                │
├───────────────────────────────────────────┤
│ ✓ Precondition            │                │
├───────────────────────────────────────────┤
│ THEN                      │                │
├───────────────────────────────────────────┤
│ ✓ Expected outcome        │                │
├───────────────────────────────────────────┤
│ Scenario 2                │ New header     │
├───────────────────────────────────────────┤
│ ...                       │                │
└───────────────────────────────────────────┘
```

## Benefits

### For Developers
1. **Familiar**: Looks like GitHub tables/cards
2. **Scannable**: Clear sections with headers
3. **Organized**: Bordered items, easy to track
4. **Professional**: Clean, modern design

### For Presentations
1. **Readable**: High contrast, clear structure
2. **Focused**: Each section stands out
3. **Clean**: No visual clutter
4. **Consistent**: Matches other GitHub-styled elements

## Typography

- **Section headers**: 0.75em, uppercase, 600 weight, green
- **List items**: 0.75em, normal weight, full brightness
- **Checkmarks**: 1.3em, bold, green
- **Line height**: 1.6 for comfortable reading

## Colors Used

| Element | Color | Usage |
|---------|-------|-------|
| **Container background** | `#161b22` | GitHub subtle canvas |
| **Container border** | `#30363d` | GitHub default border |
| **Section header bg** | `#010409` | GitHub inset (darkest) |
| **Section header text** | `#3fb950` | GitHub success green |
| **List item text** | `#e6edf3` | GitHub default foreground |
| **List item border** | `#21262d` | GitHub muted border |
| **Checkmarks** | `#3fb950` | GitHub success green |

## Technical Implementation

### HTML Structure
```html
<div class="criteria-section">
  <!-- Optional scenario header for multiple scenarios -->
  <div class="criteria-scenario">Scenario 1</div>

  <!-- Given section -->
  <div class="criteria-label">GIVEN</div>
  <ul class="criteria-list">
    <li>Resume JSON file exists at specified path</li>
    <li>File contains valid JSON structure</li>
  </ul>

  <!-- When section -->
  <div class="criteria-label">WHEN</div>
  <ul class="criteria-list">
    <li>The system reads the JSON file</li>
  </ul>

  <!-- Then section -->
  <div class="criteria-label">THEN</div>
  <ul class="criteria-list">
    <li>Resume data is successfully parsed</li>
    <li>All required fields are present</li>
    <li>Data structure is valid</li>
  </ul>
</div>
```

### Border Strategy
- Container: 1px solid border
- Headers: Bottom border (1px)
- List items: Bottom border (1px), except last
- Scenario headers: Top border (2px, thicker) for emphasis

## Before/After Metrics

| Metric | Before | After |
|--------|--------|-------|
| **Visual weight** | Light | Strong |
| **Structure** | Loose | Tight |
| **Scannability** | Medium | High |
| **GitHub similarity** | Low | High |
| **Professional feel** | Good | Excellent |
| **Border usage** | Minimal | Structured |
| **Spacing** | Loose | Compact |
| **Readability** | Good | Better |

## Responsive Design

The card design scales well:
- Headers remain readable
- Items maintain structure
- Checkmarks stay aligned
- Borders provide clear boundaries

## Accessibility

Improvements:
- ✅ Higher contrast (full brightness text)
- ✅ Clear section headers
- ✅ Structured list format
- ✅ Consistent spacing
- ✅ Semantic HTML structure

## Usage in Slideshows

Every beat with acceptance criteria now displays:
1. **Slide header**: "Beat X: [Name]"
2. **Subheader**: "Acceptance Criteria"
3. **One or more criteria cards**: Each with Given/When/Then/And sections
4. **Scenario headers**: If multiple scenarios exist

## Summary

The new acceptance criteria design:
- ✅ Matches GitHub's card/table aesthetic
- ✅ Provides better visual hierarchy
- ✅ Improves scannability during presentations
- ✅ Looks professional and modern
- ✅ Maintains consistency with other GitHub-styled elements
- ✅ Uses proper GitHub color palette
- ✅ Creates a familiar developer experience

Perfect for presenting technical workflows to developer audiences! 🎉
