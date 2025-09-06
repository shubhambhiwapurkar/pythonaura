# Cosmotalks API Documentation

## Base URL
```
https://cosmicapp-app.kindflower-34fe9cb7.eastus.azurecontainerapps.io
```

## Table of Contents
- [Authentication](#authentication)
- [User Management](#user-management)
- [Birth Charts](#birth-charts)
- [Chat](#chat)
- [Daily Content](#daily-content)

## Authentication

### Login
`POST /api/v1/auth/login`

Authenticate a user and receive access and refresh tokens.

**Request Body** (application/x-www-form-urlencoded):
```
username: string (email address)
password: string
```

**Response** (200 OK):
```json
{
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer"
}
```

**Error Responses:**
- 401 Unauthorized: Invalid credentials
- 422 Unprocessable Entity: Invalid input format

### Register
`POST /api/v1/auth/signup`

Create a new user account.

**Request Body** (application/json):
```json
{
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "birth_date": "string",
    "birth_time": "string",
    "birth_place": "string"
}
```

**Response** (201 Created):
```json
{
    "id": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "birth_details": {}
}
```

### Refresh Token
`POST /api/v1/auth/refresh-token`

Get a new access token using a refresh token.

**Headers:**
```
Authorization: Bearer {refresh_token}
```

**Response** (200 OK):
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

## User Management

### Get Current User
`GET /api/v1/user/me`

Get details of the currently authenticated user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
    "id": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "birth_details": {
        "date": "string",
        "time": "string",
        "place": "string"
    },
    "created_at": "datetime"
}
```

### Delete Account
`DELETE /api/v1/account`

Delete the current user's account and all associated data.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
    "message": "Account successfully deleted",
    "status": "success"
}
```

## Birth Charts

### Create Birth Chart
`POST /api/v1/chart`

Create a new birth chart for the current user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body** (application/json):
```json
{
    "birth_date": "string (YYYY-MM-DD)",
    "birth_time": "string (HH:mm)",
    "latitude": "number",
    "longitude": "number",
    "timezone": "string"
}
```

**Response** (201 Created):
```json
{
    "id": "string",
    "user": "string",
    "birth_data": {
        "date": "datetime",
        "time": "string",
        "city": "string",
        "state": "string",
        "country": "string",
        "latitude": "number",
        "longitude": "number",
        "timezone": "string"
    },
    "chart_data": {
        "ascendant": "string",
        "sun_sign": "string",
        "moon_sign": "string",
        "planets": {},
        "houses": {},
        "aspects": {}
    },
    "created_at": "datetime"
}
```

### Get Birth Chart
`GET /api/v1/chart/{chart_id}`

Retrieve a specific birth chart.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
    "id": "string",
    "user": "string",
    "birth_data": {
        "date": "datetime",
        "time": "string",
        "city": "string",
        "state": "string",
        "country": "string",
        "latitude": "number",
        "longitude": "number",
        "timezone": "string"
    },
    "chart_data": {
        "ascendant": "string",
        "sun_sign": "string",
        "moon_sign": "string",
        "planets": {},
        "houses": {},
        "aspects": {}
    },
    "created_at": "datetime"
}
```

### Get User Charts
`GET /api/v1/chart/user`

Retrieve all birth charts for the current user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
[
    {
        "id": "string",
        "user": "string",
        "birth_data": {...},
        "chart_data": {...},
        "created_at": "datetime"
    }
]
```

### Get Chart Transits
`GET /api/v1/chart/{chart_id}/transits`

Get daily transits for a specific birth chart.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
    "date": "string",
    "transits": [
        {
            "planet": "string",
            "aspect": "string",
            "target": "string",
            "description": "string"
        }
    ]
}
```

## Chat

### Create Chat Session
`POST /api/v1/chat/sessions`

Create a new chat session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body** (application/json):
```json
{
    "title": "string (optional)",
    "context": {} (optional)
}
```

**Response** (201 Created):
```json
{
    "id": "string",
    "user": "string",
    "title": "string",
    "messages": [],
    "context": {},
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Send Message
`POST /api/v1/chat/sessions/{session_id}/messages`

Send a message in a chat session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body** (application/json):
```json
{
    "content": "string",
    "message_type": "string (optional, default: text)"
}
```

**Response** (200 OK):
```json
{
    "id": "string",
    "role": "assistant",
    "content": "string",
    "message_type": "string",
    "timestamp": "datetime",
    "metadata": {}
}
```

### Get Messages
`GET /api/v1/chat/sessions/{session_id}/messages`

Get all messages from a chat session.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
    "messages": [
        {
            "id": "string",
            "role": "string",
            "content": "string",
            "message_type": "string",
            "timestamp": "datetime",
            "metadata": {}
        }
    ]
}
```

## Daily Content

### Get Daily Content
`GET /api/v1/daily/content`

Get personalized daily content for the current user.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
```
date: string (optional, YYYY-MM-DD format)
```

**Response** (200 OK):
```json
{
    "date": "string",
    "dailyAffirmation": "string",
    "dailyChartInsight": "string",
    "keyTransits": [
        {
            "transit": "string",
            "description": "string"
        }
    ],
    "exploreTopic": "string"
}
```

## Error Responses

All endpoints may return the following error responses:

### 401 Unauthorized
```json
{
    "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
    "detail": [
        {
            "loc": ["string"],
            "msg": "string",
            "type": "string"
        }
    ]
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error message"
}
```

## Authentication Notes

1. All protected endpoints require a valid JWT token in the Authorization header
2. Access tokens expire after 30 minutes
3. Refresh tokens are valid for 7 days
4. Use the refresh token endpoint to get a new access token
5. Invalid tokens will return a 401 Unauthorized response

## Rate Limiting

- Standard rate limit: 100 requests per minute per IP
- Chat endpoints: 30 requests per minute per user
- Daily content: 24 requests per day per user

## Data Types

### DateTime Format
All datetime fields follow ISO 8601 format: `YYYY-MM-DDTHH:mm:ss.sssZ`

### ObjectId
MongoDB ObjectIds are represented as 24-character hexadecimal strings

### Coordinates
- Latitude: Float between -90 and 90
- Longitude: Float between -180 and 180

## Best Practices

1. Always validate tokens before making requests
2. Handle token expiration gracefully by implementing refresh token logic
3. Implement proper error handling for all possible response codes
4. Cache daily content responses when appropriate
5. Use appropriate content-type headers for all requests
