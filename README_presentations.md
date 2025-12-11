# Musical Sequence Interactive Presentations

Generate beautiful, interactive HTML presentations from your musical sequence JSON files. Perfect for presenting workflows to your team with a progressive disclosure experience!

## 🎯 Overview

The presentation tool transforms verbose sequence documentation into an engaging, collapsible navigation interface where you can:

- **Expand movements** to reveal their beats
- **Expand beats** to see handlers, tests, acceptance criteria, and more
- **Collapse sections** as you move through the presentation
- **Navigate smoothly** with auto-scrolling and keyboard shortcuts

## 🚀 Quick Start

### Generate a Presentation

```bash
# Single sequence
python scripts/generate_sequence_presentation.py sequences/hybrid-resume-generation.sequence.json

# Multiple sequences
python scripts/generate_sequence_presentation.py sequences/*.sequence.json

# Custom output directory
python scripts/generate_sequence_presentation.py sequences/hybrid-resume-generation.sequence.json --output-dir my-presentations
```

### View the Presentation

Open the generated HTML file in any modern web browser:

```bash
# Default location: presentations/<sequence-id>.presentation.html
open presentations/hybrid-resume-generation.presentation.html
```

## ✨ Features

### Progressive Disclosure Experience

The presentation automatically guides your audience through the workflow:

1. **First view**: See the sequence overview with metadata, purpose, and governance
2. **Expand a movement**: Click any movement to reveal its beats
3. **Expand a beat**: Click any beat to see detailed information:
   - Handler details (name, source path, capabilities)
   - User stories
   - Acceptance criteria (Given/When/Then)
   - Test file references
4. **Navigate**: Sections auto-scroll into view when expanded
5. **Clean up**: Collapse previous sections as you move forward

### Interactive Controls

- **Expand All** button - Show everything at once
- **Collapse All** button - Reset to overview
- **ESC key** - Quick collapse all sections
- **Auto-collapse siblings** - When you expand a movement/beat, its siblings collapse automatically

### Beautiful Design

- **Dark theme** optimized for presentations
- **Color-coded sections**:
  - Movements: Blue accents
  - Beats: Orange/amber accents
  - User stories: Blue gradient
  - Acceptance criteria: Green accents
- **Smooth animations** for all transitions
- **Responsive layout** works on any screen size

## 🎨 What's Included in the Presentation

### Header Section
- Sequence name and title
- Description
- Key metadata in a grid layout

### Metadata Cards
- Sequence ID, Domain, Package
- Musical properties (Key, Tempo, Time Signature)
- Total beats count
- Status

### Purpose & Context
- Purpose statement
- Trigger event
- Business value

### User Story
- Sequence-level user story (As a... I want to... So that...)

### Governance
- Policies list
- Metrics list

### Event Flow
- All events emitted by the sequence in order

### Movements (Collapsible)
Each movement shows:
- Movement number and name
- Beat count badge
- Description
- Movement properties (ID, tempo, error handling, status)
- Movement-level user story
- **Collapsible beats** within each movement

### Beats (Collapsible)
Each beat shows:
- Beat number, name, and event
- Description
- **Handler details** (name, source path, capabilities)
- **User story** (beat-level)
- **Acceptance criteria** (Given/When/Then scenarios)
- **Test file** reference

## 🎬 Presentation Tips

### For Live Presentations

1. **Start collapsed**: The presentation auto-expands the first movement after load
2. **Go movement-by-movement**: Expand each movement as you discuss it
3. **Deep-dive on key beats**: Expand beats when you need to show implementation details
4. **Use Collapse All**: Reset between major sections or Q&A

### For Documentation

1. **Use Expand All**: Generate a full view for reference
2. **Share the HTML**: Single-file presentations are easy to distribute
3. **No dependencies**: All CSS/JS is embedded, works offline

### Keyboard Shortcuts

- `ESC` - Collapse all sections
- `Click` - Toggle section expand/collapse

## 📊 Comparison with Markdown Reports

| Feature | Markdown Report | HTML Presentation |
|---------|----------------|-------------------|
| **Format** | Static markdown | Interactive HTML |
| **Navigation** | Scroll through all content | Expand/collapse on demand |
| **Presentation** | Verbose, overwhelming | Progressive disclosure |
| **File size** | Text only | Single-file HTML |
| **Use case** | Deep documentation | Live presentations, exploration |
| **Accessibility** | Easy to read linearly | Better for selective viewing |

## 🔧 Customization

The presentation uses CSS variables for easy theming. Edit the `:root` section in the generated CSS to customize colors:

```css
:root {
    --primary-color: #2563eb;      /* Blue - movements */
    --secondary-color: #7c3aed;    /* Purple - details */
    --success-color: #059669;      /* Green - criteria */
    --accent-color: #f59e0b;       /* Orange - beats/events */
    --bg-color: #0f172a;           /* Dark background */
    --card-bg: #1e293b;            /* Card background */
}
```

## 📝 Example Output

Generated presentations are saved to:
```
presentations/
├── hybrid-resume-generation.presentation.html
├── surgical-resume-update.presentation.html
└── ...
```

Each file is a complete, self-contained HTML presentation with:
- Embedded CSS (no external stylesheets)
- Embedded JavaScript (no external scripts)
- Works offline
- No build step required

## 🎓 When to Use This Tool

**Use the presentation tool when:**
- Presenting workflow sequences to stakeholders
- Training team members on new sequences
- Reviewing sequence design interactively
- Exploring complex workflows step-by-step

**Use the markdown report tool when:**
- Creating comprehensive documentation
- Generating reference materials
- Archiving sequence specifications
- Preparing detailed technical specs

## 🤝 Integration with Existing Tools

Works alongside your existing workflow:

1. **JSON sequences** → Define your workflows
2. **Markdown reports** (`generate_sequence_report.py`) → Generate documentation
3. **HTML presentations** (`generate_sequence_presentation.py`) → Create interactive presentations

All three formats serve different needs and complement each other!

## 🎉 Happy Presenting!

Your musical sequences just got a lot more presentable. Enjoy showcasing your workflows with style! 🎵✨
