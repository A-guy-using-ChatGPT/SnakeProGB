@echo off
:prompt
set /p answer="Are you British? (Y/N): "
if /i "%answer%"=="Y" (
    start index.html
) else if /i "%answer%"=="N" (
    start minigame1.py
) else (
    echo Invalid input. Please type Y for Yes or N for No.
    goto prompt
)
