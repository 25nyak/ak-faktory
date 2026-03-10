@echo off
set LD_PATH="C:\LDPlayer\LDPlayer9"
cd /d %LD_PATH%
echo [ATLAS KLICK] Waking up the factory units...

:: Launching first 5 units
for /l %%i in (0,1,4) do (
    ldconsole.exe launch --index %%i
)
timeout /t 45

:: Open Telegram on all units
for /l %%i in (0,1,4) do (
    ldconsole.exe runapp --index %%i --packagename org.telegram.messenger
)
echo [READY] Your units are online. Fire the Python script.
pause
