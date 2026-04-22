import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class TestIFrame(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_iframe_rich_text_editor(self):
        self.driver.get('https://the-internet.herokuapp.com/iframe')
        
        # Switch to the iframe
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
        
        # Interact with the editor body
        editor_body = self.wait.until(EC.element_to_be_clickable((By.ID, "tinymce")))
        
        # Use JS to set the content directly for stability in the test environment
        test_text = "Refactored TinyMCE Test"
        self.driver.execute_script(f"arguments[0].innerHTML = '<p>{test_text}</p>';", editor_body)
        
        # Verify text
        self.wait.until(lambda d: test_text in editor_body.text)
        self.assertEqual(editor_body.text, test_text)
        
        # Switch back to default content
        self.driver.switch_to.default_content()
        self.assertIn("An iFrame containing the TinyMCE WYSIWYG Editor", self.driver.find_element(By.TAG_NAME, "h3").text)

if __name__ == "__main__":
    unittest.main()
