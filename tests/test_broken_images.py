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
        self.url = "https://the-internet.herokuapp.com/broken_images"

    def tearDown(self):
        self.driver.quit()

    def helper_evaluate_image(self, img_element):
        """Helper rule to determine if an individual image element is broken via HTTP request."""
        src = img_element.get_attribute('src')
        if not src:
            return False # Missing source counts as broken or missing
        try:
            response = requests.get(src, stream=True, timeout=5)
            # A valid image must return status 200
            return response.status_code == 200
        except:
            return False

    def test_tc1_verify_total_images_on_page(self):
        """TC1: Verify correct total count of images on page to ensure script doesn't silently pass if DOM changes."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        images = self.driver.find_elements(By.TAG_NAME, "img")
        
        # Herokuapp broken images page has 4 images including avatar
        self.assertTrue(len(images) >= 3, "There should be at least 3 images present on the page layout.")

    def test_tc2_identify_broken_images(self):
        """TC2: Explicitly identify images that return non-200 profiles."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        images = self.driver.find_elements(By.TAG_NAME, "img")
        
        broken_imgs = []
        for img in images:
            if not self.helper_evaluate_image(img):
                broken_imgs.append(img.get_attribute('outerHTML'))
                
        # The intent is to verify exactly *which* images or how many fail reliably
        # On Herokuapp there are 2 broken profile pics out of 4 total imgs.
        self.assertEqual(len(broken_imgs), 2, "There are exactly two broken images on the Heroku app demo.")

    def test_tc3_identify_valid_images(self):
        """TC3: Ensure the script correctly recognizes 200 OK valid images such as the footer avatar."""
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "img")))
        images = self.driver.find_elements(By.TAG_NAME, "img")
        
        valid_imgs = []
        for img in images:
            if self.helper_evaluate_image(img):
                valid_imgs.append(img.get_attribute('outerHTML'))
                
        self.assertTrue(len(valid_imgs) >= 1, "There should be at least one valid image on the page.")

if __name__ == "__main__":
    unittest.main()
