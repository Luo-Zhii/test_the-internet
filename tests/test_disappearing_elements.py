import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Initialize professional logger
logger = logging.getLogger(__name__)

class TestDisappearingElements(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # Headless mode is typically managed by your run_fast.py patch
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15) # Increased timeout for parallel stability
        self.url = 'https://the-internet.herokuapp.com/disappearing_elements'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_verify_permanent_links(self):
        """TC1: Verify that guaranteed navigation links are always present on the UI."""
        logger.info(f"Step 1: Navigating to {self.url}")
        self.driver.get(self.url)
        
        # BUG FIX: The link text on Herokuapp is 'Contact Us', not 'Contact'
        # 'Portfolio' is also a permanent link that should be verified.
        permanent_links = ["Home", "About", "Contact Us", "Portfolio"]
        
        for text in permanent_links:
            logger.info(f"Checking for permanent link: {text}")
            # Use LINK_TEXT for exact match verification
            element = self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, text)))
            self.assertTrue(element.is_displayed(), f"Link '{text}' should be visible on the page.")
            
        logger.info("TC1 Result: All permanent links verified successfully.")

    def test_tc2_gallery_appears_on_refresh(self):
        """TC2: Refresh the page up to 5 times to catch the volatile 'Gallery' link."""
        logger.info("Step 1: Starting volatile element detection for 'Gallery'...")
        self.driver.get(self.url)
        
        found = False
        for i in range(5):
            logger.info(f"Refresh Attempt #{i+1}: Searching for Gallery link...")
            elements = self.driver.find_elements(By.LINK_TEXT, "Gallery")
            
            if len(elements) > 0 and elements[0].is_displayed():
                logger.info("Success: Gallery link detected! Executing click...")
                elements[0].click()
                
                # Verify navigation leads to the intentional 404 page
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                self.assertIn("Not Found", self.driver.page_source)
                found = True
                break
                
            self.driver.refresh()
            # Wait for a static element to ensure page reload is complete
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))

        if not found:
            self.fail("Result Failed: 'Gallery' link did not appear after 5 refreshes.")
        else:
            logger.info("TC2 Result: Gallery interaction verified.")

if __name__ == "__main__":
    unittest.main()