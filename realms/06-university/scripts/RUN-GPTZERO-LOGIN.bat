@echo off
chcp 65001 >nul
cd /d "C:\Users\User\Desktop\PERFORM\realms\06-university\scripts"
echo === GPTZERO LOGIN + SCAN ===
echo 1. A window opens - LOG IN to GPTZero inside it (one time, session saves)
echo 2. After login the script pastes the drill text and scans automatically
echo 3. Score + screenshot get logged. Just wait until it says DONE.
python battery_gptzero.py "C:\Users\User\Desktop\PERFORM\realms\06-university\courses\Политология\DRILL-referat-politicheski-rezhimi\02-versions\p3-final.txt" --words 350
pause
