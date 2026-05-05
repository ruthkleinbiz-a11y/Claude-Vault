@echo off
:: ZenithMind OS (Cowork) — Upgrade
:: Run this from your NEW ZenithMind-OS-Cowork folder to migrate data from an old version.

setlocal enabledelayedexpansion

set "NEW_DIR=%~dp0"
set "NEW_DIR=%NEW_DIR:~0,-1%"

set "NEW_VERSION=unknown"
if exist "%NEW_DIR%\VERSION" (
    set /p NEW_VERSION=<"%NEW_DIR%\VERSION"
)

echo ═══════════════════════════════════════════════════════
echo   ZenithMind OS (Cowork) — Upgrade to v%NEW_VERSION%
echo ═══════════════════════════════════════════════════════
echo.

:: ─── Check if this folder already has user data ─────────────────────────

if exist "%NEW_DIR%\session-progress.md" (
    findstr /c:"Current Lesson" "%NEW_DIR%\session-progress.md" >nul 2>&1
    if not errorlevel 1 (
        echo This folder already has session data.
        echo If you've already migrated, you're good to go.
        echo.
        set /p CONFIRM="Continue anyway and overwrite? (y/N): "
        if /i not "!CONFIRM!"=="y" (
            echo Upgrade cancelled. Your existing data is untouched.
            goto :eof
        )
        echo.
    )
)

:: ─── Find old install ───────────────────────────────────────────────────

set "OLD_DIR="

echo Enter the path to your old ZenithMind-OS-Cowork folder:
echo (You can drag the folder onto this window)
echo.
set /p OLD_DIR="> "

:: Strip quotes
set "OLD_DIR=!OLD_DIR:"=!"

if not exist "!OLD_DIR!" (
    echo Error: Folder not found: !OLD_DIR!
    goto :eof
)

if not exist "!OLD_DIR!\lesson-1\CLAUDE.md" (
    echo Error: That doesn't look like a ZenithMind OS folder.
    goto :eof
)

set "OLD_VERSION=pre-1.0"
if exist "!OLD_DIR!\VERSION" (
    set /p OLD_VERSION=<"!OLD_DIR!\VERSION"
)

echo.
echo Migrating from: !OLD_DIR! (v!OLD_VERSION!)
echo.

:: ─── Migrate user data ──────────────────────────────────────────────────

set "MIGRATED=0"

if exist "!OLD_DIR!\session-progress.md" (
    copy /y "!OLD_DIR!\session-progress.md" "%NEW_DIR%\session-progress.md" >nul
    echo   + session-progress.md
    set /a MIGRATED+=1
)

for %%L in (1 2 3 4) do (
    if exist "!OLD_DIR!\lesson-%%L\outputs\" (
        set "FOUND=0"
        for %%F in ("!OLD_DIR!\lesson-%%L\outputs\*") do set "FOUND=1"
        if !FOUND!==1 (
            if not exist "%NEW_DIR%\lesson-%%L\outputs" mkdir "%NEW_DIR%\lesson-%%L\outputs"
            xcopy "!OLD_DIR!\lesson-%%L\outputs\*" "%NEW_DIR%\lesson-%%L\outputs\" /E /I /Y /Q >nul 2>nul
            echo   + lesson-%%L/outputs/
            set /a MIGRATED+=1
        )
    )
)

if !MIGRATED!==0 (
    echo   No user data found to migrate.
)

echo.
echo ═══════════════════════════════════════════════════════
echo   Upgrade complete! !MIGRATED! file(s) migrated.
echo   Old folder preserved: !OLD_DIR!
echo.
echo   Next: Open Cowork, select this folder, and say
echo   'Let's continue'
echo ═══════════════════════════════════════════════════════
echo.
pause

endlocal
