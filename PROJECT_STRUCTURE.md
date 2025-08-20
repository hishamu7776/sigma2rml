# Project Structure

This document provides an overview of the Sigma to RML Transpiler project structure.

## 📁 Root Directory

```
sigma2rml/
├── README.md              # Main project documentation
├── PROJECT_STRUCTURE.md   # This file - project structure overview
├── .gitignore            # Git ignore patterns
├── backend/              # Python backend application
└── frontend/             # Next.js frontend application
```

## 🐍 Backend Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   ├── api/                     # REST API endpoints
│   │   ├── __init__.py
│   │   ├── files.py            # File upload/download endpoints
│   │   ├── translate.py         # Translation API endpoint
│   │   └── transpile.py         # Transpilation API endpoint
│   ├── core/                    # Core transpilation logic
│   │   ├── __init__.py
│   │   ├── ast/                # Abstract Syntax Tree nodes
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base AST node class
│   │   │   ├── nodes.py        # AST node implementations
│   │   │   └── condition_parser.py  # Condition parsing logic
│   │   ├── parser.py            # Sigma rule parser
│   │   └── transpiler.py        # Main transpilation engine
│   ├── storage/                 # File storage and database
│   │   ├── __init__.py
│   │   ├── db.py               # Database operations
│   │   └── store.py            # File storage operations
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── file_handler.py      # File handling utilities
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_all.py             # Comprehensive test runner
│   ├── test_basic_patterns.py  # Basic pattern tests
│   ├── test_complex_conditions.py  # Complex condition tests
│   ├── test_numerical_modifiers.py # Numerical modifier tests
│   ├── test_quantifiers.py     # Quantifier pattern tests
│   ├── test_temporal_operators.py  # Temporal operator tests
│   ├── test_transpiler.py      # Transpiler core tests
│   └── test_unsupported_modifiers.py # Unsupported modifier tests
├── uploaded_files/              # User uploaded Sigma rules
├── translated_files/            # Generated RML files
├── venv/                       # Python virtual environment
├── requirements.txt             # Python dependencies
└── run_tests.py                # Simple test runner script
```

## ⚛️ Frontend Structure

```
frontend/
├── app/                        # Next.js app router
│   ├── favicon.ico
│   ├── globals.css             # Global styles
│   ├── layout.tsx              # Root layout component
│   ├── page.tsx                # Home page
│   ├── files/                  # File management page
│   │   └── page.tsx
│   ├── sigma-to-rml/          # Main transpilation page
│   │   └── page.tsx
│   ├── transpile/              # Transpilation interface
│   │   └── page.tsx
│   └── upload/                 # File upload page
│       └── page.tsx
├── components/                  # React components
│   ├── FileListTable.tsx       # File listing table
│   ├── FileViewer.tsx          # File content viewer
│   ├── Navbar.tsx              # Navigation bar
│   └── ui/                     # UI components
│       └── button.tsx          # Button component
├── lib/                        # Utility libraries
│   ├── api.ts                  # API client functions
│   └── utils.ts                # Utility functions
├── public/                     # Static assets
│   ├── file.svg
│   ├── globe.svg
│   └── next.svg
├── eslint.config.mjs           # ESLint configuration
├── next.config.ts              # Next.js configuration
├── package.json                # Node.js dependencies
└── package-lock.json           # Locked dependency versions
```

## 🔧 Key Components

### Backend Core Components

1. **AST Nodes** (`backend/app/core/ast/`)
   - `base.py`: Base class for all AST nodes
   - `nodes.py`: Implementation of specific node types (Selection, Match, And, Or, Not, etc.)
   - `condition_parser.py`: Parser for complex Sigma conditions

2. **Transpiler Engine** (`backend/app/core/`)
   - `parser.py`: Parses Sigma YAML rules into AST
   - `transpiler.py`: Converts AST into RML format

3. **API Endpoints** (`backend/app/api/`)
   - `transpile.py`: Main transpilation endpoint
   - `translate.py`: Translation endpoint
   - `files.py`: File management endpoints

### Frontend Components

1. **Main Pages**
   - Home page with project overview
   - Sigma to RML transpilation interface
   - File upload and management
   - Transpilation results viewer

2. **Reusable Components**
   - Navigation bar
   - File listing table
   - File content viewer
   - UI components (buttons, etc.)

## 🧪 Testing Structure

The test suite is organized by functionality:

- **Basic Patterns**: Simple selections, field matching
- **Numerical Modifiers**: Comparison operators (lt, lte, gt, gte)
- **Complex Conditions**: Nested logic, negation, parentheses
- **Quantifiers**: "all of them", "1 of selection*" patterns
- **Temporal Operators**: Time-based patterns and counting
- **Unsupported Modifiers**: Handling of unsupported Sigma features

## 📁 File Storage

- **`uploaded_files/`**: Stores user-uploaded Sigma rule files
- **`translated_files/`**: Stores generated RML output files
- **`file_registry.json`**: Tracks file metadata and relationships

## 🚀 Getting Started

1. **Backend**: Navigate to `backend/` and follow the installation instructions in README.md
2. **Frontend**: Navigate to `frontend/` and run `npm install` followed by `npm run dev`
3. **Testing**: Use `python run_tests.py` in the backend directory to run all tests

## 🔍 Development Workflow

1. **Backend Changes**: Modify files in `backend/app/` and test with `python run_tests.py`
2. **Frontend Changes**: Modify files in `frontend/app/` and `frontend/components/`
3. **Testing**: Add new tests to appropriate test files in `backend/tests/`
4. **Documentation**: Update README.md and PROJECT_STRUCTURE.md as needed
