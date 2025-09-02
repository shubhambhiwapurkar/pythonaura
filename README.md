# Python Backend Migration Project

This project contains the Python backend services for the astrology application, migrated from the original Node.js implementation.

## Project Structure

The project consists of three main components:

1. **Main Backend (FastAPI)** - Located in `/app`
   - Main API gateway
   - Authentication & user management
   - Database interactions
   - Service orchestration

2. **Astrology Service** - Located in `/astrology-service`
   - Birth chart calculations
   - Planetary positions
   - Astrological computations

3. **Daily Content Generator** - Located in `/daily-content-generator`
   - Azure Function
   - Generates personalized daily content
   - Integrates with Google's Generative AI

## Prerequisites

- Python 3.9+
- Azure CLI (for deployment)
- Docker (for containerization)
- MongoDB/Azure Cosmos DB (with MongoDB API)

## Setup Instructions

1. Clone the repository
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies for each component:
   ```bash
   # Main Backend
   cd app
   pip install -r requirements.txt

   # Astrology Service
   cd ../astrology-service
   pip install -r requirements.txt

   # Daily Content Generator
   cd ../daily-content-generator
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env` in the `app` directory
   - Update the values with your actual configuration

5. Start the services locally:
   - Use VS Code tasks (View -> Command Palette -> "Tasks: Run Task")
   - Or manually:
     ```bash
     # Main Backend
     cd app
     uvicorn main:app --reload --host 0.0.0.0 --port 8000

     # Astrology Service
     cd astrology-service
     uvicorn main:app --reload --host 0.0.0.0 --port 8001
     ```

## Deployment to Azure

### Container Apps

1. Build and push Docker images:
   ```bash
   # Main Backend
   cd app
   docker build -t your-registry.azurecr.io/main-backend:latest .
   docker push your-registry.azurecr.io/main-backend:latest

   # Astrology Service
   cd ../astrology-service
   docker build -t your-registry.azurecr.io/astrology-service:latest .
   docker push your-registry.azurecr.io/astrology-service:latest
   ```

2. Deploy to Azure Container Apps using Azure CLI or Azure Portal

### Azure Function

1. Deploy the Daily Content Generator:
   ```bash
   cd daily-content-generator
   func azure functionapp publish your-function-app-name
   ```

## API Documentation

After starting the services, access the API documentation:
- Main Backend: http://localhost:8000/docs
- Astrology Service: http://localhost:8001/docs

## Testing

Run tests for each component:
```bash
# Main Backend
cd app
pytest

# Astrology Service
cd ../astrology-service
pytest

# Daily Content Generator
cd ../daily-content-generator
pytest
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[Your License Here]
