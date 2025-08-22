# System Architecture

## Overview

The Sigma to RML Transpiler is built using a modern, scalable architecture that separates concerns between the frontend user interface, backend API services, and the core transpiler engine. This architecture ensures maintainability, testability, and extensibility.

## High-Level Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    Python API    ┌─────────────────┐
│   Frontend      │ ◄──────────────► │   Backend API   │ ◄──────────────► │ Transpiler      │
│   (Next.js)     │                 │   (FastAPI)     │                 │ Engine          │
└─────────────────┘                 └─────────────────┘                 └─────────────────┘
         │                                   │                                   │
         │                                   │                                   │
         ▼                                   ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐                 ┌─────────────────┐
│   User Browser  │                 │   File Storage  │                 │   AST Parser    │
│                 │                 │   (Local FS)    │                 │   & Generator   │
└─────────────────┘                 └─────────────────┘                 └─────────────────┘
```

## Frontend Architecture

### Technology Stack
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4
- **State Management**: React hooks and local state
- **HTTP Client**: Axios for API communication

### Component Structure
```
frontend/
├── app/                          # Next.js app router pages
│   ├── page.tsx                 # Home page
│   ├── sigma-to-rml/            # Main translation interface
│   ├── transpile/               # Simple transpiler
│   └── files/                   # File management
├── components/                   # Reusable UI components
│   ├── ui/                      # Base UI components
│   ├── FileViewer.tsx           # File content display
│   └── Navigation.tsx           # Site navigation
└── lib/                         # Utility libraries
    ├── api.ts                   # API client functions
    └── utils.ts                 # Helper functions
```

### Key Features
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Updates**: Live preview of translation results
- **File Management**: Upload, view, and manage Sigma rule files
- **Error Handling**: User-friendly error messages and validation

## Backend API Architecture

### Technology Stack
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.8+
- **Server**: Uvicorn ASGI server
- **Validation**: Pydantic models
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### API Structure
```
backend/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/                     # API route modules
│   │   ├── transpile.py         # Text-based transpilation
│   │   ├── translate.py         # File-based translation
│   │   ├── files.py             # File management
│   │   └── upload.py            # File upload handling
│   ├── core/                    # Core business logic
│   │   ├── transpiler_refactored.py  # Main transpiler
│   │   ├── ast/                 # Abstract Syntax Tree components
│   │   └── parser.py            # Parsing utilities
│   └── storage/                 # Data persistence
│       └── db.py                # File metadata storage
```

### API Design Principles
- **RESTful Design**: Standard HTTP methods and status codes
- **Input Validation**: Comprehensive YAML and data validation
- **Error Handling**: Detailed error messages with HTTP status codes
- **File Management**: Secure file upload and storage
- **CORS Support**: Cross-origin resource sharing configuration

## Transpiler Engine Architecture

### Core Components

#### 1. Condition Simplifier
- **Purpose**: Applies De Morgan's laws and simplifies complex conditions
- **Features**: Parentheses parsing, logical operator optimization
- **Output**: Simplified condition strings for easier processing

#### 2. Quantifier Expander
- **Purpose**: Expands Sigma quantifier patterns to explicit conditions
- **Supported Patterns**: `all of selection*`, `any of selection*`, `1 of selection*`
- **Output**: Expanded condition strings with explicit selections

#### 3. Field Value Extractor
- **Purpose**: Extracts and formats field values from Sigma rules
- **Features**: Numerical modifier support (`|gte`, `|lte`, `|gt`, `|lt`)
- **Output**: Formatted field values for RML generation

#### 4. RML Line Generator
- **Purpose**: Generates individual RML code sections
- **Components**: Logsource filters, selection definitions, monitor expressions
- **Output**: Structured RML code blocks

### Temporal Processing

#### Temporal Condition Detection
- **Operators**: `| near`, `| before`, `| after`, `| within`, `| count()`
- **Timeframes**: Support for seconds (s), minutes (m), hours (h)
- **Default**: 10 seconds for `| near` operations

#### Temporal RML Generation
- **State Machines**: Monitor state tracking with timestamps
- **Event Types**: Timed event definitions with timestamp parameters
- **Patterns**: Near operations, count operations, general timeframes

### Data Flow

```
Sigma Rule Input
       │
       ▼
┌─────────────────┐
│   YAML Parser   │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Condition Parse │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│   Simplifier    │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│   Expander      │
└─────────────────┘
       │
       ▼
┌─────────────────┐
│ Temporal Check  │
└─────────────────┘
       │
       ▼
┌─────────────────┐    ┌─────────────────┐
│  Basic RML      │    │ Temporal RML    │
│  Generator      │    │ Generator       │
└─────────────────┘    └─────────────────┘
       │                       │
       └───────────────────────┘
                   │
                   ▼
            RML Output
```

## Storage Architecture

### File Storage
- **Upload Directory**: `backend/uploaded_files/`
- **Translation Output**: `backend/translated_files/`
- **Metadata**: JSON-based file registry with file paths and status

### Data Persistence
- **File Registry**: JSON file tracking uploaded and translated files
- **Metadata Storage**: File information, translation status, and RML paths
- **File Operations**: Secure file handling with path normalization

## Security Considerations

### Input Validation
- **YAML Validation**: Strict YAML parsing with error handling
- **File Type Restrictions**: Limited to `.yml` and `.yaml` files
- **Path Security**: Path traversal prevention and normalization

### API Security
- **CORS Configuration**: Restricted to development origins
- **Input Sanitization**: Comprehensive input validation and sanitization
- **Error Handling**: Secure error messages without information disclosure

## Scalability Features

### Modular Design
- **Component Separation**: Clear separation of concerns
- **Interface Contracts**: Well-defined interfaces between components
- **Dependency Injection**: Loose coupling for easy testing and extension

### Performance Optimizations
- **Lazy Loading**: Components loaded on demand
- **Efficient Parsing**: Optimized condition parsing algorithms
- **Memory Management**: Proper resource cleanup and management

### Extensibility
- **Plugin Architecture**: Easy addition of new Sigma patterns
- **Custom Modifiers**: Extensible field modifier system
- **Template System**: Configurable RML output templates

## Deployment Architecture

### Development Environment
- **Local Development**: Hot-reload servers for both frontend and backend
- **Environment Variables**: Configuration through environment files
- **Debug Mode**: Comprehensive logging and error reporting

### Production Considerations
- **Static Build**: Next.js static export for frontend
- **API Scaling**: FastAPI with multiple worker processes
- **File Storage**: Scalable file storage solutions
- **Monitoring**: Health check endpoints and logging
