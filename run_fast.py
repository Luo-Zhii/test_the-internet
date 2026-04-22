import os
import time
import pytest
import logging
import webbrowser
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION & ENVIRONMENT SETUP ---
os.environ['WDM_LOCAL'] = '1' 
os.environ['WDM_LOG'] = '0'

def cleanup_system():
    """Force kill any orphaned chrome/chromedriver processes to prevent memory leaks."""
    print(" Step 1: Cleaning up zombie processes...")
    try:
        if os.name == 'posix':  # Linux/Mac
            subprocess.run(["pkill", "-f", "chrome"], stderr=subprocess.DEVNULL)
            subprocess.run(["pkill", "-f", "chromedriver"], stderr=subprocess.DEVNULL)
        else:  # Windows
            os.system("taskkill /f /im chrome.exe /t >nul 2>&1")
            os.system("taskkill /f /im chromedriver.exe /t >nul 2>&1")
    except Exception as e:
        print(f" Cleanup warning: {e}")

def pre_warm_driver():
    """Download and cache the driver once before parallel execution to avoid race conditions."""
    print(" Step 2: Pre-warming ChromeDriver (Singleton Pattern)...")
    try:
        path = ChromeDriverManager().install()
        print(f" Driver is ready at: {path}")
        return path
    except Exception as e:
        print(f" Critical Error: Could not prepare driver. {e}")
        return None

# Execute Prep Tasks
cleanup_system()
pre_warm_driver()

# --- MONKEY PATCHING FOR GLOBAL HEADLESS ENFORCEMENT ---
original_chrome_init = webdriver.Chrome.__init__

def patched_chrome_init(self, *args, **kwargs):
    """Injects headless and stability options into every Chrome instance automatically."""
    options = kwargs.get('options', Options())
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Suppress logging clutter in terminal
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    kwargs['options'] = options
    original_chrome_init(self, *args, **kwargs)

# Apply the patch to Selenium's core
webdriver.Chrome.__init__ = patched_chrome_init

# --- PYTEST DYNAMIC PLUGIN (STABILIZATION & REPORTING) ---
# --- PYTEST DYNAMIC PLUGIN (STABILIZATION & REPORTING) ---
class ExecutionOptimizerPlugin:
    """Plugin to handle inter-test cooldowns and force log capture for HTML reports."""
    
    def pytest_runtest_teardown(self, item, nextitem):
        """Inject a micro-cooldown to allow the OS to release network sockets."""
        time.sleep(0.5) 

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """Rescue and attach console logs for PASSED tests before pytest-html purges them."""
        outcome = yield
        report = outcome.get_result()
        
        # We only care about the actual execution phase of successfully passed tests
        if report.when == "call" and report.passed:
            
            # STEP 1: Extract all captured logs, stdout, and stderr from Pytest's internal memory
            log_sections = []
            for section_name, section_content in report.sections:
                log_sections.append(f"=== {section_name.upper()} ===\n{section_content}")
            
            full_log = "\n\n".join(log_sections)
            
            # STEP 2: Forcefully inject the extracted text back into the HTML report
            if full_log.strip():
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extra = getattr(report, "extra", [])
                    # Append the rescued logs as a distinct text block
                    extra.append(pytest_html.extras.text(full_log, name="Detailed Execution Logs"))
                    report.extra = extra
# --- MAIN EXECUTION ---
print("\n" + "="*45)
print(" STARTING ROBUST MULTI-THREADED TEST SUITE ")
print("="*45)

# Execution flags explanation:
# -n 2: Runs 2 workers (Safest for local RAM management)
# --dist=loadfile: Ensures all tests in one file run on the same worker (state consistency)
# --reruns 1: Auto-retry flaky tests once if they fail due to network jitter
# --timeout 120: Hard-kill any test hanging longer than 2 minutes
# --- MAIN EXECUTION ---
exit_code = pytest.main([
    "tests/", 
    "-n", "4",
    "-v", 
    "--html=report.html", 
    "--self-contained-html",
    "--capture=tee-sys",
    "--dist=loadfile",
    "--reruns", "1",
    "--timeout", "60",
    
    # --- SENIOR FIX: X-RAY DEBUGGING MODE ---
    # Lowering the threshold to DEBUG forces Selenium and urllib3 
    # to expose every single underlying HTTP request and DOM action.
    "--log-cli-level=DEBUG",
    "--log-level=DEBUG",
    # "--log-cli-level=INFO",
    # "--log-level=INFO",
    "--log-format=%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    "--log-date-format=%H:%M:%S"
], plugins=[ExecutionOptimizerPlugin()])

# --- POST-EXECUTION ---
print("\n" + "="*45)
report_path = f"file://{os.path.abspath('report.html')}"
print(f"TEST RUN COMPLETE. Opening Report...")
print(f"Location: {report_path}")
print("="*45)

webbrowser.open(report_path)