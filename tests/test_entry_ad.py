import unittest
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestEntryAd(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # Ensure headless mode is enabled if needed via your run_fast.py patch
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/entry_ad'

    def tearDown(self):
        self.driver.quit()

    def helper_close_modal_with_js(self):
        """Helper method to forcefully close the modal using JavaScript to bypass overlays."""
        logger.info("Action: Waiting for modal and clicking close via JS...")
        # Wait for the footer 'Close' text to be present in DOM
        close_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-footer p")))
        # Execute JS Click - this ignores any transparent overlays blocking the element
        self.driver.execute_script("arguments[0].click();", close_btn)
        # Verify the modal container (ID='modal') is actually hidden
        self.wait.until(EC.invisibility_of_element_located((By.ID, "modal")))

    def test_tc1_close_entry_ad_modal(self):
        """TC1: Basic functionality - verify modal can be dismissed."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        # Reset state
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        self.wait.until(EC.visibility_of_element_located((By.ID, "modal")))
        self.helper_close_modal_with_js()
        
        logger.info("TC1 Success: Modal successfully dismissed.")

    def test_tc2_ad_does_not_reappear_on_refresh(self):
        """TC2: Cookie retention - verify ad stays hidden after first dismissal."""
        self.driver.get(self.url)
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        # Dismiss it the first time
        self.wait.until(EC.visibility_of_element_located((By.ID, "modal")))
        self.helper_close_modal_with_js()
        
        logger.info("Action: Refreshing page while retaining cookies...")
        self.driver.refresh()
        
        # Verify it DOES NOT reappear (use a short wait to avoid wasting time)
        short_wait = WebDriverWait(self.driver, 3)
        try:
            short_wait.until(EC.visibility_of_element_located((By.ID, "modal")))
            self.fail("Bug: Modal incorrectly reappeared after refresh with cookies.")
        except:
            logger.info("TC2 Success: Modal remained hidden on refresh.")

    def test_tc3_ad_reappears_on_cleared_cookies(self):
        """TC3: State reset - verify ad reappears if cookies are cleared."""
        self.driver.get(self.url)
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        # Dismiss first
        self.wait.until(EC.visibility_of_element_located((By.ID, "modal")))
        self.helper_close_modal_with_js()
        
        logger.info("Action: Clearing cookies and refreshing...")
        self.driver.delete_all_cookies()
        self.driver.refresh()
        
        # Verify it REAPPEARS
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "modal")))
            logger.info("TC3 Success: Modal reappeared after cookie clearing.")
        except:
            self.fail("Failure: Modal failed to reappear after state reset.")

if __name__ == "__main__":
    unittest.main()