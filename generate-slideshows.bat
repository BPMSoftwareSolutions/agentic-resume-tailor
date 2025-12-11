@echo off
REM Generate HTML Slideshows for Musical Sequences
REM Usage: generate-slideshows.bat

echo.
echo ========================================
echo Musical Sequence Slideshow Generator
echo ========================================
echo.

if not exist "slideshows" (
    echo Creating slideshows directory...
    mkdir slideshows
)

echo Generating slideshows for all sequences...
echo.

.venv\Scripts\python.exe scripts\generate_sequence_slideshow.py sequences\*.sequence.json

echo.
echo ========================================
echo Generation Complete!
echo ========================================
echo.
echo Slideshows saved to: slideshows\
echo.
echo To present a slideshow, open any .html file in your browser:
dir /b slideshows\*.slideshow.html
echo.
echo Navigation Tips:
echo   - Arrow keys or Space to navigate
echo   - ESC for overview mode
echo   - F for full-screen
echo   - ? for help
echo.

pause
