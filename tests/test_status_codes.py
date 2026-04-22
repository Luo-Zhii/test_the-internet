import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize logger for traceability
logger = logging.getLogger(__name__)

class TestStatusCodes(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/status_codes'

    def tearDown(self):
        self.driver.quit()

    def helper_verify_status_code(self, code):
        """Helper to navigate, click, and verify exact output safely."""
        logger.info(f"Step 1: Navigating to base URL for status code {code}")
        self.driver.get(self.url)
        
        logger.info(f"Step 2: Clicking the link for status {code}")
        link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, code)))
        link.click()
        
        logger.info("Step 3: Verifying the landing page text containing the status code")
        status_text = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".example p"))).text
        self.assertIn(f"This page returned a {code} status code.", status_text, f"The message did not reflect status {code}.")
        
        # CRITICAL FIX: Removed self.driver.back()
        # Navigating back via browser history in headless mode causes flaky DOM states.
        # It is strictly safer to let the next test case re-trigger self.driver.get(self.url)
        logger.info(f"Result: Status {code} verified successfully without triggering back-navigation flakiness.")

    def test_tc1_status_code_200_ok(self):
        """TC1: Verify proper routing and message for successful 200 code OK."""
        self.helper_verify_status_code("200")

    def test_tc2_status_code_301_moved(self):
        """TC2: Verify proper routing and message for 301 Moved Permanently."""
        self.helper_verify_status_code("301")

    def test_tc3_status_code_404_not_found(self):
        """TC3: Verify proper routing and message for 404 Not Found."""
        self.helper_verify_status_code("404")

    def test_tc4_status_code_500_server_error(self):
        """TC4: Verify proper routing and message for 500 Internal Server error."""
        self.helper_verify_status_code("500")

if __name__ == "__main__":
    unittest.main()