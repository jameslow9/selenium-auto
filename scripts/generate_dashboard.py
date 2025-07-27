#!/usr/bin/env python3
"""
Test Dashboard Generator for AQX Trading Platform
Generates an interactive HTML dashboard with test results
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_test_results():
    """Load test results from various sources"""
    results = {
        "summary": {},
        "test_details": [],
        "screenshots": [],
        "logs": []
    }
    
    # Load test summary
    summary_file = Path("reports/test_summary.json")
    if summary_file.exists():
        with open(summary_file) as f:
            results["summary"] = json.load(f)
    
    # Load detailed test report
    report_file = Path("reports/test_report.json")
    if report_file.exists():
        with open(report_file) as f:
            report_data = json.load(f)
            results["test_details"] = report_data.get("test_results", [])
    
    # Find screenshots
    screenshot_dir = Path("screenshots")
    if screenshot_dir.exists():
        results["screenshots"] = [
            str(f.relative_to(screenshot_dir)) 
            for f in screenshot_dir.glob("*.png")
        ]
    
    # Find logs
    log_dir = Path("logs")
    if log_dir.exists():
        results["logs"] = [
            str(f.relative_to(log_dir)) 
            for f in log_dir.glob("*.log")
        ]
    
    return results

def generate_dashboard_html(results):
    """Generate interactive HTML dashboard"""
    
    summary = results.get("summary", {})
    test_details = results.get("test_details", [])
    screenshots = results.get("screenshots", [])
    
    # Calculate metrics
    total_tests = summary.get("total_tests", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AQX Trading Platform - Test Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .header .subtitle {{
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-value {{
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .passed {{ color: #27ae60; }}
        .failed {{ color: #e74c3c; }}
        .total {{ color: #3498db; }}
        .rate {{ color: #9b59b6; }}
        
        .charts-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .test-details {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin-bottom: 30px;
        }}
        
        .test-item {{
            border-bottom: 1px solid #ecf0f1;
            padding: 15px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .test-item:last-child {{
            border-bottom: none;
        }}
        
        .test-name {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .test-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .status-passed {{
            background: #d5f4e6;
            color: #27ae60;
        }}
        
        .status-failed {{
            background: #fadbd8;
            color: #e74c3c;
        }}
        
        .screenshots-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        .screenshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .screenshot-item {{
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .screenshot-item:hover {{
            transform: scale(1.05);
        }}
        
        .screenshot-item img {{
            width: 100%;
            height: auto;
            cursor: pointer;
        }}
        
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            text-align: center;
            margin-top: 20px;
        }}
        
        @media (max-width: 768px) {{
            .charts-container {{
                grid-template-columns: 1fr;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AQX Trading Platform</h1>
            <div class="subtitle">Automated Test Results Dashboard</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value total">{total_tests}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric-card">
                <div class="metric-value passed">{passed}</div>
                <div class="metric-label">Tests Passed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value failed">{failed}</div>
                <div class="metric-label">Tests Failed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value rate">{pass_rate:.1f}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
        </div>
        
        <div class="charts-container">
            <div class="chart-card">
                <h3>Test Results Distribution</h3>
                <canvas id="resultsChart" width="400" height="200"></canvas>
            </div>
            <div class="chart-card">
                <h3>Test Categories</h3>
                <canvas id="categoriesChart" width="400" height="200"></canvas>
            </div>
        </div>
        
        <div class="test-details">
            <h3>📋 Detailed Test Results</h3>
            <div class="test-list">
"""
    
    # Add test details
    for test in test_details:
        test_name = test.get("test_name", "Unknown Test")
        status = test.get("status", "UNKNOWN")
        status_class = "status-passed" if status == "PASSED" else "status-failed"
        
        html_content += f"""
                <div class="test-item">
                    <div class="test-name">{test_name}</div>
                    <div class="test-status {status_class}">{status}</div>
                </div>
"""
    
    html_content += """
            </div>
        </div>
"""
    
    # Add screenshots section if available
    if screenshots:
        html_content += """
        <div class="screenshots-section">
            <h3>📸 Test Screenshots</h3>
            <div class="screenshot-grid">
"""
        for screenshot in screenshots[:12]:  # Limit to 12 screenshots
            html_content += f"""
                <div class="screenshot-item">
                    <img src="screenshots/{screenshot}" alt="Test Screenshot" onclick="window.open('screenshots/{screenshot}', '_blank')">
                </div>
"""
        html_content += """
            </div>
        </div>
"""
    
    html_content += f"""
        <div class="timestamp">
            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
    
    <script>
        // Results chart
        const resultsCtx = document.getElementById('resultsChart').getContext('2d');
        new Chart(resultsCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['Passed', 'Failed'],
                datasets: [{{
                    data: [{passed}, {failed}],
                    backgroundColor: ['#27ae60', '#e74c3c'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Categories chart (mock data for demonstration)
        const categoriesCtx = document.getElementById('categoriesChart').getContext('2d');
        new Chart(categoriesCtx, {{
            type: 'bar',
            data: {{
                labels: ['Login', 'Trading', 'Views', 'Bulk Ops'],
                datasets: [{{
                    label: 'Tests',
                    data: [2, 4, 4, 2],
                    backgroundColor: ['#3498db', '#9b59b6', '#f39c12', '#1abc9c'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    return html_content

def main():
    """Main function to generate dashboard"""
    print("🔄 Generating test dashboard...")
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Load test results
    results = load_test_results()
    
    # Generate HTML dashboard
    dashboard_html = generate_dashboard_html(results)
    
    # Save dashboard
    dashboard_path = Path("reports/test_dashboard.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print(f"✅ Dashboard generated: {dashboard_path}")
    print(f"🌐 Open file://{dashboard_path.absolute()} in your browser")

if __name__ == "__main__":
    main()