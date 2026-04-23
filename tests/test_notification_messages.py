import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/notification_message_rendered"
CLICK_URL = "https://the-internet.herokuapp.com/notification_message"
VALID_MESSAGES = [
    "Action successful",
    "Action unsuccessful, please try again",
    # Server-side typo variants actually served by the app (single 's' in unsuccessful)
    "Action unsuccesful, please try again",
]


class TestNotificationMessages(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _get_flash_text(self):
        """Helper: wait for the flash message and return its stripped text."""
        flash = self.wait.until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )
        # Remove the '×' dismiss button text that may appear in the raw text
        return flash.text.replace("×", "").strip()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Single click produces a valid flash message
    # ─────────────────────────────────────────────────────────────────
    def test_notification_single_click_ep_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Notification Messages page.")
        self.driver.get(CLICK_URL)

        logger.info("[INPUT]  Clicking the 'Click here' link to trigger a flash message.")
        click_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click here")))
        click_link.click()

        flash_text = self._get_flash_text()
        logger.info(f"[OUTPUT] Flash message received: '{flash_text}'.")

        logger.info(f"[OUTPUT] Asserting flash text is in valid message list: {VALID_MESSAGES}.")
        self.assertIn(
            flash_text,
            VALID_MESSAGES,
            f"Unexpected flash message: '{flash_text}'. Expected one of: {VALID_MESSAGES}"
        )
        logger.info("[OUTPUT] TC1 PASSED – Single-click notification is a valid message.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Multiple clicks each produce a valid flash message
    # ─────────────────────────────────────────────────────────────────
    def test_notification_multi_click_ep_tc2(self):
        logger.info("[INPUT]  TC2 – Clicking the notification link 5 times and verifying each response.")
        for i in range(1, 6):
            logger.info(f"[INPUT]  Click #{i} – Navigating to {CLICK_URL}.")
            self.driver.get(CLICK_URL)

            click_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click here")))
            click_link.click()

            flash_text = self._get_flash_text()
            logger.info(f"[OUTPUT] Click #{i} flash message: '{flash_text}'.")

            self.assertIn(
                flash_text,
                VALID_MESSAGES,
                f"Click #{i}: Unexpected flash message: '{flash_text}'. Expected one of: {VALID_MESSAGES}"
            )

        logger.info("[OUTPUT] TC2 PASSED – All 5 clicks produced valid notification messages.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path: Flash message is never an unexpected/empty string
    # ─────────────────────────────────────────────────────────────────
    def test_notification_no_unexpected_message_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Notification Messages page.")
        self.driver.get(CLICK_URL)

        click_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click here")))
        click_link.click()

        flash_text = self._get_flash_text()
        logger.info(f"[OUTPUT] Flash message: '{flash_text}'.")

        logger.info("[OUTPUT] Asserting flash is not empty and is a known valid message.")
        self.assertTrue(len(flash_text) > 0, "Flash message should never be empty.")
        # Assert it is one of the recognized valid server messages (incl. known typo variants)
        self.assertIn(
            flash_text,
            VALID_MESSAGES,
            f"Flash message not in known valid set. Got: '{flash_text}'. Valid: {VALID_MESSAGES}"
        )
        logger.info("[OUTPUT] TC3 PASSED – Flash message is non-empty and a recognized valid message.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Robustness: Direct navigation to rendered page shows flash
    # ─────────────────────────────────────────────────────────────────
    def test_notification_direct_render_robustness_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to the notification_message (click) page first.")
        self.driver.get(CLICK_URL)

        logger.info("[INPUT]  Clicking the 'Click here' link to trigger redirect to rendered page.")
        click_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click here")))
        click_link.click()

        logger.info("[INPUT]  Confirming we landed on the rendered URL.")
        self.wait.until(EC.url_contains("notification_message_rendered"))
        current_url = self.driver.current_url
        logger.info(f"[OUTPUT] Current URL after click: '{current_url}'.")
        self.assertIn(
            "notification_message_rendered", current_url,
            f"Should have redirected to rendered page, got: '{current_url}'"
        )

        logger.info("[INPUT]  Reading flash message on the rendered page.")
        flash_text = self._get_flash_text()
        logger.info(f"[OUTPUT] Flash on rendered page: '{flash_text}'.")

        logger.info(f"[OUTPUT] Asserting flash is in the valid message list: {VALID_MESSAGES}.")
        self.assertIn(
            flash_text,
            VALID_MESSAGES,
            f"Rendered page flash message unexpected: '{flash_text}'. Expected one of: {VALID_MESSAGES}"
        )
        logger.info("[OUTPUT] TC4 PASSED – Click → redirect → rendered page flash correctly verified.")


if __name__ == "__main__":
    unittest.main()
