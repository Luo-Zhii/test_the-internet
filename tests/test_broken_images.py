import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestBrokenImages(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_broken_images(self):
        self.driver.get("https://the-internet.herokuapp.com/broken_images")
        
        # Wait for images to be present
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        image_list = self.driver.find_elements(By.TAG_NAME, "img")
        
        broken_images = []
        for img in image_list:
            src = img.get_attribute('src')
            if not src:
                continue
                
            try:
                response = requests.get(src, stream=True, timeout=5)
                if response.status_code != 200:
                    broken_images.append(img.get_attribute('outerHTML'))
            except Exception as e:
                broken_images.append(f"{img.get_attribute('outerHTML')} (Error: {str(e)})")
        
        # Verify no images are broken
        # Note: The herokuapp page intentionally has broken images.
        # This test will document them if they exist.
        self.assertEqual(len(broken_images), 2, f"Found {len(broken_images)} broken images: {broken_images}")

if __name__ == "__main__":
    unittest.main()
