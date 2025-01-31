# Password Strength Analyzer

A Python-based tool for comprehensive password security analysis, featuring advanced pattern detection, common password checks, and security recommendations.

## Features

- Basic password analysis:
  - Length verification
  - Character complexity checks
  - Special character validation
  - Score-based strength assessment

- Advanced security checks:
  - Common password detection
  - Keyboard pattern analysis
  - Password entropy analysis
  - Dictionary word similarity check

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/password-strength-analyzer.git
cd password-strength-analyzer
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

1. Basic password analysis:
```bash
python main.py "yourpassword"
```

2. Detailed analysis:
```bash
python main.py "yourpassword" -v
```

3. Analyze multiple passwords:
```bash
python main.py "password1" "password2" "password3"
```

4. Analyze passwords from file:
```bash
python main.py -f passwords.txt
```

5. JSON output:
```bash
python main.py "yourpassword" --json
```

### As a Module

```python
from src.analyzer.password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
result = analyzer.analyze_password("yourpassword")
print(result)
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```

4. Push to the branch:
```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

For coverage report:
```bash
python -m pytest --cov=src tests/
```

## Project Structure

```
password-strength-analyzer/
├── src/
│   └── analyzer/
│       ├── __init__.py
│       ├── password_analyzer.py
│       └── advanced_analyzer.py
├── tests/
│   ├── __init__.py
│   └── test_password_analyzer.py
├── data/
│   └── common_passwords.txt
├── main.py
├── requirements.txt
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Improvements

- [ ] API integration for leaked password verification
- [ ] Machine learning-based pattern detection
- [ ] Password generation suggestions
- [ ] Web interface
- [ ] Multiple language support