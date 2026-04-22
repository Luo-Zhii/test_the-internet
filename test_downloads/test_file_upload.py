import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestFileUpload(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/upload'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_upload_valid_file(self):
        """TC1: Verify that providing a valid local file path properly completes the upload sequence."""
        self.driver.get(self.url)
        file_to_upload = os.path.abspath(__file__)
        file_name = os.path.basename(file_to_upload)
        
        # Injection
        upload_input = self.wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
        upload_input.send_keys(file_to_upload)
        
        # Click Submit
        self.driver.find_element(By.ID, "file-submit").click()
        
        # Result Validation
        header = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        self.assertEqual(header.text, "File Uploaded!")
        
        uploaded_file = self.wait.until(EC.visibility_of_element_located((By.ID, "uploaded-files")))
        self.assertEqual(uploaded_file.text.strip(), file_name, "Uploaded file name text should match the submitted file.")

    def test_tc2_upload_empty_submission(self):
        """TC2: Submit the form without providing any file input."""
        print("\\nAction: Injecting invalid data (empty file upload).")
        print("Expected: System should reject and show error.")
        self.driver.get(self.url)
        
        old_body = self.driver.find_element(By.TAG_NAME, "body")
        self.driver.find_element(By.ID, "file-submit").click()
        
        # Wait for page reload
        self.wait.until(EC.staleness_of(old_body))
        
        # The app throws a 500 error when uploading empty
        header = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(header.text, "Internal Server Error", "Submitting empty upload should result in strict server error on this platform.")
        print("Actual: Error message verified successfully.")

if __name__ == "__main__":
    unittest.main()