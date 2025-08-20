# Sigma to RML Transpiler

A robust and production-ready transpiler that converts Sigma detection rules to RML (Runtime Monitoring Language) format. This tool enables security analysts and researchers to translate Sigma rules into executable monitoring specifications.

## 🚀 Features

### Core Capabilities
- **Complete Sigma Rule Support**: Handles all basic Sigma detection patterns
- **Advanced Quantifiers**: Full support for "all of them", "all of selection*", "1 of selection*", "N of selection*"
- **Temporal Operations**: Handle `| near`, `| count() > N` with smart timeframe conversion
- **Numerical Modifiers**: Support for `lt`, `lte`, `gt`, `gte` with intelligent logic handling
- **Complex Logical Structures**: Proper handling of nested conditions, parentheses, and negation

### Supported Sigma Patterns
- **Basic Selections**: Simple field matching with exact values
- **List Values**: OR-based field matching with multiple values
- **Comparison Operators**: Numerical comparisons with proper RML translation
- **Logical Operators**: AND, OR, NOT with correct RML syntax
- **Quantified Patterns**: Complex selection patterns with proper RML generation
- **Temporal Patterns**: Time-based event correlation and counting

### RML Output Features
- **Safe Value Generation**: Automatic generation of safe values for monitoring
- **Proper Negation**: Correct handling of NOT conditions without operator inversion
- **Monitor Generation**: Automatic RML Monitor pattern generation
- **Logsource Filtering**: Proper logsource-based event filtering

## 🏗️ Architecture

### Backend (Python/FastAPI)
```
backend/
├── app/
│   ├── core/
│   │   ├── ast/           # Abstract Syntax Tree nodes
│   │   ├── parser.py      # Sigma rule parser
│   │   └── transpiler.py  # Core transpilation logic
│   ├── api/               # REST API endpoints
│   ├── storage/           # File storage and database
│   └── utils/             # Utility functions
├── tests/                 # Comprehensive test suite
└── requirements.txt       # Python dependencies
```

### Frontend (Next.js/React)
```
frontend/
├── app/                   # Next.js app router
├── components/            # React components
├── lib/                   # API utilities
└── public/                # Static assets
```

## 📋 Prerequisites

- **Python 3.8+** for backend
- **Node.js 18+** for frontend
- **Git** for version control

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sigma2rml
   ```

2. **Set up Python environment**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🎯 Usage

### Web Interface

1. **Navigate to the Sigma to RML page**
2. **Input your Sigma rule** in YAML format
3. **Click "Transpile"** to generate RML
4. **Review the generated RML** code
5. **Copy or download** the RML output

### API Usage

```bash
# Transpile a Sigma rule
curl -X POST "http://localhost:8000/api/transpile" \
  -H "Content-Type: application/json" \
  -d '{
    "sigma_rule": {
      "logsource": {"product": "windows", "service": "security"},
      "detection": {
        "selection": {"EventID": 4738},
        "condition": "selection"
      }
    }
  }'
```

### Example Sigma Rules

#### Basic Selection
```yaml
title: Basic Selection Rule
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4624
  condition: selection
```

#### Numerical Modifier
```yaml
title: Numerical Modifier Rule
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4738
    AttributeValue|gte: 7
  condition: selection
```

#### Complex Condition
```yaml
title: Complex Condition Rule
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4738
  check_value:
    AttributeValue|gte: 7
  condition: selection and check_value
```

## 🔧 Configuration

### Backend Configuration

The backend can be configured through environment variables:

```bash
# CORS settings
ALLOW_ORIGINS=http://localhost:3000

# File storage settings
UPLOAD_DIR=uploaded_files
TRANSLATED_DIR=translated_files
```

### Frontend Configuration

Frontend configuration is handled through Next.js configuration files:

```typescript
// next.config.ts
const nextConfig = {
  // API base URL
  env: {
    API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000'
  }
}
```

## 🧪 Testing

### Running Tests

```bash
cd backend

# Run all tests with the test runner
python run_tests.py

# Run specific test categories
python tests/test_basic_patterns.py
python tests/test_numerical_modifiers.py
python tests/test_complex_conditions.py
```

### Test Coverage

The test suite covers:
- **Basic Patterns**: Simple selections, multiple values, logical operators
- **Numerical Modifiers**: All supported comparison operators
- **Complex Conditions**: Nested logic, negation, quantifiers
- **Temporal Operators**: Time-based patterns and counting
- **Edge Cases**: Boundary conditions and error handling

## 📚 API Reference

### Endpoints

#### POST `/api/transpile`
Transpiles a Sigma rule to RML format.

**Request Body:**
```json
{
  "sigma_rule": {
    // Sigma rule in YAML format
  }
}
```

**Response:**
```json
{
  "rml": "Generated RML code",
  "status": "success"
}
```

#### POST `/api/upload`
Uploads a Sigma rule file for processing.

#### GET `/api/files`
Retrieves list of uploaded and translated files.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure Python virtual environment is activated
   - Check that all dependencies are installed

2. **CORS Errors**
   - Verify backend CORS configuration
   - Check frontend API base URL

3. **File Upload Issues**
   - Ensure upload directories have proper permissions
   - Check file size limits

### Debug Mode

Enable debug logging by setting environment variables:

```bash
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true
```

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests for new functionality**
5. **Submit a pull request**

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript/TypeScript**: Use ESLint and Prettier
- **Tests**: Maintain comprehensive test coverage

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Sigma Project**: For the excellent detection rule specification
- **RML Community**: For the Runtime Monitoring Language specification
- **Contributors**: All those who have contributed to this project

## 📞 Support

For questions, issues, or contributions:

- **Issues**: Use the GitHub issue tracker
- **Discussions**: Join the GitHub discussions
- **Documentation**: Check the inline code documentation

---

**Note**: This transpiler is designed for production use and has been thoroughly tested with comprehensive test suites covering all supported Sigma patterns and edge cases.
