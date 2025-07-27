#!/usr/bin/env python3
"""
AQX Trading Platform Test Runner
Main script to execute automated tests with various options
"""

import argparse
import subprocess
import sys
import os
import json
from datetime import datetime
from pathlib import Path

class TestRunner:
    """Test execution and management class"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.reports_dir = self.base_dir / "reports"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories
        self.reports_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def run_tests(self, test_type="all", browser="chrome", headless=False, parallel=False):
        """Run automated tests with specified parameters"""
        
        print(f"🚀 Starting AQX Trading Platform Tests")
        print(f"📊 Test Type: {test_type}")
        print(f"🌐 Browser: {browser}")
        print(f"👁️  Headless: {headless}")
        print(f"⚡ Parallel: {parallel}")
        print("-" * 50)
        
        # Build pytest command
        cmd = ["python", "-m", "pytest"]
        
        # Add test markers based on type
        if test_type != "all":
            cmd.extend(["-m", test_type])
        
        # Add verbosity
        cmd.append("-v")
        
        # Add HTML report
        report_name = f"{test_type}_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        cmd.extend(["--html", str(self.reports_dir / report_name)])
        cmd.append("--self-contained-html")
        
        # Add JUnit XML for CI
        junit_name = f"junit_{test_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        cmd.extend(["--junit-xml", str(self.reports_dir / junit_name)])
        
        # Add parallel execution if requested
        if parallel:
            cmd.extend(["-n", "auto"])
        
        # Set environment variables
        env = os.environ.copy()
        if headless:
            env["HEADLESS"] = "true"
        env["BROWSER"] = browser
        
        # Execute tests
        print(f"🔄 Executing command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.base_dir,
                env=env,
                capture_output=True,
                text=True
            )
            
            # Print output
            if result.stdout:
                print("📄 Test Output:")
                print(result.stdout)
            
            if result.stderr:
                print("⚠️  Warnings/Errors:")
                print(result.stderr)
            
            # Generate dashboard
            self.generate_dashboard()
            
            # Print results summary
            self.print_summary(result.returncode, report_name)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False
    
    def generate_dashboard(self):
        """Generate test dashboard"""
        try:
            print("📊 Generating test dashboard...")
            subprocess.run([
                "python", 
                str(self.base_dir / "scripts" / "generate_dashboard.py")
            ], check=True)
            print("✅ Dashboard generated successfully")
        except Exception as e:
            print(f"⚠️  Dashboard generation failed: {e}")
    
    def print_summary(self, exit_code, report_name):
        """Print test execution summary"""
        print("\n" + "="*60)
        print("📋 TEST EXECUTION SUMMARY")
        print("="*60)
        
        status = "✅ PASSED" if exit_code == 0 else "❌ FAILED"
        print(f"Status: {status}")
        print(f"HTML Report: {self.reports_dir / report_name}")
        print(f"Dashboard: {self.reports_dir / 'test_dashboard.html'}")
        print(f"Screenshots: {self.screenshots_dir}")
        print(f"Logs: {self.logs_dir}")
        
        # Try to load and display test summary
        summary_file = self.reports_dir / "test_summary.json"
        if summary_file.exists():
            try:
                with open(summary_file) as f:
                    summary = json.load(f)
                    
                print(f"\n📈 Results:")
                print(f"  Total Tests: {summary.get('total_tests', 'N/A')}")
                print(f"  Passed: {summary.get('passed', 'N/A')}")
                print(f"  Failed: {summary.get('failed', 'N/A')}")
                
                if summary.get('total_tests', 0) > 0:
                    pass_rate = (summary.get('passed', 0) / summary.get('total_tests', 1)) * 100
                    print(f"  Pass Rate: {pass_rate:.1f}%")
                    
            except Exception as e:
                print(f"⚠️  Could not load test summary: {e}")
        
        print("="*60)
    
    def list_available_tests(self):
        """List all available test markers and tests"""
        print("📋 Available Test Types:")
        print("  - all: Run all tests")
        print("  - smoke: Basic functionality tests")
        print("  - critical: Critical path tests")
        print("  - trading: Trading operations tests")
        print("  - view: View/display tests")
        print("  - bulk: Bulk operations tests")
        print("  - regression: Regression tests")
        
        print("\n🔍 Available Tests:")
        try:
            result = subprocess.run([
                "python", "-m", "pytest", "--collect-only", "-q"
            ], capture_output=True, text=True, cwd=self.base_dir)
            
            if result.stdout:
                tests = [line for line in result.stdout.split('\n') if '::test_' in line]
                for test in tests[:10]:  # Show first 10 tests
                    print(f"  - {test.strip()}")
                
                if len(tests) > 10:
                    print(f"  ... and {len(tests) - 10} more tests")
        except Exception as e:
            print(f"⚠️  Could not collect test list: {e}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="AQX Trading Platform Automated Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --type smoke                    # Run smoke tests
  python run_tests.py --type critical --headless      # Run critical tests headlessly
  python run_tests.py --type all --parallel           # Run all tests in parallel
  python run_tests.py --list                          # List available tests
        """
    )
    
    parser.add_argument(
        "--type", "-t",
        choices=["all", "smoke", "critical", "trading", "view", "bulk", "regression"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    
    parser.add_argument(
        "--browser", "-b",
        choices=["chrome", "firefox", "edge"],
        default="chrome",
        help="Browser to use for testing (default: chrome)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel (requires pytest-xdist)"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available tests and exit"
    )
    
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Generate dashboard only (no test execution)"
    )
    
    args = parser.parse_args()
    
    # Initialize test runner
    runner = TestRunner()
    
    # Handle special commands
    if args.list:
        runner.list_available_tests()
        return
    
    if args.dashboard_only:
        runner.generate_dashboard()
        return
    
    # Run tests
    success = runner.run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=args.headless,
        parallel=args.parallel
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()