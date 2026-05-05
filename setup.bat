@echo off
:: ZenithMind OS — Setup & Upgrade
:: Handles fresh installs AND upgrades from previous versions.
:: Run once per version. After this, say 'zenithmind' in any Claude session to start.

setlocal enabledelayedexpansion

set "ZMOS_DIR=%~dp0"
set "ZMOS_DIR=%ZMOS_DIR:~0,-1%"
set "CONFIG_FILE=%USERPROFILE%\.zenithmind"
set "BIN_DIR=%USERPROFILE%\.local\bin"
set "CLAUDE_MD=%USERPROFILE%\.claude\CLAUDE.md"

:: Read new version
set "NEW_VERSION=unknown"
if exist "%ZMOS_DIR%\VERSION" (
    set /p NEW_VERSION=<"%ZMOS_DIR%\VERSION"
)

:: ─── Detect install state ───────────────────────────────────────────────

set "MODE=fresh"
set "OLD_DIR="
set "OLD_VERSION="

if exist "%CONFIG_FILE%" (
    set /p OLD_DIR=<"%CONFIG_FILE%"
)

if defined OLD_DIR (
    if "!OLD_DIR!"=="%ZMOS_DIR%" (
        set "MODE=refresh"
    ) else if exist "!OLD_DIR!" (
        set "OLD_VERSION=pre-1.0"
        if exist "!OLD_DIR!\VERSION" (
            set /p OLD_VERSION=<"!OLD_DIR!\VERSION"
        )
        set "MODE=upgrade"
    )
)

:: ─── Execute based on mode ──────────────────────────────────────────────

if "%MODE%"=="refresh" (
    echo ZenithMind OS v%NEW_VERSION% — already set up in this folder.
    echo Refreshing launcher...
    goto :register
)

if "%MODE%"=="upgrade" (
    echo ═══════════════════════════════════════════════════════
    echo   ZenithMind OS — Upgrading
    echo   From: v!OLD_VERSION! ^(!OLD_DIR!^)
    echo   To:   v%NEW_VERSION% ^(%ZMOS_DIR%^)
    echo ═══════════════════════════════════════════════════════
    echo.

    :: Step 1: Backup old install
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set "DATESTAMP=%%c%%a%%b"
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set "TIMESTAMP=%%a%%b"
    set "BACKUP_DIR=%USERPROFILE%\.zenithmind-backup-%DATESTAMP%-%TIMESTAMP%"

    echo Creating backup of old install...
    xcopy "!OLD_DIR!" "!BACKUP_DIR!\" /E /I /Q >nul
    echo   Backup saved: !BACKUP_DIR!
    echo.

    :: Step 2: Migrate user data
    echo Migrating your data...
    set "MIGRATED=0"

    if exist "!OLD_DIR!\session-progress.md" (
        copy /y "!OLD_DIR!\session-progress.md" "%ZMOS_DIR%\session-progress.md" >nul
        echo   + session-progress.md
        set /a MIGRATED+=1
    )

    for %%L in (1 2 3 4) do (
        if exist "!OLD_DIR!\lesson-%%L\outputs\" (
            set "FOUND=0"
            for %%F in ("!OLD_DIR!\lesson-%%L\outputs\*") do set "FOUND=1"
            if !FOUND!==1 (
                if not exist "%ZMOS_DIR%\lesson-%%L\outputs" mkdir "%ZMOS_DIR%\lesson-%%L\outputs"
                xcopy "!OLD_DIR!\lesson-%%L\outputs\*" "%ZMOS_DIR%\lesson-%%L\outputs\" /E /I /Y /Q >nul 2>nul
                echo   + lesson-%%L/outputs/
                set /a MIGRATED+=1
            )
        )
    )

    if !MIGRATED!==0 (
        echo   No user data found to migrate.
    )

    echo.
    echo Migration complete.
    echo   Old folder preserved: !OLD_DIR!
    echo   Backup: !BACKUP_DIR!
    echo.
    goto :register
)

:: Fresh install
echo Setting up ZenithMind OS v%NEW_VERSION%...
echo.

:register
:: ─── Register launcher + CLI command (all modes) ────────────────────────

:: Save install path
echo %ZMOS_DIR%> "%CONFIG_FILE%"

:: Create bin directory
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

:: Create launcher script
(
echo @echo off
echo set /p ZMOS_DIR=^<"%%USERPROFILE%%\.zenithmind"
echo if not exist "%%ZMOS_DIR%%" ^(
echo     echo ZenithMind OS folder not found.
echo     echo Open Claude Code from your ZenithMind-OS folder to re-run setup.
echo     exit /b 1
echo ^)
echo cd /d "%%ZMOS_DIR%%" ^&^& claude %%*
) > "%BIN_DIR%\zenithmind.bat"

:: Add to user PATH if not already there
echo %PATH% | find /i ".local\bin" >nul
if errorlevel 1 (
    powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';%BIN_DIR%', 'User')" >nul 2>&1
)

:: Register ZenithMind as a global trigger in Claude Code
if not exist "%USERPROFILE%\.claude" mkdir "%USERPROFILE%\.claude"
findstr /c:"## ZenithMind OS" "%CLAUDE_MD%" >nul 2>&1
if errorlevel 1 (
    echo. >> "%CLAUDE_MD%"
    echo ## ZenithMind OS >> "%CLAUDE_MD%"
    echo. >> "%CLAUDE_MD%"
    echo **Trigger:** "zenithmind", "let's do zenithmind", "start zenithmind", "continue zenithmind", "let's continue zenithmind", "pick up zenithmind", "zenith mind" >> "%CLAUDE_MD%"
    echo. >> "%CLAUDE_MD%"
    echo When ANY of these triggers appear in the user's message: >> "%CLAUDE_MD%"
    echo. >> "%CLAUDE_MD%"
    echo 1. Read `~/.zenithmind` to get the install path >> "%CLAUDE_MD%"
    echo 2. `cd` into that folder >> "%CLAUDE_MD%"
    echo 3. Read the `CLAUDE.md` at that path >> "%CLAUDE_MD%"
    echo 4. Follow the **Session Start — Loading Protocol** in that CLAUDE.md >> "%CLAUDE_MD%"
    echo 5. If the user said "continue" or "pick up" — check `session-progress.md` and resume where they left off >> "%CLAUDE_MD%"
    echo 6. If the user said "start" or "let's do" — check progress and either start fresh or resume >> "%CLAUDE_MD%"
    echo. >> "%CLAUDE_MD%"
    echo **This works from ANY Claude Code session, ANY folder, ANY terminal.** The trigger phrase is the only thing needed. >> "%CLAUDE_MD%"
    echo Registered ZenithMind as a global trigger in Claude Code.
) else (
    echo ZenithMind trigger already registered in Claude Code.
)

echo.
echo Setup complete!
echo   - Say 'zenithmind' in any Claude session to start or continue
echo   - Or type 'zenithmind' in any terminal

endlocal
