import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestInfiniteScroll(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_infinite_scroll_content_loading(self):
        self.driver.get('https://the-internet.herokuapp.com/infinite_scroll')
        
        # Get initial scroll height
        initial_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Scroll down multiple times
        for i in range(5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for content to load (height to change)
            self.wait.until(lambda d: d.execute_script("return document.body.scrollHeight") > initial_height)
            initial_height = self.driver.execute_script("return document.body.scrollHeight")
        
        # Verify final height is significantly larger
        final_height = self.driver.execute_script("return document.body.scrollHeight")
        self.assertGreater(final_height, initial_height // 2) # Just a sanity check

if __name__ == "__main__":
    unittest.main()
