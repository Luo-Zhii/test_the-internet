import unittest
import time  # CRITICAL: Added missing import to resolve NameError
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize logger for traceability
logger = logging.getLogger(__name__)

class TestInfiniteScroll(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # Headless mode is typically forced via run_fast.py monkey patch
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/infinite_scroll'

    def tearDown(self):
        self.driver.quit()

    def get_paragraph_count(self):
        """Helper to count injected paragraph blocks (div.jscroll-added)."""
        return len(self.driver.find_elements(By.CLASS_NAME, "jscroll-added"))

    def test_tc1_initial_content_load(self):
        """TC1: Verify that initial content chunks are present on page load."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        # Ensure the dynamic content container is ready
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jscroll-added")))
        
        count = self.get_paragraph_count()
        logger.info(f"Initial block count: {count}")
        self.assertGreaterEqual(count, 1, "Expected at least one paragraph on load.")

    def test_tc2_scroll_loads_more_content(self):
        """TC2: Scroll heavily to trigger AJAX calls and verify content injection."""
        logger.info("Starting TC2: Infinite Scroll Load Test")
        self.driver.get(self.url)
        
        # Capture the state before scrolling
        initial_count = self.get_paragraph_count()
        logger.info(f"Initial count before scrolling: {initial_count}")

        # Execute 3 scroll actions to trigger multiple AJAX batches
        for i in range(3):
            logger.info(f"Action: Scrolling to bottom (Attempt #{i+1})")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # THE OBSERVER EFFECT: We must wait for the network request to finish.
            # Using a 1.5s sleep to ensure DOM update in headless environments.
            time.sleep(1.5) 
            
            current_count = self.get_paragraph_count()
            logger.info(f"Current paragraph count: {current_count}")
            
        # Final validation
        final_count = self.get_paragraph_count()
        self.assertGreater(final_count, initial_count, "Result Failed: No new content was loaded.")
        logger.info(f"TC2 Success: Content grew from {initial_count} to {final_count} blocks.")

if __name__ == "__main__":
    unittest.main()