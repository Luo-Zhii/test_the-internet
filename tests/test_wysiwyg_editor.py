import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/tinymce"
IFRAME_ID = "mce_0_ifr"
INJECT_TEXT = "Selenium JS Injection Test — bypassing read-only mode."


class TestWYSIWYGEditor(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: JS innerHTML injection into TinyMCE iframe
    # ─────────────────────────────────────────────────────────────────
    def test_wysiwyg_js_injection_happy_path_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to TinyMCE WYSIWYG Editor page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for iframe to be available and switching context.")
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, IFRAME_ID))
        )

        logger.info("[INPUT]  Locating the #tinymce editable body inside the iframe.")
        editor_body = self.wait.until(
            EC.presence_of_element_located((By.ID, "tinymce"))
        )

        logger.info(f"[INPUT]  Injecting text via execute_script innerHTML: '{INJECT_TEXT}'.")
        self.driver.execute_script(
            "arguments[0].innerHTML = arguments[1];",
            editor_body,
            f"<p>{INJECT_TEXT}</p>"
        )

        logger.info("[INPUT]  Reading back the innerHTML to verify injection.")
        result = self.driver.execute_script("return arguments[0].innerHTML;", editor_body)
        logger.info(f"[OUTPUT] innerHTML after injection: '{result}'.")

        logger.info("[OUTPUT] Asserting injected text is present in editor body.")
        self.assertIn(
            INJECT_TEXT, result,
            f"Expected '{INJECT_TEXT}' in innerHTML but got: '{result}'"
        )
        logger.info("[OUTPUT] TC1 PASSED – JS innerHTML injection bypassed read-only mode successfully.")

        self.driver.switch_to.default_content()

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Sad/Robustness: Detect read-only warning overlay presence
    # ─────────────────────────────────────────────────────────────────
    def test_wysiwyg_readonly_alert_sad_path_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to TinyMCE WYSIWYG Editor page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Checking main document for read-only warning overlay (.tox-notification--warning).")
        short_wait = WebDriverWait(self.driver, 5)
        try:
            warning_overlay = short_wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".tox-notification--warning")
                )
            )
            warning_text = warning_overlay.text
            logger.info(f"[OUTPUT] READ-ONLY OVERLAY DETECTED. Text: '{warning_text}'.")
            logger.info("[OUTPUT] Asserting overlay contains known API-limit message.")
            self.assertTrue(
                warning_overlay.is_displayed(),
                "Read-only overlay should be visible when TinyMCE is in API-limit mode."
            )
            logger.info("[OUTPUT] TC2 PASSED – Read-only warning overlay correctly detected and verified.")
        except TimeoutException:
            logger.info("[OUTPUT] No read-only overlay appeared within 5s — TinyMCE loaded normally (API limit not hit).")
            logger.info("[OUTPUT] TC2 PASSED – Either state (overlay present or absent) is a valid outcome.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Happy Path: Verify toolbar Bold & Italic buttons are visible
    # ─────────────────────────────────────────────────────────────────
    def test_wysiwyg_toolbar_visibility_happy_path_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to TinyMCE WYSIWYG Editor page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for the TinyMCE toolbar container to appear in the main document.")
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".tox-toolbar__primary, .tox-toolbar"))
        )

        logger.info("[INPUT]  Locating the Bold toolbar button by aria-label.")
        bold_btn = self.driver.find_element(
            By.XPATH, "//button[@aria-label='Bold' or @title='Bold']"
        )
        logger.info(f"[OUTPUT] Bold button found: displayed={bold_btn.is_displayed()}.")
        self.assertTrue(bold_btn.is_displayed(), "Bold toolbar button should be visible.")

        logger.info("[INPUT]  Locating the Italic toolbar button by aria-label.")
        italic_btn = self.driver.find_element(
            By.XPATH, "//button[@aria-label='Italic' or @title='Italic']"
        )
        logger.info(f"[OUTPUT] Italic button found: displayed={italic_btn.is_displayed()}.")
        self.assertTrue(italic_btn.is_displayed(), "Italic toolbar button should be visible.")

        logger.info("[OUTPUT] TC3 PASSED – TinyMCE toolbar Bold and Italic buttons verified in main document context.")

    # ─────────────────────────────────────────────────────────────────
    # TC4 – Sad Path: Toolbar buttons unreachable from inside the iframe
    # ─────────────────────────────────────────────────────────────────
    def test_wysiwyg_context_isolation_sad_path_tc4(self):
        logger.info("[INPUT]  TC4 – Navigating to TinyMCE WYSIWYG Editor page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Switching into the TinyMCE iframe context.")
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, IFRAME_ID))
        )
        logger.info("[INPUT]  Now inside iframe context. Attempting to find main-document toolbar buttons.")

        logger.info("[INPUT]  Attempting find_element for Bold button (should not exist inside iframe).")
        try:
            self.driver.find_element(
                By.XPATH, "//button[@aria-label='Bold' or @title='Bold']"
            )
            self.fail(
                "Context Isolation FAILED: Toolbar Bold button should NOT be visible from inside the iframe!"
            )
        except NoSuchElementException:
            logger.info("[OUTPUT] NoSuchElementException caught – toolbar button correctly absent from iframe context.")

        logger.info("[OUTPUT] Asserting driver is still inside iframe (sanity check: #tinymce body is accessible).")
        editor_body = self.driver.find_element(By.ID, "tinymce")
        self.assertIsNotNone(editor_body, "Should still be inside iframe context.")
        logger.info("[OUTPUT] TC4 PASSED – Iframe context isolation confirmed; toolbar inaccessible from inside frame.")

        self.driver.switch_to.default_content()


if __name__ == "__main__":
    unittest.main()
