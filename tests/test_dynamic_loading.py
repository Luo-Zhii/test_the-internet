import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "https://the-internet.herokuapp.com/dynamic_loading"


class TestDynamicLoading(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – EP Happy Path: Hidden element (Example 1)
    # ─────────────────────────────────────────────────────────────────
    def test_hidden_element_ep_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Dynamic Loading Example 1 (hidden element).")
        self.driver.get(f"{BASE_URL}/1")

        logger.info("[INPUT]  Locating and clicking the Start button.")
        start_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )
        start_button.click()

        logger.info("[INPUT]  Waiting for the loading bar to become invisible.")
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        logger.info("[OUTPUT] Asserting that the #finish element is visible and contains 'Hello World!'.")
        finish = self.wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        self.assertTrue(finish.is_displayed(), "#finish element should be visible.")
        self.assertEqual(finish.text, "Hello World!", f"Expected 'Hello World!' but got '{finish.text}'.")
        logger.info("[OUTPUT] TC1 PASSED – Hidden element revealed successfully.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – EP Happy Path: Rendered element (Example 2)
    # ─────────────────────────────────────────────────────────────────
    def test_rendered_element_ep_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Dynamic Loading Example 2 (rendered element).")
        self.driver.get(f"{BASE_URL}/2")

        logger.info("[INPUT]  Locating and clicking the Start button.")
        start_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )
        start_button.click()

        logger.info("[INPUT]  Waiting for the loading bar to become invisible.")
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        logger.info("[OUTPUT] Asserting that the #finish element is rendered in the DOM and visible.")
        finish = self.wait.until(EC.presence_of_element_located((By.ID, "finish")))
        self.assertTrue(finish.is_displayed(), "#finish element should be rendered and visible.")
        self.assertEqual(finish.text, "Hello World!", f"Expected 'Hello World!' but got '{finish.text}'.")
        logger.info("[OUTPUT] TC2 PASSED – Rendered element is present and correct.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path / Robustness: Double-click Start
    # ─────────────────────────────────────────────────────────────────
    def test_double_click_sad_path_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Dynamic Loading Example 1 for double-click robustness test.")
        self.driver.get(f"{BASE_URL}/1")

        logger.info("[INPUT]  Locating the Start button.")
        start_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )

        logger.info("[INPUT]  Rapidly double-clicking the Start button.")
        start_button.click()
        try:
            # Attempt a second click immediately; button may disappear, so allow failure
            start_button.click()
            logger.info("[INPUT]  Second click was accepted (button still interactable).")
        except Exception as e:
            logger.info(f"[INPUT]  Second click was rejected gracefully: {type(e).__name__} – {e}")

        logger.info("[INPUT]  Waiting for the loading bar to become invisible after double-click.")
        self.wait.until(EC.invisibility_of_element_located((By.ID, "loading")))

        logger.info("[OUTPUT] Asserting that the page recovers and shows 'Hello World!'.")
        finish = self.wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        self.assertEqual(finish.text, "Hello World!", f"Expected 'Hello World!' but got '{finish.text}'.")
        logger.info("[OUTPUT] TC3 PASSED – Double-click did not crash or corrupt the loading state.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path / Negative: Wrong button selector
    # ─────────────────────────────────────────────────────────────────
    def test_missing_element_sad_path_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to Dynamic Loading Example 1.")
        self.driver.get(f"{BASE_URL}/1")

        logger.info("[INPUT]  Attempting to locate a non-existent button selector: 'button#wrong-id'.")
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#wrong-id"))
            )
            logger.info("[OUTPUT] UNEXPECTED: 'button#wrong-id' was found. Test FAILED.")
            self.fail("Expected TimeoutException was NOT thrown. The element 'button#wrong-id' should not exist.")
        except TimeoutException:
            logger.info("[OUTPUT] TC4 PASSED – TimeoutException gracefully caught. Non-existent element confirmed absent.")

    # ─────────────────────────────────────────────────────────────────
    # TC5 – BVA: 0.5-second timeout boundary on loading bar
    # ─────────────────────────────────────────────────────────────────
    def test_short_timeout_bva_tc5(self):
        logger.info("[INPUT]  TC5 – Navigating to Dynamic Loading Example 1.")
        self.driver.get(f"{BASE_URL}/1")

        logger.info("[INPUT]  Locating and clicking the Start button.")
        start_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )
        start_button.click()

        logger.info("[INPUT]  Using a BVA short timeout of 0.5s to wait for loading bar disappearance.")
        short_wait = WebDriverWait(self.driver, 0.5)
        try:
            short_wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
            logger.info("[OUTPUT] UNEXPECTED: Loading completed within 0.5s. Test FAILED.")
            self.fail("Expected TimeoutException was NOT thrown. Loading bar disappeared faster than 0.5s boundary.")
        except TimeoutException:
            logger.info("[OUTPUT] TC5 PASSED – TimeoutException gracefully caught. Loading bar persisted beyond 0.5s boundary.")


if __name__ == "__main__":
    unittest.main()
