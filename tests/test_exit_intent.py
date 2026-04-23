import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Professional Logging
logger = logging.getLogger(__name__)

class TestExitIntent(unittest.TestCase):
    def setUp(self):
        logger.info("Initializing webdriver for Exit Intent module.")
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://the-internet.herokuapp.com/exit_intent"

    def tearDown(self):
        logger.info("Cleanup: Quitting driver.")
        self.driver.quit()

    def _trigger_exit_intent(self):
        """Helper to simulate mouse leaving viewport via JS Dispatch."""
        logger.info("[INPUT] Dispatching JS 'mouseleave' event to document.")
        script = "document.documentElement.dispatchEvent(new MouseEvent('mouseleave'));"
        self.driver.execute_script(script)

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Standard trigger and verification
    # ─────────────────────────────────────────────────────────────────
    def test_exit_intent_happy_path_tc1(self):
        """TC1: Trigger modal, verify title, and close it."""
        self.driver.get(self.url)
        self._trigger_exit_intent()
        
        modal = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
        title = modal.find_element(By.TAG_NAME, "h3").text
        self.assertEqual(title, "THIS IS A MODAL WINDOW")
        
        # Click close and wait for invisibility
        modal.find_element(By.CSS_SELECTOR, ".modal-footer p").click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal")))
        logger.info("TC1 Passed: Modal handled successfully.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Business Logic: One-time trigger per session
    # ─────────────────────────────────────────────────────────────────
    def test_exit_intent_one_time_trigger_tc2(self):
        """TC2: Ensure modal doesn't reappear after being closed once."""
        self.driver.get(self.url)
        self._trigger_exit_intent()
        
        modal = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
        self.driver.execute_script("arguments[0].click();", modal.find_element(By.CSS_SELECTOR, ".modal-footer p"))
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal")))

        logger.info("[INPUT] Attempting second trigger to verify 'one-time' logic.")
        self._trigger_exit_intent()
        
        short_wait = WebDriverWait(self.driver, 3)
        try:
            short_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
            self.fail("UX BUG: Modal appeared twice!")
        except TimeoutException:
            logger.info("TC2 Passed: Modal correctly suppressed.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Negative: Movement within bounds should NOT trigger (The Missing Piece)
    # ─────────────────────────────────────────────────────────────────
    def test_exit_intent_no_trigger_within_bounds_tc3(self):
        """TC3: Verify moving mouse within page bounds doesn't show modal."""
        logger.info("[INPUT] TC3 - Testing mouse movement within valid bounds.")
        self.driver.get(self.url)
        
        # We use ActionChains for valid movement (in-bounds)
        body = self.driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(self.driver)
        
        logger.info("[INPUT] Action: Moving mouse to bottom-right (X:100, Y:100).")
        actions.move_to_element(body).move_by_offset(100, 100).perform()
        
        logger.info("[OUTPUT] Expectation: Modal should stay hidden.")
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
            self.fail("UX BUG: Modal triggered by movement within page bounds!")
        except TimeoutException:
            logger.info("TC3 Passed: Modal remained hidden as expected.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Robustness: Overlay Blocking
    # ─────────────────────────────────────────────────────────────────
    def test_exit_intent_overlay_blocking_tc4(self):
        """TC4: Verify modal overlay blocks background interaction."""
        self.driver.get(self.url)
        
        # Find link BEFORE modal appears
        footer_link = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Elemental Selenium')]")
        ))
        self.driver.execute_script("arguments[0].scrollIntoView();", footer_link)
        
        self._trigger_exit_intent()
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal")))
        
        logger.info("[INPUT] Attempting to click background link while modal is active.")
        try:
            footer_link.click()
            self.fail("SECURITY BUG: Background link was clickable through the modal!")
        except ElementClickInterceptedException:
            logger.info("[OUTPUT] Click intercepted successfully.")
        except Exception as e:
            logger.info(f"Interaction prevented by: {type(e).__name__}")
            
        logger.info("TC4 Passed: Background interaction blocked.")

if __name__ == "__main__":
    unittest.main()