@echo off
chcp 65001 > nul
echo ========================================================
echo   MO BAO CAO ALLURE REPORT TREN TRINH DUYET
echo ========================================================
if exist "allure-report" (
    echo Dang mo bao cao tai allure-report...
    allure open allure-report
) else if exist "allure-results" (
    echo Chua bien dich sang allure-report, dang mo truc tiep tu allure-results...
    allure serve allure-results
) else (
    echo Khong tim thay thu muc allure-report hoac allure-results.
    echo Vui long chay kiem thu truoc bang lenh: python run_allure.py hoac chay file run_allure.bat
    pause
)
