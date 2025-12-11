# Musical Sequence Slideshows 🎬

Transform your musical sequence JSON files into professional, presentation-ready HTML slideshows powered by Reveal.js!

## 🎯 Overview

The slideshow generator creates beautiful, navigable presentations that walk through your sequence workflows step-by-step. Perfect for stakeholder presentations, team training, and workflow walkthroughs!

### What You Get

Each slideshow contains:
- **Title Slide** - Sequence name and overview
- **Overview Slide** - Purpose, trigger, and metadata
- **User Story Slide** - Domain/service/workflow level story
- **Governance Slide** - Policies and metrics
- **Movements Summary** - List of all movements
- **Per-Movement Slides**:
  - Movement divider (section break)
  - Beats summary for that movement
  - **Per-Beat Slides (3 slides per beat)**:
    - User Story slide
    - Acceptance Criteria slide
    - Handler Summary slide (source, event, tests)
- **End Slide** - Thank you and navigation tips

## 🚀 Quick Start

### Generate a Slideshow

```bash
# Single sequence
python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json

# Multiple sequences
python scripts/generate_sequence_slideshow.py sequences/*.sequence.json

# Custom output directory
python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json --output-dir my-slideshows
```

### Present Your Slideshow

Open the generated HTML file in any modern web browser and start presenting!

```bash
# Default location: slideshows/<sequence-id>.slideshow.html
open slideshows/hybrid-resume-generation.slideshow.html
```

## 🎨 Slideshow Features

### Professional Design

- **Modern UI** - Dark theme with gradient accents
- **Typography** - Inter for text, JetBrains Mono for code
- **Color-coded sections**:
  - 🔵 Primary (Blue) - Movements, main content
  - 🟣 Secondary (Purple) - Details, handlers
  - 🟠 Accent (Orange) - Beats, events
  - 🟢 Success (Green) - Acceptance criteria
- **Smooth animations** - Slide and fade transitions
- **Responsive** - 16:9 aspect ratio, optimized for 1280×720

### Navigation

