@echo off

echo 🔍 Verifying EmotionEye deployment...

REM Check if containers are running
docker-compose ps | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo ❌ Containers are not running. Please run deploy.bat first.
    pause
    exit /b 1
)

REM Run deployment tests
echo 🧪 Running API tests...
python test_deployment.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Deployment verification completed successfully!
    echo 🌐 Your EmotionEye application is ready at:
    echo    Frontend: http://localhost
    echo    Backend:  http://localhost:5000
    echo.
    echo 📋 Useful commands:
    echo    View logs:     docker-compose logs -f
    echo    Stop service:  docker-compose down
    echo    Restart:       docker-compose restart
) else (
    echo ❌ Deployment verification failed!
    echo 📋 Troubleshooting:
    echo    Check logs:    docker-compose logs
    echo    Restart:       docker-compose restart
    pause
    exit /b 1
)

pause