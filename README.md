# Sigma to RML Transpiler

A modern web application that converts Sigma security rules to Runtime Monitoring Language (RML) specifications. This tool provides an intuitive interface for security analysts and developers to transform Sigma detection rules into executable RML monitoring specifications.

## 🚀 Features

- **Sigma Rule Parsing**: Parse and validate Sigma YAML rules
- **RML Generation**: Generate Runtime Monitoring Language specifications
- **Temporal Support**: Handle time-based correlation patterns (`| near`, `| count()`, timeframes)
- **Advanced Conditions**: Support for complex logical conditions, negation, and quantifiers
- **File Management**: Upload, store, and manage Sigma rule files
- **Real-time Translation**: Instant conversion with live preview
- **Modern UI**: Responsive web interface built with Next.js and Tailwind CSS

## 🏗️ Architecture

The application follows a modern microservices architecture:

- **Frontend**: Next.js 15 with React 19, TypeScript, and Tailwind CSS
- **Backend**: FastAPI with Python 3.8+
- **Transpiler Engine**: Modular Python-based Sigma-to-RML converter
- **Storage**: File-based storage with JSON metadata tracking

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.8+
- **Dependencies**: PyYAML, Pydantic, Uvicorn
- **Architecture**: Modular transpiler with AST parsing

### Frontend
- **Framework**: Next.js 15 with React 19
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 4
- **UI Components**: Radix UI, custom components
- **HTTP Client**: Axios

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn package manager

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🚀 Usage

1. **Start the application**: Run both backend and frontend servers
2. **Upload Sigma Rules**: Use the file upload interface or paste YAML directly
3. **Translate**: Click translate to generate RML specifications
4. **Download**: Save the generated RML for use in monitoring systems

## 🌐 Language Support

### Sigma
Sigma is a generic signature format for SIEM systems. For detailed specifications and documentation, visit:
- [Sigma Specification](https://github.com/SigmaHQ/sigma/wiki)
- [Sigma Rules Repository](https://github.com/SigmaHQ/sigma)
- [Sigma Rule Writing Guide](https://github.com/SigmaHQ/sigma/wiki/Rule-Creation-Guide)

### RML (Runtime Monitoring Language)
RML is a language for defining runtime monitoring specifications. For reference documentation, visit:
- [RML Language Reference](https://rml-lang.org/)
- [RML Specification](https://rml-lang.org/specification)
- [RML Examples](https://rml-lang.org/examples)

## 🧪 Testing

Run the comprehensive test suite:

```bash
cd backend
python tests/test_all.py
```

The test suite covers:
- Basic pattern translation
- Temporal operators
- Complex conditions
- Numerical modifiers
- Quantifiers
- Edge cases

## 📁 Project Structure

```
sigma2rml/
├── backend/                 # Python FastAPI backend
│   ├── app/                # Application code
│   │   ├── core/          # Transpiler engine
│   │   ├── api/           # API endpoints
│   │   └── storage/       # File storage logic
│   ├── tests/             # Test suite
│   └── requirements.txt   # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/               # Next.js app router
│   ├── components/        # React components
│   └── lib/               # Utility libraries
└── docs/                  # Documentation
    ├── ARCHITECTURE.md    # System architecture
    ├── API_REFERENCE.md   # API documentation
    └── DIAGRAMS.md        # System diagrams
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Detailed system architecture and design
- **[API_REFERENCE.md](docs/API_REFERENCE.md)**: Complete API endpoint documentation
- **[DIAGRAMS.md](docs/DIAGRAMS.md)**: System diagrams and flowcharts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- SigmaHQ for the Sigma specification
- RML Language community for the monitoring language
- FastAPI and Next.js communities for excellent frameworks

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the test examples for usage patterns
