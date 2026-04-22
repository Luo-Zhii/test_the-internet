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

    def tearDown(self):
        self.driver.quit()

    def test_context_menu_alert(self):
        self.driver.get('https://the-internet.herokuapp.com/context_menu')
        
        hot_spot = self.wait.until(EC.visibility_of_element_located((By.ID, "hot-spot")))
        
        # Right click on the hot spot
        actions = ActionChains(self.driver)
        actions.context_click(hot_spot).perform()
        
        # Handle alert
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        self.assertEqual(alert_text, "You selected a context menu")
        alert.accept()

if __name__ == "__main__":
    unittest.main()
