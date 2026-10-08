@echo off
chcp 65001 > nul
echo ========================================================
echo   CHAY AUTOMATION TEST VA TAO BAO CAO ALLURE REPORT
echo ========================================================
echo Dang chay kiem thu voi Pytest va Allure...
python run_allure.py --no-open
if %errorlevel% neq 0 (
    echo Co loi xay ra hoac mot so test case khong dat.
)
echo.
echo Dang mo bao cao Allure tren trinh duyet...
allure open allure-report
pause