- **Arrow keys** - Navigate forward/back
- **Space** - Next slide
- **ESC** - Slide overview mode (bird's eye view!)
- **Slide numbers** - Shows current/total (e.g., 15/47)
- **Progress bar** - Visual indicator at bottom
- **Touch support** - Swipe on mobile/tablets

### Reveal.js Integration

Powered by Reveal.js, the industry-standard HTML presentation framework:
- Speaker notes support
- PDF export capability
- Full-screen mode (F key)
- Jump to slide (G key + slide number)
- Pause presentation (B or . key)

## 📊 Slide Breakdown

### Example: Hybrid Resume Generation Sequence

For a sequence with 3 movements and 12 beats, you get approximately:

```
1. Title Slide
2. Overview
3. User Story
4. Governance
5. Movements Summary (all 3)
6. Movement 1 Divider
7. Movement 1 Beats Summary
8-19. Movement 1 Beats (4 beats × 3 slides = 12)
20. Movement 2 Divider
21. Movement 2 Beats Summary
22-36. Movement 2 Beats (5 beats × 3 slides = 15)
37. Movement 3 Divider
38. Movement 3 Beats Summary
39-44. Movement 3 Beats (2 beats × 3 slides = 6)
45. End Slide

Total: ~45 slides
```

### Slide Templates

#### Title Slide
- Large gradient title
- Subtitle and description
- Version and author info

#### Overview Slide
- Metadata grid (Key, Tempo, Beats)
- Purpose box
- Trigger box

#### User Story Slide
- Formatted "As a... I want to... So that..." layout
- Business value section (if available)

#### Governance Slide
- Policies as tags
- Metrics as tags
- Two-column layout

#### Movements Summary
- Grid of movement cards
- Each shows: number, name, description, beat count

#### Movement Divider
- Large centered section break
- Movement number and name
- Full-screen visual separator

#### Movement Beats Summary
- List of beats in the movement
- Each shows: beat number, name, event

#### Beat User Story Slide
- Beat description
- User story (As a... I want to... So that...)

#### Beat Acceptance Criteria Slide
- Given/When/Then/And sections
- Checkmark bullets
- Multiple scenarios supported

#### Beat Handler Summary Slide
- Handler name and source path
- Event and test file
- Capabilities as tags (if available)
- 2×2 grid layout

#### End Slide
- Thank you message
- Navigation tips

## 🎓 Presenting Tips

### Before Your Presentation

1. **Test your slideshow** - Open and navigate through once
2. **Full-screen mode** - Press F for immersive presenting
3. **Check slide count** - Note key slides for Q&A
4. **Practice navigation** - Get comfortable with arrow keys

### During Your Presentation

1. **Start with overview** (press ESC) - Show the big picture
2. **Navigate linearly** - Arrow keys through the story
3. **Jump to slides** - Press G + number for specific beats
4. **Pause when needed** - Press B or . to pause
5. **Use overview mode** - ESC for quick navigation

### Keyboard Shortcuts Reference

| Key | Action |
|-----|--------|
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `ESC` | Slide overview |
| `F` | Full-screen mode |
| `S` | Speaker notes view |
| `B` / `.` | Pause/blackout |
| `G` | Go to slide (type number) |
| `?` | Show keyboard help |

## 🎬 Slide Content Details

### Metadata Cards
Shows at a glance:
- Musical key (e.g., "C major")
- Tempo (e.g., "120 BPM")
- Total beats in sequence

### Content Boxes
Color-coded boxes for:
- Purpose statements
- Trigger events
- Descriptions
- Business value

### Movement Cards
Each movement shows:
- Large number badge
- Movement name
- Short description
- Beat count badge

### Beat Cards
Each beat shows:
- Beat number
- Beat name
- Event in monospace font

### Handler Grid
2×2 grid showing:
- Handler name (function/module)
- Event emitted
- Source file path
- Test file path
- Capabilities (as tags)

### Acceptance Criteria
Structured format:
- **Given:** Preconditions (green checkmarks)
- **When:** Actions taken
- **Then:** Expected outcomes
- **And:** Additional conditions

## 🔧 Customization

### Theme Colors

The slideshow uses CSS variables. Edit the `:root` section to customize:

```css
:root {
    --primary: #3b82f6;      /* Blue - primary accents */
    --secondary: #8b5cf6;    /* Purple - secondary accents */
    --accent: #f59e0b;       /* Orange - beats/events */
    --success: #10b981;      /* Green - criteria */
    --dark: #0f172a;         /* Background */
    --dark-alt: #1e293b;     /* Card backgrounds */
}
```

### Reveal.js Configuration

Edit the `Reveal.initialize()` call to customize:
- Transition effects
- Slide dimensions
- Auto-slide timing
- Controls visibility
- Progress bar
- Slide numbers

## 📦 Output Format

### File Structure
```
slideshows/
├── hybrid-resume-generation.slideshow.html
├── surgical-resume-update.slideshow.html
└── ...
```

### File Characteristics
- **Format:** Single HTML file
- **Size:** ~75-90 KB per sequence
- **Dependencies:** CDN-hosted Reveal.js (requires internet)
- **Compatibility:** All modern browsers
- **Offline:** Possible with local Reveal.js copy

## 🎭 Use Cases

### When to Use Slideshows

**Perfect for:**
- 📊 Stakeholder presentations
- 🎓 Team training sessions
- 👥 Client walkthroughs
- 🔍 Workflow reviews
- 📱 Screen sharing / remote demos
- 🎤 Conference presentations

**Not ideal for:**
- Quick reference (use markdown reports)
- Detailed documentation (use markdown reports)
- Deep technical reading (use interactive presentations)

## 🆚 Comparison: Three Presentation Formats

| Feature | Markdown Report | Interactive Presentation | **Slideshow** |
|---------|----------------|-------------------------|---------------|
| **Format** | Static MD | Collapsible HTML | Slide-based HTML |
| **Navigation** | Scroll | Expand/collapse | Slide forward/back |
| **Best for** | Documentation | Exploration | **Linear presentations** |
| **Interactivity** | None | High | Medium |
| **Print friendly** | ✅ Yes | ❌ No | ⚠️ Partial |
| **Presentation mode** | ❌ No | ⚠️ Partial | ✅ **Full-featured** |
| **Overview mode** | ❌ No | ❌ No | ✅ **Yes (ESC)** |
| **Dependencies** | None | None | CDN (internet) |
| **File size** | Smallest | Medium | Medium |
| **Slide count** | N/A | N/A | **~30-60 slides** |

## 🎁 Bonus Features

### PDF Export

Generate PDF from your slideshow (requires Chrome/Chromium):

```bash
# Add ?print-pdf to the URL
open slideshows/hybrid-resume-generation.slideshow.html?print-pdf

# Then: File → Print → Save as PDF
```

### Speaker Notes

Add speaker notes to slides (future enhancement):
```html
<aside class="notes">
    Remember to emphasize the scalability here!
</aside>
```

### Custom Slide Order

Skip slides by removing sections from the generator code or manually editing the HTML.

## 📝 Example Workflow

```bash
# 1. Generate slideshow
python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json

# 2. Open in browser
open slideshows/hybrid-resume-generation.slideshow.html

# 3. Practice presenting
#    - Use arrow keys to navigate
#    - Press ESC for overview
#    - Press F for full-screen

# 4. Present!
#    - Connect to projector/screen share
#    - Press F for full-screen
#    - Navigate through your sequence story
```

## 🎉 Generated Output

For `hybrid-resume-generation.sequence.json`:
- **File:** `slideshows/hybrid-resume-generation.slideshow.html`
- **Size:** ~75 KB
- **Slides:** ~45-50 slides
- **Includes:** All movements, beats, stories, criteria, handlers

For `surgical-resume-update.sequence.json`:
- **File:** `slideshows/surgical-resume-update.slideshow.html`
- **Size:** ~86 KB
- **Slides:** ~50-60 slides
- **Includes:** Complete workflow walkthrough

## 🚀 Advanced Usage

### Batch Generate All Slideshows

```bash
python scripts/generate_sequence_slideshow.py sequences/*.sequence.json
```

### Custom Output Directory

```bash
python scripts/generate_sequence_slideshow.py sequences/hybrid-resume-generation.sequence.json --output-dir presentations/2024-q4
```

### Integration with CI/CD

```yaml
# .github/workflows/generate-docs.yml
- name: Generate Slideshows
  run: |
    python scripts/generate_sequence_slideshow.py sequences/*.sequence.json

- name: Upload Slideshows
  uses: actions/upload-artifact@v3
  with:
    name: slideshows
    path: slideshows/
```

## 🎊 Happy Presenting!

Your musical sequences are now ready for the big screen! Present your workflows with confidence and style. 🎵✨

**Pro tip:** Press `?` during your slideshow to see all available keyboard shortcuts!
