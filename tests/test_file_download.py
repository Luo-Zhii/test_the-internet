import unittest
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

class TestFileDownload(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        self.download_dir = os.path.abspath("test_downloads")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Set download preferences for Headless Chrome
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # CRITICAL: Allow downloads in headless mode via CDP
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": self.download_dir
        })
        
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/download"

    def tearDown(self):
        self.driver.quit()

    def test_tc1_download_success(self):
        logger.info(f"Step 1: Navigating to {self.url}")
        self.driver.get(self.url)
        
        logger.info("Step 2: Finding the first downloadable link...")
        links = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".example a")))
        first_link = links[0]
        file_name = first_link.text
        
        logger.info(f"Action: Clicking download for file: {file_name}")
        first_link.click()
        
        logger.info("Step 3: Polling filesystem for the file...")
        file_path = os.path.join(self.download_dir, file_name)
        
        found = False
        for _ in range(20): # Wait max 10 seconds
            if os.path.exists(file_path):
                found = True
                break
            time.sleep(0.5)
            
        self.assertTrue(found, f"Result Failed: File {file_name} was not found in {self.download_dir}")
        logger.info(f"Result Success: File {file_name} downloaded correctly.")