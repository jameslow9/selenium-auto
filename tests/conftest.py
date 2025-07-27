"""
Pytest configuration and fixtures for AQX Trading Platform tests
"""

import pytest
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment - create directories and initialize"""
    directories = ["screenshots", "reports", "logs", "test_data"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create test run info
    test_run_info = {
        "test_run_id": f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "start_time": datetime.now().isoformat(),
        "environment": "test",
        "browser": "chrome"
    }
    
    with open("reports/test_run_info.json", "w") as f:
        json.dump(test_run_info, f, indent=2)

@pytest.fixture
def chrome_driver():
    """Chrome WebDriver fixture"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    
    # For headless mode (uncomment if needed)
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(
        service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    driver.quit()

@pytest.fixture
def test_data():
    """Test data fixture"""
    return {
        "valid_credentials": {
            "account_id": "998995",
            "password": "u#TuWNf2J2p$"
        },
        "invalid_credentials": {
            "account_id": "000000",
            "password": "wrongpassword"
        },
        "test_symbols": ["BTCUSD", "ETHUSD", "LTCUSD"],
        "test_quantities": [0.1, 0.5, 1.0]
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and screenshots on failure"""
    outcome = yield
    report = outcome.get_result()
    
    # Take screenshot on failure
    if report.when == "call" and report.failed:
        driver = None
        if hasattr(item.instance, 'driver'):
            driver = item.instance.driver
        elif 'chrome_driver' in item.fixturenames:
            driver = item.funcargs['chrome_driver']
        
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"screenshots/failure_{item.name}_{timestamp}.png"
            driver.save_screenshot(screenshot_name)
            
            # Add screenshot to HTML report
            if hasattr(report, 'extra'):
                report.extra.append({
                    'name': 'Screenshot',
                    'path': screenshot_name,
                    'type': 'image'
                })

def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line("markers", "smoke: Basic smoke tests")
    config.addinivalue_line("markers", "critical: Critical functionality tests")
    config.addinivalue_line("markers", "trading: Trading operations tests")
    config.addinivalue_line("markers", "view: View/Display tests")
    config.addinivalue_line("markers", "bulk: Bulk operations tests")
    config.addinivalue_line("markers", "regression: Regression tests")

def pytest_sessionfinish(session, exitstatus):
    """Generate final test report after session ends"""
    # Create summary report
    passed = session.testscollected - session.testsfailed
    summary = {
        "total_tests": session.testscollected,
        "passed": passed,
        "failed": session.testsfailed,
        "exit_status": exitstatus,
        "end_time": datetime.now().isoformat()
    }
    
    with open("reports/test_summary.json", "w") as f:
        json.dump(summary, f, indent=2)