@echo off
echo Setting up Python development environment...

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies for main backend
echo Installing main backend dependencies...
cd app
pip install -r requirements.txt
cd ..

:: Install dependencies for astrology service
echo Installing astrology service dependencies...
cd astrology-service
pip install -r requirements.txt
cd ..

:: Install dependencies for daily content generator
echo Installing daily content generator dependencies...
cd daily-content-generator
pip install -r requirements.txt
cd ..

:: Create .env file from template for main backend
echo Creating .env file...
copy app\.env.example app\.env

echo Setup complete! Please update the .env file with your configuration values.
echo To activate the virtual environment in the future, run: venv\Scripts\activate.bat
