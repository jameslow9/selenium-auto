# AQX Trading Platform - Selenium Automation Framework

🚀 **Comprehensive automation testing framework for AQX Trading Platform using Python Selenium**

[![Tests](https://github.com/jameslow9/selenium-auto/actions/workflows/test-automation.yml/badge.svg)](https://github.com/jameslow9/selenium-auto/actions/workflows/test-automation.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.15.2-green.svg)](https://selenium-python.readthedocs.io/)

## 📋 Project Overview

This project provides a complete automation testing solution for the AQX Trading Platform, covering all critical functionalities including login, trading operations, order management, and bulk operations. Since the market is closed and live trading is not available, the framework includes mock functionality to demonstrate complete test scenarios.

## ✨ Key Features

- **Complete Test Coverage**: Login, Trading, Views, Bulk Operations
- **Mock Trading Engine**: Simulates trading operations when market is closed
- **Interactive Dashboard**: Beautiful HTML reports with charts and metrics
- **CI/CD Ready**: GitHub Actions integration with automated testing
- **Cross-Platform**: Supports multiple browsers and operating systems
- **Parallel Execution**: Run tests concurrently for faster execution
- **Screenshot Capture**: Automatic screenshots on test failures
- **Best Practices**: Following Selenium and pytest best practices

## 🏗️ Project Structure

```
selenium-auto/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest configuration and fixtures
│   └── test_aqx_platform.py          # Main test suite
├── scripts/
│   └── generate_dashboard.py         # Dashboard generator
├── .github/
│   └── workflows/
│       └── test-automation.yml       # CI/CD pipeline
├── reports/                          # Test reports and results
├── screenshots/                      # Test screenshots
├── logs/                            # Test execution logs
├── requirements.txt                 # Python dependencies
├── pytest.ini                      # Pytest configuration
├── run_tests.py                     # Test runner script
└── README.md                        # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Chrome browser (latest version)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jameslow9/selenium-auto.git
   cd selenium-auto
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run smoke tests**
   ```bash
   python run_tests.py --type smoke
   ```

## 🧪 Test Categories

### Smoke Tests (`--type smoke`)
- Basic login page loading
- Essential functionality verification

### Critical Tests (`--type critical`)
- Login with valid credentials
- Core platform functionality

### Trading Tests (`--type trading`)
- Buy order placement
- Sell order placement
- Order execution verification

### View Tests (`--type view`)
- Order notifications
- Open positions display
- Pending orders view
- Position history

### Bulk Operations (`--type bulk`)
- Bulk close positions
- Bulk delete orders

## 🔧 Usage Examples

### Basic Test Execution

```bash
# Run all tests
python run_tests.py

# Run specific test type
python run_tests.py --type critical

# Run tests in headless mode
python run_tests.py --type smoke --headless

# Run tests in parallel
python run_tests.py --type all --parallel
```

### Advanced Options

```bash
# List available tests
python run_tests.py --list

# Generate dashboard only
python run_tests.py --dashboard-only

# Run with specific browser (future feature)
python run_tests.py --browser chrome --type trading
```

### Using pytest directly

```bash
# Run with pytest
pytest tests/ -v -m smoke

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run specific test
pytest tests/test_aqx_platform.py::TestAQXLoginFunctionality::test_login_page_loads -v
```

## 📊 Test Reporting

The framework generates multiple types of reports:

### Interactive Dashboard
- **Location**: `reports/test_dashboard.html`
- **Features**: Charts, metrics, screenshots, detailed results
- **Auto-generated**: After each test run

### HTML Reports
- **Location**: `reports/*_test_report.html`
- **Features**: Detailed test results, logs, screenshots
- **Format**: Self-contained HTML files

### JSON Reports
- **Location**: `reports/test_report.json`
- **Features**: Machine-readable test results
- **Usage**: API integration, custom reporting

## 🔄 CI/CD Integration

### GitHub Actions

The project includes a complete GitHub Actions workflow:

```yaml
# Triggers
- Push to main/develop branches
- Pull requests
- Daily scheduled runs
- Manual workflow dispatch

# Features
- Multi-Python version testing (3.9, 3.10, 3.11)
- Parallel test execution
- Automatic report generation
- Artifact upload
- GitHub Pages deployment
- PR comment with results
```

### Running in CI

1. **Fork the repository**
2. **Enable GitHub Actions**
3. **Push changes** - tests run automatically
4. **View results** in Actions tab

## 🛠️ Configuration

### Test Configuration

Edit `test_aqx_platform.py` to modify:

```python
@dataclass
class TestConfig:
    base_url: str = "https://aqxtrader.aquariux.com/web"
    account_id: str = "998995"
    password: str = "u#TuWNf2J2p$"
    timeout: int = 20
    page_load_wait: int = 5
```

### Pytest Configuration

Modify `pytest.ini` for:
- Test discovery patterns
- Markers and categories
- Default options
- Warning filters

## 📸 Screenshots

Screenshots are automatically captured:
- **On test failures**: Error diagnostics
- **During test execution**: Progress tracking
- **Before/after actions**: State verification

Location: `screenshots/` directory

## 🏢 Mock Trading Engine

Since the market is closed, the framework includes a sophisticated mock trading engine:

```python
class MockAPIResponse:
    - login_success()
    - trade_order_success()
    - get_mock_positions()
```

**Features:**
- Realistic order responses
- Position tracking
- Transaction history
- Bulk operations simulation

## 🎯 Element Locators

The framework uses data-testid attributes for reliable element identification:

```python
class AQXPageLocators:
    # Login Elements
    ACCOUNT_ID_INPUT = (By.CSS_SELECTOR, '[data-testid="login-user-id"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[data-testid="login-password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-submit"]')
    
    # Trading Elements
    BUY_BUTTON = (By.CSS_SELECTOR, '[data-testid="trade-button-order-buy"]')
    SELL_BUTTON = (By.CSS_SELECTOR, '[data-testid="trade-button-order-sell"]')
```

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   ```bash
   # Install webdriver-manager
   pip install webdriver-manager
   ```

2. **Tests running slowly**
   ```bash
   # Use parallel execution
   python run_tests.py --parallel
   ```

3. **Elements not found**
   - Check if page loaded completely
   - Verify element locators
   - Increase wait times

### Debug Mode

```bash
# Run with verbose output
python run_tests.py --type smoke -v

# Check logs
cat logs/test_execution.log

# View screenshots
open screenshots/
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-test`
3. **Add tests**: Follow existing patterns
4. **Run tests**: `python run_tests.py --type all`
5. **Submit PR**: Include test results

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where possible

## 📝 Git Best Practices

This project demonstrates Git best practices:

### Branch Strategy
```bash
# Feature development
git checkout -b feature/trading-tests
git commit -m "feat: add buy/sell order tests"

# Bug fixes
git checkout -b fix/login-timeout
git commit -m "fix: increase login wait time"

# Documentation
git commit -m "docs: update README with new examples"
```

### Commit Messages
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `test:` Testing
- `refactor:` Code refactoring

## 📈 Performance Optimization

### Test Execution Speed

```python
# Parallel execution
pytest -n auto

# Headless mode
python run_tests.py --headless

# Specific test selection
pytest -m "smoke and not slow"
```

### Resource Management

- Automatic driver cleanup
- Screenshot compression
- Log rotation
- Report archiving

## 🔒 Security Considerations

- Credentials in environment variables (production)
- Secure screenshot handling
- Safe test data management
- Access control for reports

## 📚 Learning Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model](https://selenium-python.readthedocs.io/page-objects.html)
- [WebDriver Best Practices](https://selenium.dev/documentation/webdriver/)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/jameslow9/selenium-auto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jameslow9/selenium-auto/discussions)
- **Email**: [Contact](mailto:your-email@example.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AQX Trading Platform team
- Selenium WebDriver community
- Pytest framework contributors
- GitHub Actions ecosystem

---

**Happy Testing! 🎉**

*Built with ❤️ for FinTech automation*