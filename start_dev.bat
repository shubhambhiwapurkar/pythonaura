@echo off
echo Starting development environment...

:: Stop any running containers and remove them
echo Stopping existing Docker containers...
docker-compose down

:: Wait for the container to be removed
timeout /t 5

:: Start MongoDB using Docker Compose
echo Starting MongoDB...
docker-compose up -d

:: Wait for MongoDB to be ready
timeout /t 5

:: Start the main backend
echo Starting main backend...
start cmd /k "venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Start the astrology service
echo Starting astrology service...
start cmd /k "venv\Scripts\activate.bat && cd astrology-service && uvicorn main:app --reload --host 0.0.0.0 --port 8001"

echo Development environment is starting up...
echo Main backend will be available at: http://localhost:8000
echo Astrology service will be available at: http://localhost:8001
echo MongoDB is running on: localhost:27017
