# API Reference

## Overview

The Sigma to RML Transpiler API provides RESTful endpoints for converting Sigma security rules to Runtime Monitoring Language (RML) specifications. The API is built using FastAPI and provides comprehensive input validation, error handling, and automatic documentation.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Common Response Format

All API responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "message": "Human-readable description",
  "data": {}, // Response-specific data
  "timestamp": "ISO 8601 timestamp"
}
```

## Error Handling

### HTTP Status Codes

- **200 OK**: Request successful
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

### Error Response Format

```json
{
  "detail": "Detailed error message",
  "status_code": 400,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Endpoints

### 1. Root Information

#### GET /

Returns basic API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to Sigma2RML backend",
  "version": "1.0.0",
  "description": "Sigma to RML Transpiler API",
  "endpoints": {
    "upload": "/upload",
    "transpile": "/transpile",
    "files": "/files",
    "translate": "/translate",
    "docs": "/docs"
  }
}
```

### 2. Health Check

#### GET /health

Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 3. Transpilation

#### POST /transpile

Transpiles Sigma rule text to RML.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `sigma_text` field

**Parameters:**
- `sigma_text` (string, required): Sigma rule in YAML format

**Example Request:**
```bash
curl -X POST "http://localhost:8000/transpile" \
  -F "sigma_text=title: Example Rule
detection:
  selection:
    EventID: 4624
  condition: selection"
```

**Response:**
```json
{
  "status": "success",
  "rml": "// log source filter\nlogsource matches {product: 'windows', service: 'security'};\n\n// event types\nsafe_selection not matches {eventid: 4624};\n\n// property section\nMain = logsource >> Monitor;\nMonitor = safe_selection*;",
  "input_length": 89,
  "output_length": 234,
  "message": "Sigma rule successfully transpiled to RML"
}
```

#### POST /transpile/validate

Validates Sigma rule format without transpiling.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `sigma_text` field

**Response:**
```json
{
  "status": "success",
  "valid": true,
  "message": "Sigma rule format is valid",
  "structure": {
    "has_title": true,
    "has_logsource": false,
    "has_detection": true,
    "detection_keys": ["selection", "condition"]
  }
}
```

### 4. File Translation

#### POST /translate/{filename}

Translates a Sigma rule file to RML and saves the result.

**Parameters:**
- `filename` (string, path parameter): Name of the file to translate

**Response:**
```json
{
  "status": "success",
  "filename": "example.yml",
  "rml_text": "// Generated RML content...",
  "rml_path": "translated_files/example.rml",
  "actual_rml_path": "D:\\path\\to\\translated_files\\example.rml",
  "message": "Successfully translated example.yml to RML"
}
```

#### GET /translate/{filename}/status

Gets the translation status of a file.

**Response:**
```json
{
  "filename": "example.yml",
  "translated": true,
  "rml_path": "translated_files/example.rml",
  "title": "Example Rule"
}
```

### 5. File Management

#### GET /files

Lists all uploaded and translated files.

**Response:**
```json
[
  {
    "filename": "example.yml",
    "title": "Example Rule",
    "uploaded_at": "2024-01-01T00:00:00Z",
    "translated": true,
    "rml_path": "translated_files/example.rml"
  }
]
```

#### GET /files/{filename}

Gets information about a specific file.

**Response:**
```json
{
  "filename": "example.yml",
  "title": "Example Rule",
  "content": "title: Example Rule\ndetection:\n  selection:\n    EventID: 4624\n  condition: selection",
  "translated": true,
  "rml_path": "translated_files/example.rml"
}
```

#### GET /files/rml/{filename}

Gets the RML content for a translated file.

**Response:**
```json
{
  "filename": "example.yml",
  "rml": "// Generated RML content...",
  "translated_at": "2024-01-01T00:00:00Z"
}
```

#### DELETE /files/{filename}

Deletes a file and its associated RML output.

**Response:**
```json
{
  "status": "success",
  "message": "File example.yml deleted successfully"
}
```

### 6. File Upload

#### POST /upload

Uploads a Sigma rule file.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `file` field

**Parameters:**
- `file` (file, required): Sigma rule file (.yml or .yaml)

**Response:**
```json
{
  "status": "success",
  "filename": "example.yml",
  "title": "Example Rule",
  "message": "File uploaded successfully",
  "file_path": "uploaded_files/example.yml"
}
```

#### GET /upload/allowed-types

Gets the list of allowed file types.

**Response:**
```json
{
  "allowed_types": [".yml", ".yaml"],
  "max_size": "10MB"
}
```

## Data Models

### Sigma Rule Structure

```yaml
title: Rule Title
id: unique-rule-id
description: Rule description
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4624
    Image: "*.exe"
  condition: selection
  timeframe: 5m  # Optional
level: high
```

### RML Output Structure

```rml
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
safe_selection not matches {eventid: 4624, image: '*.exe'};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;
```

### Temporal RML Structure

```rml
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
timed_selection(ts) matches {timestamp: ts, eventid: 4624};
timed_other_events(ts) matches {timestamp: ts};

// property section
Main = logsource >> Monitor<0, 0>!;
Monitor<start_ts, s1> = {
    let ts; timed_selection(ts) (
        if (start_ts == 0 || ts - start_ts > 300000)
            Monitor<ts, 1>
        else (
            empty
        )
    )
};
```

## Error Codes and Messages

### Common Error Messages

| Error Code | Message | Description |
|------------|---------|-------------|
| 400 | "Sigma rule text is required" | Missing required input |
| 400 | "Invalid YAML format" | Malformed YAML syntax |
| 400 | "Missing required fields" | Incomplete Sigma rule structure |
| 404 | "File not found" | Requested file doesn't exist |
| 500 | "Transpilation failed" | Internal transpiler error |

### Validation Errors

```json
{
  "detail": "Missing required fields: detection",
  "status_code": 400,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting

Currently, the API does not implement rate limiting. All endpoints are accessible without restrictions.

## CORS Configuration

The API is configured with CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`

## Testing

### Test Endpoints

The API includes several test endpoints for development and validation:

- **Health Check**: `/health`
- **API Info**: `/`
- **OpenAPI Schema**: `/openapi.json`

### Example Test Requests

```bash
# Test basic transpilation
curl -X POST "http://localhost:8000/transpile" \
  -F "sigma_text=detection: {selection: {EventID: 4624}, condition: selection}"

# Test file upload
curl -X POST "http://localhost:8000/upload" \
  -F "file=@example.yml"

# Test file translation
curl -X POST "http://localhost:8000/translate/example.yml"
```

## Versioning

The current API version is 1.0.0. Future versions will be available under versioned endpoints (e.g., `/v2/`).

## Support

For API support and questions:
- Check the interactive documentation at `/docs`
- Review the error messages and status codes
- Examine the test examples in the codebase
- Open an issue on the project repository
