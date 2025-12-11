@echo off
REM Generate Interactive HTML Presentations for Musical Sequences
REM Usage: generate-presentations.bat

echo.
echo ========================================
echo Musical Sequence Presentation Generator
echo ========================================
echo.

if not exist "presentations" (
    echo Creating presentations directory...
    mkdir presentations
)

echo Generating presentations for all sequences...
echo.

.venv\Scripts\python.exe scripts\generate_sequence_presentation.py sequences\*.sequence.json

echo.
echo ========================================
echo Generation Complete!
echo ========================================
echo.
echo Presentations saved to: presentations\
echo.
echo To view a presentation, open any .html file in your browser:
dir /b presentations\*.presentation.html
echo.

pause
