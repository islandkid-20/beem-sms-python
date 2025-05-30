# Beem SMS Python Package - Complete File Structure

```
beem-sms-python/
├── beem_sms/                    # Main package directory
│   ├── __init__.py             # Package initialization and exports
│   ├── client.py               # Main SMS client implementation
│   ├── exceptions.py           # Custom exception classes
│   ├── validators.py           # Phone number validation utilities
│   └── cli.py                  # Command-line interface
│
├── tests/                       # Test suite
│   ├── __init__.py             # Test package initialization
│   ├── conftest.py             # Pytest fixtures and configuration
│   ├── test_client.py          # Tests for main client
│   └── test_validators.py      # Tests for validators
│
├── .github/                     # GitHub configuration
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline configuration
│
├── docs/                        # Documentation (optional)
│   ├── conf.py
│   ├── index.rst
│   └── ...
│
├── setup.py                     # Package setup (legacy)
├── pyproject.toml              # Modern Python project configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Makefile                    # Development automation
├── .pre-commit-config.yaml     # Pre-commit hooks configuration
├── README.md                   # Project documentation
├── LICENSE                     # License file (create MIT license)
├── .gitignore                  # Git ignore rules
└── CHANGELOG.md                # Version history (optional)
```

## Key Files Overview

### Core Package (`beem_sms/`)
- **`__init__.py`** - Exports all public classes and functions
- **`client.py`** - Main BeemSMSClient with all SMS functionality
- **`exceptions.py`** - Custom exception hierarchy
- **`validators.py`** - Phone number validation utilities
- **`cli.py`** - Command-line interface implementation

### Tests (`tests/`)
- **`conftest.py`** - Shared test fixtures
- **`test_client.py`** - Comprehensive client tests
- **`test_validators.py`** - Validator utility tests

### Configuration Files
- **`setup.py`** - Package metadata and dependencies
- **`pyproject.toml`** - Modern packaging configuration with tool settings
- **`requirements.txt`** - Runtime dependencies
- **`requirements-dev.txt`** - Development dependencies
- **`Makefile`** - Development workflow automation
- **`.pre-commit-config.yaml`** - Code quality checks
- **`.github/workflows/ci.yml`** - CI/CD pipeline

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/islandkid-20/beem-sms-python.git
   cd beem-sms-python
   ```

2. **Set up development environment:**
   ```bash
   make dev-setup
   ```

3. **Run tests:**
   ```bash
   make test
   ```

4. **Check code quality:**
   ```bash
   make check
   ```

5. **Build package:**
   ```bash
   make build
   ```

## Usage Examples

### Basic Python Usage
```python
from beem_sms import BeemSMSClient

client = BeemSMSClient("api_key", "secret_key")
response = client.send_sms("YourApp", "+255742892731", "Hello!")
```

### CLI Usage
```bash
beem-sms send --sender "YourApp" --message "Hello!" \
    --recipients "+255742892731"
```

### Bulk SMS
```python
results = client.send_bulk_sms(
    "YourApp", 
    ["+255742892731", "+255783346386"], 
    "Bulk message"
)
```