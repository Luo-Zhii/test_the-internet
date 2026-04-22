import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestFileDownload(unittest.TestCase):
    def setUp(self):
        self.download_dir = os.path.join(os.getcwd(), "test_downloads")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        prefs = {"download.default_directory": self.download_dir}
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()
        # Cleanup downloads
        for file in os.listdir(self.download_dir):
            os.remove(os.path.join(self.download_dir, file))
        os.rmdir(self.download_dir)

    def test_file_download_first_item(self):
        self.driver.get('https://the-internet.herokuapp.com/download')
        
        # Locate the first download link
        download_links = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".example a")))
        first_link = download_links[0]
        file_name = first_link.text
        first_link.click()
        
        # Wait for file to appear in download dir
        file_path = os.path.join(self.download_dir, file_name)
        
        # Polling for file existence as Selenium doesn't track download completion
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                break
            time.sleep(0.5)
            
        self.assertTrue(os.path.exists(file_path), f"File {file_name} was not downloaded")

if __name__ == "__main__":
    unittest.main()
