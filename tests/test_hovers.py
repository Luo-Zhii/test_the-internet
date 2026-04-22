import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestHovers(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_hover_details_visibility(self):
        self.driver.get('https://the-internet.herokuapp.com/hovers')
        
        # Locate the first figure
        figure = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "figure")))
        
        # Perform hover
        actions = ActionChains(self.driver)
        actions.move_to_element(figure).perform()
        
        # Verify caption details appear
        caption = figure.find_element(By.CLASS_NAME, "figcaption")
        self.wait.until(lambda d: caption.is_displayed())
        
        header = caption.find_element(By.TAG_NAME, "h5")
        self.assertEqual(header.text, "name: user1")
        
        link = caption.find_element(By.LINK_TEXT, "View profile")
        self.assertTrue(link.is_displayed())

if __name__ == "__main__":
    unittest.main()
