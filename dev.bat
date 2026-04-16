@echo off
echo Starting RoleFit Development Environment...
echo.

echo [1/2] Starting Backend API on port 8000...
start cmd /k "cd backend && venv\Scripts\activate && uvicorn api:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend on port 3000...
start cmd /k "cd frontend && npm run dev"

echo.
echo ✓ Backend: http://localhost:8000
echo ✓ Frontend: http://localhost:3000
echo ✓ API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul
