@echo off
echo Baslatiliyor...
git init
git add .
git commit -m "Initial commit: Open source Stealth Interview Copilot release"
git remote add origin https://github.com/picaquality/Stealth-Interview-CoPliot.git
git branch -M main
git push -u origin main
echo Bitti! Kapatmak icin bir tusa bas...
pause
