import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestDynamicContent(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_dynamic_content_changes_on_refresh(self):
        self.driver.get('https://the-internet.herokuapp.com/dynamic_content')
        
        # Capture initial state of the 3 content rows
        initial_images = [img.get_attribute("src") for img in self.driver.find_elements(By.CSS_SELECTOR, "#content .large-2.columns img")]
        initial_texts = [txt.text for txt in self.driver.find_elements(By.CSS_SELECTOR, "#content .large-10.columns")]
        
        # Refresh the page
        self.driver.refresh()
        
        # Capture refreshed state
        refreshed_images = [img.get_attribute("src") for img in self.driver.find_elements(By.CSS_SELECTOR, "#content .large-2.columns img")]
        refreshed_texts = [txt.text for txt in self.driver.find_elements(By.CSS_SELECTOR, "#content .large-10.columns")]
        
        # Verify that at least one image or text has changed (Dynamic Content usually changes at least one)
        # We check if the lists are not identical
        self.assertNotEqual(initial_images, refreshed_images, "Images did not change after refresh")
        self.assertNotEqual(initial_texts, refreshed_texts, "Texts did not change after refresh")

if __name__ == "__main__":
    unittest.main()
