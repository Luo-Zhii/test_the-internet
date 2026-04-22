import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestContextMenu(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://the-internet.herokuapp.com/context_menu'

    def tearDown(self):
        self.driver.quit()

    def test_tc1_context_menu_success(self):
        """TC1: Right-click the hot spot correctly triggers the JS alert."""
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        
        # Perform right click
        actions = ActionChains(self.driver)
        actions.context_click(hot_spot).perform()
        
        # Verify alert presence and text
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        
        self.assertEqual(alert.text, "You selected a context menu", "Alert text does not match expected output.")
        alert.accept()

    def test_tc2_left_click_ignores_menu(self):
        """TC2: Verify that standard left click does not trigger the context menu alert."""
        self.driver.get(self.url)
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        
        # Perform standard left click
        actions = ActionChains(self.driver)
        actions.click(hot_spot).perform()
        
        # Wait up to 2 seconds to fail fast ensuring NO alert displays
        import time 
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.alert_is_present())
            self.fail("Alert incorrectly triggered on left-click.")
        except:
            self.assertTrue(True, "Successfully confirmed alert does not appear on left click.")

if __name__ == "__main__":
    unittest.main()
