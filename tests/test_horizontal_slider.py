import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestHorizontalSlider(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_slider_with_keyboard(self):
        self.driver.get("https://the-internet.herokuapp.com/horizontal_slider")
        
        slider = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='range']")))
        
        # Move right twice (usually increments by 0.5)
        slider.send_keys(Keys.ARROW_RIGHT)
        slider.send_keys(Keys.ARROW_RIGHT)
        
        value = self.driver.find_element(By.ID, "range").text
        self.assertEqual(value, "1")

    def test_slider_with_actions(self):
        self.driver.get("https://the-internet.herokuapp.com/horizontal_slider")
        
        slider = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='range']")))
        
        # Move using mouse offset
        actions = ActionChains(self.driver)
        actions.click_and_hold(slider).move_by_offset(20, 0).release().perform()
        
        value = self.driver.find_element(By.ID, "range").text
        # Value will depend on screen resolution/offset, but we verify it's no longer "0"
        self.assertNotEqual(value, "0")

if __name__ == "__main__":
    unittest.main()
