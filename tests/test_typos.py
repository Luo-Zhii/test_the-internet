import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

URL = "https://the-internet.herokuapp.com/typos"
CORRECT_TEXT = "won't"
TYPO_TEXT = "won,t"
MAX_REFRESHES = 10


class TestTypos(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        logger.info("[TEARDOWN] Quitting driver.")
        self.driver.quit()

    def _get_second_paragraph(self) -> str:
        """Helper: wait for the second paragraph and return its text."""
        paragraphs = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example p"))
        )
        text = paragraphs[1].text.strip() if len(paragraphs) > 1 else ""
        logger.info(f"[INPUT]  Second paragraph text: '{text}'.")
        return text

    # ─────────────────────────────────────────────────────────────────
    # TC1 – Happy Path: Refresh until the correct text appears
    # ─────────────────────────────────────────────────────────────────
    def test_typos_refresh_until_correct_tc1(self):
        logger.info(f"[INPUT]  TC1 – Refreshing up to {MAX_REFRESHES}× until correct text '{CORRECT_TEXT}' appears.")
        found_correct = False

        for attempt in range(1, MAX_REFRESHES + 1):
            logger.info(f"[INPUT]  Attempt {attempt}: Navigating to Typos page.")
            self.driver.get(URL)
            text = self._get_second_paragraph()

            if CORRECT_TEXT in text:
                logger.info(f"[OUTPUT] Correct text found on attempt {attempt}: '{text}'.")
                found_correct = True
                break
            else:
                logger.info(f"[OUTPUT] Incorrect text on attempt {attempt}: '{text}'. Refreshing.")

        self.assertTrue(
            found_correct,
            f"Correct text '{CORRECT_TEXT}' was not found in {MAX_REFRESHES} refreshes."
        )
        logger.info("[OUTPUT] TC1 PASSED – Correct text eventually appeared within allowed refreshes.")

    # ─────────────────────────────────────────────────────────────────
    # TC2 – Sad Path / A/B Bug Detection: Catch & log the 'won,t' typo
    # ─────────────────────────────────────────────────────────────────
    def test_typos_detect_known_typo_tc2(self):
        logger.info("[INPUT]  TC2 – Loading Typos page once and inspecting for the known 'won,t' typo.")
        found_typo = False
        found_correct = False

        for attempt in range(1, MAX_REFRESHES + 1):
            self.driver.get(URL)
            text = self._get_second_paragraph()

            if TYPO_TEXT in text:
                found_typo = True
                logger.info(
                    f"[OUTPUT] ⚠ A/B BUG DETECTED on attempt {attempt}: "
                    f"Typo variant served – text contains '{TYPO_TEXT}'. Full text: '{text}'"
                )
                break
            elif CORRECT_TEXT in text:
                found_correct = True
                logger.info(f"[OUTPUT] Correct variant on attempt {attempt}: '{text}'.")
                break

        if found_typo:
            logger.info("[OUTPUT] TC2 INFO – Typo variant was observed and logged as an A/B defect.")
        elif found_correct:
            logger.info("[OUTPUT] TC2 INFO – Only correct variant observed in this run (typo is random).")
        else:
            self.fail(f"Neither expected text nor known typo found in {MAX_REFRESHES} attempts.")

        # TC2 passes regardless of which variant appeared — the goal is detection + logging
        logger.info("[OUTPUT] TC2 PASSED – Page text classified and logged correctly.")

    # ─────────────────────────────────────────────────────────────────
    # TC3 – Robustness: Assert page always has two paragraphs (structure)
    # ─────────────────────────────────────────────────────────────────
    def test_typos_page_structure_robustness_tc3(self):
        logger.info("[INPUT]  TC3 – Navigating to Typos page to verify DOM structure.")
        self.driver.get(URL)

        logger.info("[INPUT]  Waiting for all paragraphs in .example to load.")
        paragraphs = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example p"))
        )
        logger.info(f"[OUTPUT] Number of <p> elements found: {len(paragraphs)}.")

        logger.info("[OUTPUT] Asserting page always has exactly 2 paragraphs regardless of A/B variant.")
        self.assertEqual(
            len(paragraphs), 2,
            f"Expected 2 paragraphs in .example div, but found {len(paragraphs)}."
        )

        second_text = paragraphs[1].text.strip()
        logger.info(f"[OUTPUT] Second paragraph content: '{second_text}'.")
        logger.info("[OUTPUT] Asserting second paragraph is one of the two known A/B variants.")
        # Server randomly delivers correct or typo variant of this sentence.
        known_variants = [
            "Sometimes you'll see a typo, other times you won't.",
            "Sometimes you'll see a typo, other times you won,t.",
        ]
        self.assertIn(
            second_text,
            known_variants,
            f"Unexpected second paragraph: '{second_text}'. Expected one of: {known_variants}"
        )
        logger.info("[OUTPUT] TC3 PASSED – Page structure is consistent across A/B variants.")


if __name__ == "__main__":
    unittest.main()
