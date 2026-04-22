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
logger = logging.getLogger(__name__)

class TestDynamicContent(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # Headless mode is handled by your run_fast.py patch
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/dynamic_content'

    def tearDown(self):
        self.driver.quit()

    def get_content_state(self):
        """
        Helper to return current images and texts.
        The selector uses '>' to target only direct children rows, 
        avoiding the parent container 'large-10' confusion.
        """
        # Specific selector to target the 3 content rows only
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#content > .row:not(.large-centered)")
        
        images = []
        texts = []
        
        for row in rows:
            img = row.find_element(By.CSS_SELECTOR, ".large-2 img").get_attribute("src")
            txt = row.find_element(By.CSS_SELECTOR, ".large-10").text.strip()
            images.append(img)
            texts.append(txt)
            
        return images, texts

    def test_tc1_content_structure_intact(self):
        """TC1: Verify that 3 rows of images and text blocks always render."""
        logger.info(f"Navigating to: {self.url}")
        self.driver.get(self.url)
        
        images, texts = self.get_content_state()
        
        logger.info(f"Detected {len(images)} images and {len(texts)} text blocks.")
        
        # This will now correctly return 3 instead of 4
        self.assertEqual(len(images), 3, "Failure: Image count should be exactly 3.")
        self.assertEqual(len(texts), 3, "Failure: Text block count should be exactly 3.")
        
        for i, (img, txt) in enumerate(zip(images, texts)):
            self.assertIsNotNone(img, f"Row {i+1}: Image source is missing.")
            self.assertGreater(len(txt), 10, f"Row {i+1}: Text content is too short.")

    def test_tc2_content_changes_on_refresh(self):
        """TC2: Validate that standard load changes at least some of the dynamic content."""
        logger.info("Executing TC2: Testing content randomization on refresh...")
        self.driver.get(self.url)
        initial_images, initial_texts = self.get_content_state()
        
        # Retry up to 3 times to account for rare 'same-random' luck
        for attempt in range(3):
            logger.info(f"Refresh attempt #{attempt + 1}")
            self.driver.refresh()
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content .row")))
            
            refreshed_images, refreshed_texts = self.get_content_state()
            
            if initial_images != refreshed_images or initial_texts != refreshed_texts:
                logger.info("Success: Content successfully randomized.")
                return
                
        self.fail("Critical Failure: Content remained identical across 3 refreshes.")

    def test_tc3_static_content_parameter(self):
        """TC3: Verify that '?with_content=static' locks the first two rows."""
        static_url = self.url + "?with_content=static"
        logger.info(f"Navigating to Static Content URL: {static_url}")
        self.driver.get(static_url)
        
        initial_images, initial_texts = self.get_content_state()
        
        self.driver.refresh()
        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content .row")))
        refreshed_images, refreshed_texts = self.get_content_state()
        
        logger.info("Comparing the first two rows for static persistence...")
        
        # Check first 2 rows specifically
        self.assertEqual(initial_images[:2], refreshed_images[:2], "Error: Static images changed!")
        self.assertEqual(initial_texts[:2], refreshed_texts[:2], "Error: Static texts changed!")
        
        # Log the 3rd row shift for debugging
        if initial_texts[2] != refreshed_texts[2]:
            logger.info("Success: First two rows remained static while the third row changed.")
        else:
            logger.info("Observation: All rows remained identical this time (Randomness luck).")

if __name__ == "__main__":
    unittest.main()