# Resume Editor Web Interface

A modern, responsive web application for managing your master resume data.

## Quick Start

1. **Start the API server:**
   ```bash
   cd ../..
   python src/api/app.py
   ```

2. **Open the web interface:**
   - Option 1: Open `index.html` directly in your browser
   - Option 2: Use a local server:
     ```bash
     python -m http.server 8080
     ```
     Then navigate to `http://localhost:8080`

## Files

- **index.html** - Main HTML structure and layout
- **app.js** - Application logic and API integration
- **styles.css** - Responsive styling and themes

## Features

### Resume Management
- ✅ Edit all resume sections
- ✅ Add/remove experience entries
- ✅ Manage education and certifications
- ✅ Tag management for skills

### Data Safety
- ✅ Automatic backups on save
- ✅ Manual backup creation
- ✅ Backup history viewer
- ✅ One-click restoration

### User Experience
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Real-time validation
- ✅ Unsaved changes warning
- ✅ Intuitive navigation

## Configuration

### API Endpoint
The API base URL is configured in `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

Change this if your API server runs on a different host/port.

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Development

### Code Structure

```
app.js
├── Configuration
│   └── API_BASE_URL
├── State Management
│   ├── resumeData
│   ├── currentSection
│   └── hasUnsavedChanges
├── API Functions
│   ├── loadResumeData()
│   ├── saveResumeData()
│   ├── validateResumeData()
│   ├── createBackup()
│   ├── loadBackups()
│   └── restoreBackup()
├── Render Functions
│   ├── renderBasicInfo()
│   ├── renderSummary()
│   ├── renderTechnicalProficiencies()
│   ├── renderAreasOfExpertise()
│   ├── renderExperience()
│   ├── renderEducation()
│   └── renderCertifications()
└── Utility Functions
    ├── showAlert()
    ├── navigateToSection()
    └── collectFormData()
```

### Adding New Sections

1. Add section to HTML navigation
2. Create section container in HTML
3. Add render function in `app.js`
4. Add to `renderAllSections()`
5. Update `collectFormData()` if needed

### Styling

The application uses Bootstrap 5 for base styling with custom CSS in `styles.css`.

Key CSS classes:
- `.content-section` - Main section containers
- `.experience-card` - Experience entry cards
- `.bullet-item` - Accomplishment bullets
- `.tag-badge` - Technology tags

## Troubleshooting

### "Failed to load resume data"
- Ensure API server is running on port 5000
- Check browser console for CORS errors
- Verify `data/master_resume.json` exists

### Changes not saving
- Check API server logs
- Verify file permissions on `data/` directory
- Check browser console for errors

### UI not updating
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- Clear browser cache
- Check for JavaScript errors in console

## Keyboard Shortcuts

- **Ctrl/Cmd + S** - Save changes (coming soon)
- **Esc** - Close modals

## Accessibility

The interface follows WCAG 2.1 guidelines:
- ✅ Keyboard navigation
- ✅ Focus indicators
- ✅ ARIA labels
- ✅ Semantic HTML
- ✅ Color contrast compliance

## Performance

- Lazy loading of sections
- Debounced auto-save (coming soon)
- Optimized re-renders
- Minimal dependencies

## Security Notes

⚠️ **This interface is designed for local use only.**

For production deployment:
- Add authentication
- Implement HTTPS
- Sanitize all inputs
- Add CSRF protection
- Implement rate limiting

## Contributing

When modifying the web interface:

1. Test on multiple browsers
2. Verify responsive design
3. Check accessibility
4. Update documentation
5. Follow existing code style

## Related Documentation

- [Full Documentation](../../docs/RESUME_EDITOR_WEB_INTERFACE.md)
- [API Documentation](../../docs/RESUME_EDITOR_WEB_INTERFACE.md#api-documentation)
- [GitHub Issue #2](https://github.com/BPMSoftwareSolutions/agentic-resume-tailor/issues/2)

