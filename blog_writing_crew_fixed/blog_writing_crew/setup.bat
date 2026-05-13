@echo off
REM ============================================================
REM  Blog Writing Crew - Windows Setup Script
REM  Run this ONCE to set up. Then use run.bat to start the crew.
REM ============================================================

echo [1/4] Creating virtual environment with uv...
uv venv .venv
if errorlevel 1 (
    echo ERROR: uv not found. Install it with: pip install uv
    pause
    exit /b 1
)

echo [2/4] Installing crewai and tools...
uv pip install "crewai[tools]==1.14.4"
if errorlevel 1 goto :error

echo [3/4] Installing litellm (needed for Groq support)...
uv pip install "litellm>=1.83.7"
if errorlevel 1 goto :error

echo [4/4] Installing the project itself...
uv pip install -e .
if errorlevel 1 goto :error

echo.
echo ============================================================
echo  Setup complete!
echo  Run the crew with:   run.bat
echo  Or directly with:    python run.py
echo ============================================================
pause
exit /b 0

:error
echo.
echo ERROR during setup. See message above.
pause
exit /b 1
