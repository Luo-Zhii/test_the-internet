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

    def tearDown(self):
        self.driver.quit()

    def test_file_upload_success(self):
        self.driver.get('https://the-internet.herokuapp.com/upload')
        
        # Get the ABSOLUTE path of the current running script file itself
        file_to_upload = os.path.abspath(__file__)
        
        # Send the absolute path to the file input element
        upload_input = self.wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
        upload_input.send_keys(file_to_upload)
        
        # Click Submit
        self.driver.find_element(By.ID, "file-submit").click()
        
        # Verify success message
        header = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
        self.assertEqual(header.text, "File Uploaded!")

if __name__ == "__main__":
    unittest.main()