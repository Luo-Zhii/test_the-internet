import os
import sys
import time
import pytest
import argparse
import webbrowser
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. CLI ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description="Execute a single Selenium test file and export an HTML report.")
parser.add_argument("target", help="Path to the test file (e.g., tests/test_checkbox.py)")
args = parser.parse_args()

target_file = args.target

# Validate file existence
if not os.path.exists(target_file):
    print(f"[ERROR] Target file not found: '{target_file}'")
    sys.exit(1)

# Auto-generate HTML report name based on the target script name
file_name = os.path.basename(target_file).replace('.py', '.html')
report_name = f"report_{file_name}"

# --- 2. ENVIRONMENT PREP & MONKEY PATCHING ---
os.environ['WDM_LOCAL'] = '1' 
os.environ['WDM_LOG'] = '0'

def cleanup_system():
    """Force kill orphaned chrome processes to prevent memory leaks."""
    if os.name == 'posix':
        subprocess.run(["pkill", "-f", "chrome"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "chromedriver"], stderr=subprocess.DEVNULL)

def pre_warm_driver():
    """Pre-cache ChromeDriver to prevent network race conditions."""
    try:
        return ChromeDriverManager().install()
    except Exception:
        return None

cleanup_system()
pre_warm_driver()

# Patch Selenium to strictly enforce Headless mode globally
original_chrome_init = webdriver.Chrome.__init__
def patched_chrome_init(self, *args, **kwargs):
    options = kwargs.get('options', Options())
    # options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    kwargs['options'] = options
    original_chrome_init(self, *args, **kwargs)

webdriver.Chrome.__init__ = patched_chrome_init

# --- 3. PYTEST HTML LOG RESCUE PLUGIN ---
class ExecutionOptimizerPlugin:
    def pytest_runtest_teardown(self, item, nextitem):
        """Micro-cooldown to release sockets."""
        time.sleep(0.5)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Attach captured logs/stdout/stderr into pytest-html report."""
        outcome = yield
        report = outcome.get_result()

        # Chỉ attach sau khi test body chạy xong
        if report.when != "call":
            return

        pytest_html = item.config.pluginmanager.getplugin("html")
        if not pytest_html:
            return

        log_parts = []

        log_parts.append(f"TEST CASE: {item.nodeid}")
        log_parts.append(f"RESULT: {report.outcome.upper()}")
        log_parts.append(f"DURATION: {report.duration:.2f}s")
        log_parts.append("=" * 80)

        if report.sections:
            for name, content in report.sections:
                if content.strip():
                    log_parts.append(f"\n--- {name.upper()} ---\n")
                    log_parts.append(content)

        if hasattr(report, "longreprtext") and report.failed:
            log_parts.append("\n--- FAILURE TRACEBACK ---\n")
            log_parts.append(report.longreprtext)

        full_log = "\n".join(log_parts)

        extras = getattr(report, "extras", [])

        # Link trong cột Links: bấm vào sẽ mở log dạng text
        extras.append(
            pytest_html.extras.text(
                full_log,
                name="Detailed Execution Logs"
            )
        )

        report.extras = extras
# --- 4. EXECUTION ---
print("\n" + "="*60)
print(f"🎯 TARGETING SINGLE TEST FILE: {target_file}")
print("="*60)

exit_code = pytest.main([
    target_file,
    "-v",
    "-s",
    f"--html={report_name}",
    "--self-contained-html",
    "--capture=tee-sys",
    "--show-capture=all",
    "--reruns", "1",
    "--timeout", "120",

    "--log-cli-level=INFO",
    "--log-level=INFO",
    "--log-format=%(asctime)s [%(levelname)s] %(message)s",
    "--log-date-format=%H:%M:%S"
], plugins=[ExecutionOptimizerPlugin()])

# --- 5. POST-EXECUTION ---
print("\n" + "="*60)
report_path = f"file://{os.path.abspath(report_name)}"
print(f"Execution Complete! Opening Report: {report_name}")
print("="*60)

webbrowser.open(report_path)