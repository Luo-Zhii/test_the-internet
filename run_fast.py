import os

# --- CRITICAL FIX FOR MULTI-THREADING DEADLOCK ---
# Force webdriver_manager to bypass file locking when running in parallel
os.environ['WDM_LOCAL'] = '1' 
os.environ['WDM_LOG'] = '0'

import pytest
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. Save the original Chrome initialization function
original_chrome_init = webdriver.Chrome.__init__

# 2. Create a custom initialization function to force headless mode
def headless_chrome_init(self, *args, **kwargs):
    # Get current options (if any) or create new ones
    options = kwargs.get('options', Options())
    
    # Force Headless mode and set a fixed resolution to prevent UI errors
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    
    # Update the configuration
    kwargs['options'] = options
    
    # Call the original function for Selenium to initialize
    original_chrome_init(self, *args, **kwargs)

# 3. Monkey Patching: Replace the original function with our custom one
webdriver.Chrome.__init__ = headless_chrome_init

print("=========================================")
print("🚀 HEADLESS MODE ENABLED (Max 4 Workers) 🚀")
print("=========================================")

# 4. Trigger Pytest with exactly 4 workers instead of 'auto' to prevent CPU/RAM overload
pytest.main(["tests/", "-n", "4", "--html=report.html", "--self-contained-html"])

# 5. Automatically open the HTML report after execution
report_path = f"file://{os.path.abspath('report.html')}"
print(f"\nAutomatically opening report at: {report_path}")
webbrowser.open(report_path)