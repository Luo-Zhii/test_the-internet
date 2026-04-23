import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/shadowdom"


class TestShadowDOM(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _get_shadow_text_via_js(self, host_css: str, inner_css: str) -> str:
        """Helper: pierce shadow root via JavaScript and return inner element text."""
        script = f"""
            const host = document.querySelector('{host_css}');
            if (!host || !host.shadowRoot) return null;
            const inner = host.shadowRoot.querySelector('{inner_css}');
            return inner ? inner.textContent.trim() : null;
        """
        return self.driver.execute_script(script)

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Access shadow host via Selenium 4 shadow_root
    # ─────────────────────────────────────────────────────────────────
    def test_shadow_dom_access_via_shadow_root_tc1(self):
        logger.info("[INPUT]  TC1 – Navigating to Shadow DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for first shadow host element 'my-paragraph' to be present.")
        shadow_host = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "my-paragraph"))
        )
        logger.info("[INPUT]  Accessing shadow root via Selenium 4 .shadow_root property.")
        shadow_root = shadow_host.shadow_root

        logger.info("[INPUT]  Finding <p> element inside the shadow root.")
        inner_p = shadow_root.find_element(By.CSS_SELECTOR, "p")
        text = inner_p.text
        logger.info(f"[OUTPUT] Shadow DOM inner <p> text: '{text}'.")

        logger.info("[OUTPUT] Asserting shadow DOM content is accessible and non-empty.")
        self.assertTrue(len(text) > 0, "Shadow DOM inner element text should not be empty.")
        logger.info(f"[OUTPUT] Verified shadow content is non-empty: '{text}'.")
        logger.info("[OUTPUT] TC1 PASSED – Shadow DOM accessed via .shadow_root correctly.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Happy Path: Access shadow DOM content via JavaScript injection
    # ─────────────────────────────────────────────────────────────────
    def test_shadow_dom_access_via_js_tc2(self):
        logger.info("[INPUT]  TC2 – Navigating to Shadow DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for 'my-paragraph' shadow host element to confirm page load.")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "my-paragraph")))

        logger.info("[INPUT]  Piercing shadow root of 'my-paragraph' via JavaScript.")
        text = self._get_shadow_text_via_js("my-paragraph", "p")
        logger.info(f"[OUTPUT] JS-extracted shadow text: '{text}'.")

        logger.info("[OUTPUT] Asserting JS could pierce the shadow boundary and return content.")
        self.assertIsNotNone(text, "JS should be able to pierce shadow root and return text.")
        self.assertTrue(len(text) > 0, "Shadow DOM text extracted via JS should not be empty.")
        logger.info("[OUTPUT] TC2 PASSED – Shadow DOM content accessed via JS executeScript.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Sad Path: Standard XPath from global document cannot pierce shadow boundary
    # ─────────────────────────────────────────────────────────────────
    def test_shadow_dom_xpath_cannot_pierce_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Shadow DOM page.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for 'my-paragraph' shadow host to confirm page load.")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "my-paragraph")))

        logger.info("[INPUT]  Attempting to find shadow-DOM <p> via standard XPath from document root (2s short-wait).")
        # XPath cannot cross shadow boundaries — this element lives inside a shadow root
        short_wait = WebDriverWait(self.driver, 2)
        try:
            short_wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//my-paragraph//p[contains(text(),'shadow')]")
                )
            )
            self.fail("Standard XPath should NOT be able to pierce the shadow DOM boundary.")
        except TimeoutException:
            logger.info("[OUTPUT] TimeoutException caught – standard XPath correctly blocked by shadow boundary.")
        except NoSuchElementException:
            logger.info("[OUTPUT] NoSuchElementException caught – standard XPath correctly blocked by shadow boundary.")

        logger.info("[OUTPUT] TC3 PASSED – Shadow DOM correctly encapsulates content from global XPath queries.")


if __name__ == "__main__":
    unittest.main()
