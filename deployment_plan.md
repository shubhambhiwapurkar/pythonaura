# Deployment Plan

This document outlines the steps required to deploy the integrated astrology application.

## Frontend

The frontend is a Next.js application. It can be deployed to any platform that supports Node.js, such as Vercel, Netlify, or a custom server.

### Build

To build the frontend, run the following commands:

```bash
cd frontend
npm install
npm run build
```

### Environment Variables

The frontend requires the following environment variable to be set:

*   `NEXT_PUBLIC_API_BASE_URL`: The URL of the backend API.

### Running

To run the frontend in production, use the following command:

```bash
npm start
```

## Backend

The backend is a FastAPI application. It can be deployed to any platform that supports Python, such as Heroku, AWS, or a custom server.

### Build

The backend is a Python application and does not require a build step.

### Environment Variables

The backend requires the following environment variables to be set:

*   `MONGO_URI`: The connection string for the MongoDB database.
*   `JWT_SECRET`: A secret key for signing JWTs.
*   `GOOGLE_CLIENT_SECRET`: The client secret for the Google Maps API.
*   `GEMINI_API_KEY`: The API key for the Google AI API.
*   `ASTROLOGY_SERVICE_URL`: The URL of the astrology service.
*   `CORS_ORIGIN`: The URL of the frontend application.

### Running

To run the backend in production, use a production-ready ASGI server, such as Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000