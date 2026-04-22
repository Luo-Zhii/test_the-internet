import unittest
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize professional logger
logger = logging.getLogger(__name__)

class TestFileUpload(unittest.TestCase):
    def setUp(self):
        # SENIOR FIX: Removed ChromeDriverManager().install()
        # The driver is already pre-warmed and globally patched by run_fast.py.
        # Calling webdriver.Chrome() here automatically inherits the headless options.
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/upload'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_upload_valid_file(self):
        """TC1: Upload a standard valid file and verify success message."""
        logger.info(f"Step 1: Navigating to {self.url}")
        self.driver.get(self.url)
        
        # Create a dummy file for testing purposes
        test_file_path = os.path.abspath("temp_upload_test.txt")
        with open(test_file_path, "w") as f:
            f.write("Selenium automated file upload test.")
            
        try:
            logger.info("Step 2: Locating the file input element and injecting file path...")
            upload_input = self.wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
            upload_input.send_keys(test_file_path)
            
            logger.info("Step 3: Clicking the upload submit button...")
            submit_btn = self.driver.find_element(By.ID, "file-submit")
            submit_btn.click()
            
            logger.info("Step 4: Waiting for the success header to appear...")
            success_header = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3"))).text
            logger.info(f"Verification: Found header '{success_header}'")
            
            self.assertEqual(success_header, "File Uploaded!", "The file upload success message was not displayed.")
            
        finally:
            # CLEANUP: Always remove the temporary file to keep the workspace clean
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                logger.info("Cleanup: Temporary test file removed.")

    def test_tc2_upload_empty_submission(self):
        """TC2: Submit the upload form without selecting any file."""
        logger.info("Step 1: Navigating to the upload page...")
        self.driver.get(self.url)
        
        logger.info("Step 2: Clicking submit without attaching a file...")
        submit_btn = self.driver.find_element(By.ID, "file-submit")
        submit_btn.click()
        
        logger.info("Step 3: Validating system response to empty submission...")
        # Herokuapp responds with an Internal Server Error (500) for empty uploads
        error_message = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
        logger.info(f"Verification: Found error message '{error_message}'")
        
        self.assertEqual(error_message, "Internal Server Error", "The system did not throw the expected error for an empty upload.")

if __name__ == "__main__":
    unittest.main()