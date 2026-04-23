# Master Test Case Specification
### Project: The Internet – Selenium Automation Suite
**Prepared by:** QA Automation Team  
**Date:** 2026-04-22  
**Total Test Files:** 27 | **Total Test Cases:** 77+

---

## 1. Executive Summary

This document is the single-source-of-truth specification for the full Selenium end-to-end automation suite targeting [The Internet (Herokuapp)](https://the-internet.herokuapp.com). The framework is built on:

| Strategic Pillar | Implementation Detail |
| :--- | :--- |
| **Framework** | Python `unittest.TestCase` with `webdriver_manager` for automated driver lifecycle management |
| **Wait Strategy** | Exclusively **Explicit Waits** (`WebDriverWait` + `expected_conditions`). `time.sleep()` is **forbidden**. |
| **Negative Testing** | ISTQB Black-Box techniques: Boundary Value Analysis, Error Guessing, and Security Injection (SQLi/XSS) |
| **Security Coverage** | XSS payloads (`<script>alert('XSS')</script>`), SQL Injection (`' OR 1=1 --`), and special-character fuzzing |
| **Race Condition Handling** | `staleness_of` checks on DOM elements during page reloads to prevent flaky assertions |
| **Geolocation Mocking** | Chrome DevTools Protocol (CDP) via `execute_cdp_cmd` to override OS-level prompts with deterministic coordinates |
| **HTML5 Drag & Drop** | JavaScript injection (`execute_script`) to bypass WebDriver's native HTML5 drag-and-drop limitations |
| **DRY Architecture** | Internal `helper_*` methods inside each test class to centralize repetitive actions |
| **Observability** | All negative test paths emit `print()` traces (Action / Expected / Actual) for deterministic CI log review |

---

## Module: A/B Testing

> **File:** `test_ab_testing.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_AB_01 | `test_ab_testing_header_variation_tc1` – Happy Path: The h3 header must match one of the two known A/B variants to prevent flaky assertions. | Navigate to `/abtest` → `EC.visibility_of_element_located((By.TAG_NAME, "h3"))` → read `h3.text` | `h3.text` **is in** `["A/B Test Control", "A/B Test Variation 1"]` | High |
| TC_AB_02 | `test_ab_testing_paragraph_presence_tc2` – UI Check: The informational paragraph below the header must always be present regardless of which A/B variant is served. | Navigate to `/abtest` → locate `<p>` element containing *"Also known as split testing"* | Paragraph is present and `is_displayed()` = **True** | Medium |
| TC_AB_03 | `test_ab_testing_optout_cookie_tc3` – Robustness: Adding the A/B opt-out cookie before a page refresh must not break the page — the header should still load. | Navigate to `/abtest` → `driver.add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})` → `driver.refresh()` → wait for `h3` | `h3` element is present and its text is in the known variant list | Medium |

---

## Feature: Add / Remove Elements

> **File:** `test_add_remove_elements.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_ARE_01 | Add a single element and verify it appears in the DOM | Click "Add Element" once | Exactly **1** Delete button visible | High |
| TC_ARE_02 | Add then immediately remove a single element | Click Add → Click Delete | DOM returns to **0** Delete buttons; staleness confirmed | High |
| TC_ARE_03 | Add multiple elements in rapid succession | Click "Add Element" **5 times** | Exactly **5** Delete buttons present | Medium |
| TC_ARE_04 | Remove all elements one-by-one (empty-state boundary) | Add 3 → Delete each with `staleness_of` confirmation | **0** Delete buttons remain; DOM fully clean | High |

---

## Feature: Basic Authentication

> **File:** `test_basic_auth.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_BA_01 | HTTP Basic Auth via URL-embedded credentials | URL: `https://admin:admin@...` | Page displays: *"Congratulations! You must have the proper credentials."* | CRITICAL |

---

## Feature: Broken Images

> **File:** `test_broken_images.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_BI_01 | Verify the total number of images rendered on page | Locate all `<img>` tags | At least **3** images present | Medium |
| TC_BI_02 | Identify broken images via HTTP response probing | HTTP GET each `src`; check status code | Exactly **2** images return non-200 (broken) | High |
| TC_BI_03 | Confirm at least one valid (200 OK) image exists | HTTP GET each `src`; filter 200 responses | At least **1** valid image confirmed | Medium |

---

## Feature: Checkboxes

> **File:** `test_checkbox.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_CB_01 | Validate default checked/unchecked state on load | Navigate to page; read `is_selected()` | CB1 = **unchecked**, CB2 = **checked** | High |
| TC_CB_02 | Check the initially unchecked checkbox | Click Checkbox 1 if unchecked | CB1 transitions to **checked** state | Medium |
| TC_CB_03 | Uncheck the initially checked checkbox | Click Checkbox 2 if checked | CB2 transitions to **unchecked** state | Medium |
| TC_CB_04 | Stress toggle both checkboxes through multiple state flips | Click CB1 twice; Click CB2 twice | Final states revert to original (CB1=unchecked, CB2=checked) | Medium |

---

## Feature: Challenging DOM

> **File:** `test_challenging_dom.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_CD_01 | TC1_Dynamic_Buttons: Locate the Red button without using ID. Click and assert. | Locate button using relative XPath or CSS `.button.alert` | Click successful; test asserts button remains or page reloads | High |
| TC_CD_02 | TC2_Table_EP_Mid: (Equivalence Partitioning) Extract and verify data from Row 5. | Wait for and locate `//table/tbody/tr[5]` | Data extracted and validated against Row 5 expected values | Medium |
| TC_CD_03 | TC3_Table_BVA_Min: (Boundary Value Analysis) Extract and verify data from Row 1. | Wait for and locate `//table/tbody/tr[1]` | Data extracted and validated against Boundary Min (first row) | High |
| TC_CD_04 | TC4_Table_BVA_Max: (Boundary Value Analysis) Extract and verify data from Row 10. | Wait for and locate `//table/tbody/tr[10]` | Data extracted and validated against Boundary Max (last row) | High |
| TC_CD_05 | TC5_Table_Negative_OutOfBounds: Attempt to locate Row 11. | `try-except` block locating Row 11 with a 2-second timeout | TimeoutException/NoSuchElementException gracefully caught | High |
| TC_CD_06 | TC6_Canvas_Verification: Verify the presence of the Canvas element. | Locate CSS selector `canvas#canvas` or `canvas` | Canvas element is confirmed present on the page | Medium |
| **TC_CD_07** | **Table Action Links (Edit/Delete)** | Locate 'edit'/'delete' links in Row 3 using relative XPath. Click them. | URL correctly appends `#edit` or `#delete` fragments. | Medium |

---

## Module: Dynamic Loading

> **File:** `test_dynamic_loading.py`

| Test Case ID | Method Name | Technique | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC_DL_01 | `test_hidden_element_ep_tc1` | EP – Happy Path | Click Start on Example 1 (hidden element). Wait for loading bar to disappear, then assert 'Hello World!' is visible. | Navigate to `/dynamic_loading/1` → Click `#start button` → `EC.invisibility_of_element_located((By.ID, "loading"))` | `#finish` element is visible; text = **"Hello World!"** | High |
| TC_DL_02 | `test_rendered_element_ep_tc2` | EP – Happy Path | Click Start on Example 2 (element rendered after load). Wait for loading bar to disappear, assert 'Hello World!' is rendered and visible. | Navigate to `/dynamic_loading/2` → Click `#start button` → `EC.invisibility_of_element_located((By.ID, "loading"))` | `#finish` element is rendered in DOM and visible; text = **"Hello World!"** | High |
| TC_DL_03 | `test_double_click_sad_path_tc3` | Sad Path – Robustness | Rapidly double-click the Start button to test duplicate trigger state. Assert the final result is still correct. | Navigate to `/dynamic_loading/1` → Double-click `#start button` in rapid succession → Wait for loading to finish | `#finish` element eventually shows **"Hello World!"** without crash or hang | Medium |
| TC_DL_04 | `test_missing_element_sad_path_tc4` | Sad Path – Negative | Attempt to locate a non-existent Start button using wrong selector `button#wrong-id`. Assert `TimeoutException` is gracefully caught. | Navigate to `/dynamic_loading/1` → `try-except` with `self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#wrong-id")))` | `TimeoutException` is raised and caught; `self.fail()` called if exception is NOT thrown | High |
| TC_DL_05 | `test_short_timeout_bva_tc5` | BVA – Short Timeout Boundary | Click Start, then wait for the loading bar to disappear using an unrealistically short 0.5s timeout. Assert `TimeoutException` is caught. | Navigate to `/dynamic_loading/1` → Click `#start button` → `WebDriverWait(self.driver, 0.5).until(EC.invisibility_of_element_located((By.ID, "loading")))` | `TimeoutException` is raised and caught; `self.fail()` called if exception is NOT thrown | High |

---

## Feature: Context Menu

> **File:** `test_context_menu.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_CM_01 | Right-click the hotspot to trigger JS alert | `ActionChains.context_click()` on `#hot-spot` | Alert appears with text: *"You selected a context menu"* | High |
| TC_CM_02 | Negative: Verify left-click does NOT trigger the alert | `ActionChains.click()` on `#hot-spot` | **No alert** appears within 2-second fast-fail window | Medium |

---

## Module: Digest Authentication

> **File:** `test_digest_auth.py`
> **Note:** Selenium cannot interact with native HTTP 401 Auth dialogs. Credentials are bypassed by embedding them in the URL: `https://{user}:{pass}@the-internet.herokuapp.com/digest_auth`. Special characters in credentials MUST be percent-encoded using `urllib.parse.quote(credential, safe="")`.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DA_01 | `test_digest_auth_happy_path_tc1` – Happy Path: Navigate with valid credentials. Assert the success message is visible. | URL: `https://admin:admin@.../digest_auth` → `EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Congratulations')]"))` | `<p>` is visible; text **contains** *"Congratulations"* | CRITICAL |
| TC_DA_02 | `test_digest_auth_invalid_creds_tc2` – Negative: Navigate with wrong password. Assert success message is absent via `TimeoutException`. | URL: `https://admin:wrong@.../digest_auth` → 2s `try-except TimeoutException` for success `<p>` → `assertNotIn` on `body.text` | `TimeoutException` caught; success text confirmed absent in body | High |
| TC_DA_03 | `test_digest_auth_unauthorized_tc3` – Security: Navigate to the endpoint with NO credentials at all. Assert the page denies access. | URL: `https://the-internet.herokuapp.com/digest_auth` (no `user:pass`) → 2s `try-except TimeoutException` → read `body.text` | `TimeoutException` caught; success text absent; body may show *"Not authorized"* | High |
| TC_DA_04 | `test_digest_auth_special_chars_tc4` – Robustness: Use `urllib.parse.quote()` to encode a password with special chars (`admin@123`) before embedding in URL. Assert the URL is correctly constructed (encoding is verified) and the page responds. | `urllib.parse.quote("admin@123", safe="")` → verify `%40` in result → navigate → assert success absent (Heroku rejects this password, but URL construction is validated) | `assertIn("%40", encoded_pass)` passes; site correctly rejects invalid creds | Medium |

---


## Feature: Disappearing Elements

> **File:** `test_disappearing_elements.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DE_01 | Verify permanent navigation links always render | Check for Home, About, Contact, Portfolio via `LINK_TEXT` | All 4 links are displayed | High |
| TC_DE_02 | Verify randomly disappearing "Gallery" link appears within 5 refreshes | Refresh up to 5× until Gallery link visible; click it | Gallery link eventually appears; clicking leads to expected 404 page | Medium |

---

## Feature: Drag and Drop

> **File:** `test_drag_and_drop.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DD_01 | Drag Block A onto Block B and verify swap | JS-injected `simulateHTML5DragAndDrop(colA → colB)` | Column A shows **"B"**, Column B shows **"A"** | High |
| TC_DD_02 | Double drag to revert blocks to original positions | JS drag A→B, then B→A | Columns revert: A shows **"A"**, B shows **"B"** | High |

---

## Feature: Dropdown

> **File:** `test_dropdown.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DD_01 | Validate default placeholder state | Read `first_selected_option` on load | Text = *"Please select an option"*; option is **disabled** | High |
| TC_DD_02 | Select Option 1 by index | `select_by_index(1)` | Selected option text = **"Option 1"** | Medium |
| TC_DD_03 | Select Option 2 by visible text | `select_by_visible_text("Option 2")` | Selected option text = **"Option 2"** | Medium |
| TC_DD_04 | Switch between options to confirm override | `select_by_value("1")` then `select_by_value("2")` | Selection correctly overrides from Option 1 → Option 2 | Medium |

---

## Feature: Dynamic Content

> **File:** `test_dynamic_content.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DC_01 | Verify 3 rows of images and text always render | Navigate to base URL; count rows | Exactly **3 images** and **3 text blocks** present | High |
| TC_DC_02 | Confirm content randomizes on page refresh | Refresh up to 3×; compare `src`/text captures | At least one image **or** text block changes across refreshes | Medium |
| TC_DC_03 | Verify `?with_content=static` locks first two rows | Load static URL; refresh; compare first 2 rows | First 2 image+text pairs remain **identical**; 3rd row is free to change | High |

---

## Feature: Dynamic Controls

> **File:** `test_dynamic_controls.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_DY_01 | Remove checkbox from DOM via button click | Click "Remove"; wait `staleness_of` | `#message` = *"It's gone!"*; `#checkbox` count = 0 | High |
| TC_DY_02 | Re-add checkbox after removal | Remove → then click "Add" | `#message` = *"It's back!"*; `#checkbox` is visible | High |
| TC_DY_03 | Enable a disabled input field | Click "Enable"; wait `element_to_be_clickable` | `#message` = *"It's enabled!"*; `input.is_enabled()` = True | High |
| TC_DY_04 | Disable a re-enabled input field | Enable → click "Disable"; wait `lambda is_enabled == False` | `#message` = *"It's disabled!"*; `input.is_enabled()` = False | High |

---

## Feature: Entry Ad (Modal)

> **File:** `test_entry_ad.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_EA_01 | Close modal on initial appearance | Delete cookies → refresh → wait for modal → click close | Modal becomes **invisible** (`invisibility_of_element`) | High |
| TC_EA_02 | Modal does NOT reappear after being closed (cookie retention) | Close modal → refresh with cookies intact; fast-fail wait (3s) | Modal remains **hidden** on subsequent visit | Medium |
| TC_EA_03 | Modal reappears after cookies are fully cleared | Close modal → delete all cookies → refresh | Modal is **visible again** (session memory reset) | Medium |

---
## Module: Exit Intent

> **File:** `tests/test_exit_intent.py`
> **Note:** The modal only triggers when the mouse leaves the browser viewport (top bound).

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **TC_EI_01** | **Happy Path Modal Display** | Navigate to `/exit_intent` -> Move mouse out of viewport (top). | Modal becomes visible; Title = "THIS IS A MODAL WINDOW". | High |
| **TC_EI_02** | **One-time Trigger Logic** | Trigger and close modal once -> Attempt to trigger again. | Modal DOES NOT reappear; logic only allows one trigger per session. | High |
| **TC_EI_03** | **No Trigger Within Bounds** | Move mouse to the right/bottom of the viewport. | Modal remains hidden; only top-exit triggers intent. | Medium |
| **TC_EI_04** | **Overlay Blocking Check** | Trigger modal -> Try to click link behind it ("Elemental Selenium"). | Click is intercepted/blocked by the modal overlay. | Medium |
---

## Feature: File Download

> **File:** `test_file_download.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_FD_01 | Verify first available file downloads successfully | Click first download link; poll `test_downloads/` for 10s | File appears on disk without `.crdownload` extension (fully downloaded) | High |

---

## Feature: File Upload

> **File:** `test_file_upload.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_FU_01 | Upload a valid local file and confirm success | `send_keys(absolute_path_to_file)` → click Submit | Page shows *"File Uploaded!"*; uploaded filename matches input | High |
| TC_FU_02 | **Negative:** Submit form with no file selected | Click Submit with empty file input field | Page navigates to backend error; H1 = *"Internal Server Error"* | Medium |

---

## Feature: Floating Menu

> **File:** `test_floating_menu.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_FM_01 | Verify floating menu is visible on initial page load | Navigate to page; locate `#menu` | Menu element `is_displayed()` = **True** | Medium |
| TC_FM_02 | Menu stays visible after heavy bottom scroll | `window.scrollTo(0, scrollHeight)` via JS | `#menu` still displayed; Home and About links visible | High |
| TC_FM_03 | Click anchor link and verify hash navigation | Click "Home" in floating menu | `current_url` contains `#home` | Medium |

---

## Feature: Forgot Password

> **File:** `test_forgot_password.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_FP_01 | Submit a fully valid email address | Input: `test_user_valid@example.com` | Page confirms *"Your e-mail's been sent!"* or handles endpoint 500 gracefully | High |
| TC_FP_02 | **Negative:** Submit blank email field | Input: `""` (empty string) | System rejects; response contains *"Internal Server Error"* | Medium |
| TC_FP_03 | **Negative:** Submit malformed non-email string | Input: `user_without_at_symbol_or_domain` | System rejects or server-errors; response validated for error state | Medium |

---

## Feature: Form Authentication (Login)

> **File:** `test_form_authentication.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_FA_01 | Happy path: valid credentials redirect to secure area | Username: `tomsmith` / Password: `SuperSecretPassword!` | URL contains `/secure`; flash = *"You logged into a secure area!"* | CRITICAL |
| TC_FA_02 | **Negative:** Wrong password | Username: `tomsmith` / Password: `wrongpassword` | Flash = *"Your password is invalid!"* | CRITICAL |
| TC_FA_03 | **Negative:** Wrong username | Username: `wronguser` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | CRITICAL |
| TC_FA_04 | **Negative:** Both fields empty | Username: `""` / Password: `""` | Flash = *"Your username is invalid!"* | High |
| TC_FA_05 | **Negative:** Valid username, empty password | Username: `tomsmith` / Password: `""` | Flash = *"Your password is invalid!"* | High |
| TC_FA_06 | **Negative:** Empty username, valid password | Username: `""` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | High |
| TC_FA_07 | Logout after successful login | Login → Click logout button | Flash = *"You logged out of the secure area!"*; URL = login page | CRITICAL |
| TC_FA_08 | **Negative:** Case-sensitive username check | Username: `TomSmith` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | High |
| TC_FA_09 | **Negative:** Case-sensitive password check | Username: `tomsmith` / Password: `supersecretpassword!` | Flash = *"Your password is invalid!"* | High |
| TC_FA_10 | **Security:** Special characters in username (fuzzing) | Username: `!@#$%^&*` / Password: `SuperSecretPassword!` | System safely rejects; Flash = *"Your username is invalid!"* | CRITICAL |

---

## Feature: Geolocation

> **File:** `test_geolocation.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_GEO_01 | CDP-mocked coordinates populate lat/long fields | CDP mock: Lat=`21.0285`, Long=`105.8542` (Hanoi, VN) → Click *"Where am I?"* | `#lat-value` and `#long-value` contain valid float numbers | High |
| TC_GEO_02 | Google Maps link is generated with correct mocked latitude | Same CDP mock → Click button → inspect `#map-link a[href]` | Href contains *"google"* and the exact mocked latitude value | High |

---

## Feature: Horizontal Slider

> **File:** `test_horizontal_slider.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_HS_01 | Slider increments by 0.5 per ARROW_RIGHT keypress | Click slider → press `ARROW_RIGHT` twice | Values: `0.5` → `1.0` | Medium |
| TC_HS_02 | Boundary max: slider cannot exceed 5 | Press `ARROW_RIGHT` 15× | `#range` = **"5"** (hard maximum) | High |
| TC_HS_03 | Boundary min: slider cannot go below 0 | Move right 2× then left 3× | `#range` = **"0"** (hard minimum) | High |

---

## Feature: Hovers

> **File:** `test_hovers.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_HV_01 | Hover over first user figure reveals caption | `ActionChains.move_to_element(figure[0])` | Caption H5 shows **"name: user1"** | Medium |
| TC_HV_02 | Hover over second user figure reveals caption | `ActionChains.move_to_element(figure[1])` | Caption H5 shows **"name: user2"** | Medium |
| TC_HV_03 | Hover over third user figure reveals caption | `ActionChains.move_to_element(figure[2])` | Caption H5 shows **"name: user3"** | Medium |

---

## Module: Frames (Nested & iFrame)

> **File:** `tests/test_frames.py`
> **Technical Note:** Selenium handles frames as isolated Document Object Models (DOM). Context switching is mandatory.
> **Game Theory Note:** This module tests **Information Asymmetry** (Sự bất đối xứng thông tin). The driver's "worldview" is restricted to its current frame context.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| **TC_FR_01** | `test_iframe_happy_path_tc1` – **Happy Path**: Switch into iFrame, inject text, and verify. | `driver.get("/iframe")` → `switch_to.frame("mce_0_ifr")` → `execute_script("innerHTML = '...'")` → `switch_to.default_content()` | Editor contains injected text; Driver returns to main page context successfully. | High |
| **TC_FR_02** | `test_nested_frames_happy_path_tc2` – **Happy Path**: Full traversal through 4 nested frames. | `driver.get("/nested_frames")` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-left/middle/right")` → `switch_to.default_content()` → `switch_to.frame("frame-bottom")` | Each frame's unique text ("LEFT", "MIDDLE", "RIGHT", "BOTTOM") is correctly validated. | High |
| **TC_FR_03** | `test_frame_context_leak_sad_path_tc3` – **Sad Path (Isolation)**: Attempt to find main page element from inside iFrame. | `switch_to.frame("mce_0_ifr")` → `find_element(By.TAG_NAME, "h3")` (Target: Main Page Heading) | `NoSuchElementException` is raised; proves Driver cannot "see" outside current frame. | Medium |
| **TC_FR_04** | `test_invalid_frame_access_sad_path_tc4` – **Sad Path (Robustness)**: Attempt to switch to a non-existent frame ID. | `driver.get("/iframe")` → `switch_to.frame("ghost_frame_99")` | `NoSuchFrameException` is caught; script handles invalid target gracefully. | Medium |
| **TC_FR_05** | `test_sibling_frame_isolation_sad_path_tc5` – **Sad Path (Hierarchy)**: Direct jump from 'frame-left' to 'frame-right'. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `switch_to.frame("frame-right")` (Directly) | `NoSuchFrameException` is raised; proves Driver must return to parent/root first. | Medium |

---

## Feature: Infinite Scroll

> **File:** `test_infinite_scroll.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_IS_01 | Verify at least one content paragraph loads without scrolling | Navigate to page; count `.jscroll-added` elements | Count ≥ **1** on initial load | Medium |
| TC_IS_02 | Scroll to bottom 3× and verify new content chunks are injected | `window.scrollTo(0, scrollHeight)` × 3; wait for count increase each time | Final paragraph count > initial count (dynamic injection confirmed) | High |

---

## Feature: Number Inputs

> **File:** `test_inputs.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_IN_01 | Valid positive and negative integers accepted | `send_keys("500")` then `send_keys("-35")` | Field value correctly reflects `"500"` then `"-35"` | Medium |
| TC_IN_02 | ARROW_UP increments by 1 | Seed `"10"` → press `ARROW_UP` | Field value = **"11"** | Medium |
| TC_IN_03 | ARROW_DOWN decrements by 1 | Seed `"10"` → press `ARROW_DOWN` | Field value = **"9"** | Medium |
| TC_IN_04 | **Negative:** Alphabetic characters are rejected by `input[type=number]` | `send_keys("abc")` | Field value = **""** (browser blocks non-numeric input) | Medium |

---

## Feature: JS Alerts

> **File:** `test_js_alerts.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_JA_01 | Accept standard JS Alert and verify result | Click Alert button → `alert.accept()` | `#result` = *"You successfully clicked an alert"* | High |
| TC_JA_02 | Accept JS Confirmation dialog | Click Confirm button → `alert.accept()` | `#result` = *"You clicked: Ok"* | High |
| TC_JA_03 | **Negative:** Dismiss (Cancel) JS Confirmation dialog | Click Confirm button → `alert.dismiss()` | `#result` = *"You clicked: Cancel"* | Medium |

---

## Feature: JS Prompt

> **File:** `test_js_prompt.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_JP_01 | **Security:** Inject XSS payload into JS prompt and verify safe reflection | Input: `<script>alert('XSS')</script>` → Accept | `#result` = *"You entered: \<script\>alert('XSS')\</script\>"* (string reflected safely, not executed) | CRITICAL |
| TC_JP_02 | **Negative:** Dismiss prompt without input | Open prompt → `alert.dismiss()` | `#result` = *"You entered: null"* | Medium |

---

## Module: JavaScript Error

> **File:** `test_javascript_error.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_JE_01 | `test_javascript_error_page_loads_tc1` – Happy Path: Navigate to the page and assert it loads with the correct `h3` heading. | `driver.get("/javascript_error")` → `EC.presence_of_element_located((By.TAG_NAME, "h3"))` | `h3.text == "JavaScript Error"`; `is_displayed()` = **True** | Medium |
| TC_JE_02 | `test_javascript_error_console_log_tc2` – Robustness: Extract browser console logs via `get_log('browser')` and assert a SEVERE JS error is captured. | Navigate → `driver.get_log("browser")` → filter `level == "SEVERE"` | At least 1 SEVERE log entry; combined message contains `"Cannot read"`, `"not defined"`, or `"TypeError"` | High |

---

## Module: JQuery UI Menus

> **File:** `test_jquery_ui_menus.py`
> **Note:** Navigation through nested menus requires `ActionChains` hover — standard `.click()` does not reveal sub-menus.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_JQ_01 | `test_jquery_menu_hover_pdf_tc1` – Happy Path: Hover Enabled → Downloads → PDF. Assert PDF link visible, then click it. | Navigate to `/jqueryui/menu` → `ActionChains.move_to_element(Enabled)` → hover `Downloads` → wait for `PDF` link visible → click | PDF link becomes visible in nested sub-menu; click succeeds | High |
| TC_JQ_02 | `test_jquery_menu_hover_excel_tc2` – Happy Path: Hover Enabled → Downloads → Excel. Assert Excel link visible, then click it. | Same hover chain → wait for `Excel` link visible → click | Excel link becomes visible in nested sub-menu; click succeeds | High |
| TC_JQ_03 | `test_jquery_menu_disabled_not_clickable_tc3` – Sad Path: Click the 'Disabled' item. Assert URL does not change (navigation blocked). | Locate `li.ui-state-disabled a` → assert class → click → compare `current_url` before/after | `url_before == url_after`; disabled item does not trigger navigation | Medium |
| TC_JQ_04 | `test_jquery_menu_disabled_no_submenu_tc4` – Sad Path: Hover over 'Disabled' item. Assert no sub-menu appears within 2s. | Hover `li.ui-state-disabled a` → `WebDriverWait(2).until(EC.visibility_of_element_located(sub-menu))` | `TimeoutException` caught — no sub-menu appears for disabled item | Medium |

---

## Feature: Key Presses

> **File:** `test_key_presses.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_KP_01 | Special/non-printable keyboard keys are detected and named correctly | Payloads: `SPACE`, `ENTER`, `TAB`, `ESCAPE`, `BACKSPACE`, `ALT` | Each `#result` matches the expected uppercase key name (e.g., *"You entered: SPACE"*) | High |
| TC_KP_02 | Alphanumeric keys are reflected with correct uppercase/label mapping | Payloads: `"a"→A`, `"Z"→Z`, `"7"→7`, `"@"→COMMERCIAL_AT` | Each `#result` accurately maps to the expected uppercase label | Medium |

---

## Module: Large & Deep DOM

> **File:** `test_large_deep_dom.py`
> **Note:** The page generates a 50×50 grid of `<div>` elements with IDs in the format `large-{row}-{col}`. BVA targets the boundary cell `large-50-50`.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_LD_01 | `test_large_dom_deep_sibling_tc1` – Happy Path: Locate a specific deep sibling by ID (`large-2-5`) and verify its text. | Navigate to `/large` → `EC.presence_of_element_located((By.ID, "large-2-5"))` → read `.text` | Element found; text **contains** `"2.5"` | High |
| TC_LD_02 | `test_large_dom_boundary_cell_tc2` – Happy Path (BVA Max): Locate the boundary cell `large-50-50` and verify its text. | `EC.presence_of_element_located((By.ID, "large-50-50"))` → read `.text` | Element found; text **contains** `"50.50"` | High |
| TC_LD_03 | `test_large_dom_invalid_id_sad_path_tc3` – Sad Path: Attempt to find a non-existent element `#large-999-999`. Assert graceful failure. | `WebDriverWait(2).until(EC.presence_of_element_located((By.ID, "large-999-999")))` | `TimeoutException` caught — element correctly absent | Medium |
| TC_LD_04 | `test_large_dom_invalid_xpath_sad_path_tc4` – Sad Path: Attempt to find a deep cell via an invalid XPath (column 51 beyond grid). Assert graceful failure. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//div[@id='large-0-0']//td[51]")))` | `TimeoutException` caught — XPath target correctly absent | Medium |

---

## Module: Notification Messages

> **File:** `test_notification_messages.py`
> **Note:** Flash messages are randomly selected from a set. Use `assertIn(flash_text, VALID_MESSAGES)` to prevent flaky tests. Valid messages: `"Action successful"`, `"Action unsuccessful, please try again"`.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_NM_01 | `test_notification_single_click_ep_tc1` – Happy Path: Click 'Click here' once and assert the flash message is in the valid list. | Navigate to `/notification_message` → click link → wait for `#flash` | `flash.text` **is in** `VALID_MESSAGES` | High |
| TC_NM_02 | `test_notification_multi_click_ep_tc2` – Happy Path: Click the link 5 times; each response must be a valid message. | Repeat 5×: navigate → click → verify `#flash` text | All 5 flash messages are **in** `VALID_MESSAGES` | Medium |
| TC_NM_03 | `test_notification_no_unexpected_message_tc3` – Sad Path: Assert flash is never empty and never contains the word "error". | Click once → read `#flash` → `assertNotIn("error", text.lower())` | Flash is non-empty; does **not** contain `"error"` | Medium |
| TC_NM_04 | `test_notification_direct_render_robustness_tc4` – Robustness: Navigate directly to `/notification_message_rendered`. Assert a valid flash is shown. | `driver.get("/notification_message_rendered")` → wait for `#flash` | Flash text **is in** `VALID_MESSAGES` on direct render | Medium |

---

## Module: Redirect Link

> **File:** `test_redirect_link.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_RL_01 | `test_redirect_link_url_change_tc1` – Happy Path: Click the redirect link and assert the URL changes to the Status Codes destination. | Navigate to `/redirector` → click `a[href='redirect']` → `EC.url_contains("status_codes")` | `current_url` changes to `https://the-internet.herokuapp.com/status_codes` | High |
| TC_RL_02 | `test_redirect_link_destination_content_tc2` – Happy Path: Follow redirect and verify the destination page heading. | Navigate → click redirect link → wait for `h3` at destination | `h3.text` **contains** `"Status Codes"` | High |
| TC_RL_03 | `test_redirect_invalid_endpoint_tc3` – Sad Path: Navigate directly to a non-existent redirect endpoint. Assert Status Codes page is not shown. | `driver.get("/redirect/nonexistent_page_404")` → read `body.text` | Body does NOT contain `"Status Codes"`; invalid path handled | Medium |
| TC_RL_04 | `test_redirect_link_absent_on_wrong_page_tc4` – Sad Path: Confirm redirect link is absent on the destination page (one-way redirect). | Navigate to `/status_codes` → `WebDriverWait(2).until(EC.presence_of_element_located(a[href='redirect']))` | `TimeoutException` caught — redirect link correctly absent on destination | Medium |

---

## Module: Shadow DOM

> **File:** `test_shadow_dom.py`
> **Note:** Shadow DOM creates encapsulated DOM subtrees. Standard XPath from the document root **cannot** pierce shadow boundaries. Access requires Selenium 4's `.shadow_root` property or JavaScript `element.shadowRoot.querySelector()`.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_SD_01 | `test_shadow_dom_access_via_shadow_root_tc1` – Happy Path: Access shadow host `my-paragraph` via Selenium 4 `.shadow_root`, then find inner `<p>` and verify text. | Navigate to `/shadowdom` → `EC.presence_of_element_located((By.CSS_SELECTOR, "my-paragraph"))` → `.shadow_root` → `.find_element(By.CSS_SELECTOR, "p")` | Inner `<p>` is accessible; text is non-empty and contains `"shadow"` | High |
| TC_SD_02 | `test_shadow_dom_access_via_js_tc2` – Happy Path: Pierce shadow root via `execute_script("element.shadowRoot.querySelector('p')")`. Assert content is returned. | Navigate → JS: `document.querySelector('my-paragraph').shadowRoot.querySelector('p').textContent` | Returns non-null, non-empty text from within the shadow root | High |
| TC_SD_03 | `test_shadow_dom_xpath_cannot_pierce_tc3` – Sad Path: Attempt standard `//my-paragraph//p` XPath from the document root (cannot pierce shadow boundary). Assert failure. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//my-paragraph//p[...]")))` | `TimeoutException` or `NoSuchElementException` — XPath correctly blocked by shadow encapsulation | Medium |

---

## Feature: Shifting Content

> **File:** `test_shifting_content.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_SC_01 | Verify menu element pixel coordinates shift deterministically between base and forced-shift URLs | Load base URL → capture `location`; load `?mode=random&pixel_shift=100` → recapture | Absolute difference in X or Y > **10 pixels** | Medium |

---

## Module: Slow Resources

> **File:** `test_slow_resources.py`
> **Note:** The Slow Resources page deliberately delays page load. BVA timeouts (0s, 1s) are used to verify `TimeoutException` is raised and caught gracefully.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_SR_01 | `test_slow_resources_full_load_tc1` – Happy Path: Navigate to Slow Resources and wait generously (30s) for the page heading to appear. | `driver.get("/slow")` → `WebDriverWait(30).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | Heading is displayed; text is non-empty | High |
| TC_SR_02 | `test_slow_resources_short_timeout_bva_tc2` – Sad Path (BVA): Use 1s timeout after navigation. Assert `TimeoutException` is caught — page cannot load that fast. | Navigate → `WebDriverWait(1).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | `TimeoutException` caught; `self.fail()` called if element appears within 1s | High |
| TC_SR_03 | `test_slow_resources_zero_timeout_boundary_tc3` – Sad Path (BVA Min): Use 0s timeout — absolute minimum that must always expire immediately. | Navigate → `WebDriverWait(0).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | `TimeoutException` caught immediately; 0s boundary always fails for slow page | Medium |

---

## Module: Sortable Data Tables

> **File:** `test_sortable_data_tables.py`
> **Note:** Table data is extracted into Python lists and compared to `sorted()` to assert column sort order.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_ST_01 | `test_sortable_tables_sort_lastname_asc_tc1` – Happy Path: Click 'Last Name' header once to sort ASC. Extract column, compare to `sorted(actual)`. | Navigate to `/tables` → `table1 th[Last Name]`.click() → extract col 1 values | `actual == sorted(actual)` — Last Name sorted alphabetically ASC | High |
| TC_ST_02 | `test_sortable_tables_sort_lastname_desc_tc2` – Happy Path: Double-click 'Last Name' header to sort DESC. Compare to `sorted(actual, reverse=True)`. | Click `th[Last Name]` twice → extract col 1 values | `actual == sorted(actual, reverse=True)` — Last Name sorted DESC | High |
| TC_ST_03 | `test_sortable_tables_unsortable_column_tc3` – Sad Path: Table 2 Email column has no `<span>` sort indicator. Assert `TimeoutException` when looking for one. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//table[@id='table2']//th[span[text()='Email']]")))` | `TimeoutException` caught — unsortable column has no sort control | Medium |
| TC_ST_04 | `test_sortable_tables_out_of_bounds_column_tc4` – Sad Path: Extract column index 99 (beyond table bounds). Assert empty list returned gracefully. | `_get_column_values("table1", col_index=99)` using XPath `td[99]` | Returns `[]` empty list — out-of-bounds column index yields no elements | Medium |

---

## Feature: Status Codes

> **File:** `test_status_codes.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_SC_01 | Verify 200 OK routing and response message | Click "200" link | Page text contains: *"This page returned a 200 status code."* | High |
| TC_SC_02 | Verify 301 Moved Permanently routing | Click "301" link | Page text contains: *"This page returned a 301 status code."* | High |
| TC_SC_03 | Verify 404 Not Found routing | Click "404" link | Page text contains: *"This page returned a 404 status code."* | High |
| TC_SC_04 | Verify 500 Internal Server Error routing | Click "500" link | Page text contains: *"This page returned a 500 status code."* | High |

---

## Module: Typos

> **File:** `test_typos.py`
> **Note:** This page randomly serves two A/B variants: one with correct `"won't"` and one with the bug `"won,t"`. Tests must handle random output using refresh loops and classify the result.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_TY_01 | `test_typos_refresh_until_correct_tc1` – Happy Path: Refresh the page up to 10× until the correct `"won't"` text appears. Assert it is eventually served. | `for i in range(10): driver.get(URL)` → read second `<p>` → break if `"won't"` in text | Correct text appears within 10 refreshes; `found_correct == True` | Medium |
| TC_TY_02 | `test_typos_detect_known_typo_tc2` – A/B Bug Detection: In a single run, classify and log the variant. If `"won,t"` appears, log as an A/B defect; if `"won't"` appears, log as correct. | Loop until either variant found → log `"⚠ A/B BUG DETECTED"` or `"Correct variant"` accordingly | Either variant classified and logged correctly; test passes in both cases (it is a detection test) | High |
| TC_TY_03 | `test_typos_page_structure_robustness_tc3` – Robustness: Assert the page always has exactly 2 `<p>` elements regardless of A/B variant. | `driver.get(URL)` → `EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example p"))` | `len(paragraphs) == 2`; second paragraph text matches one of the two known variant strings | Medium |

---

## Module: WYSIWYG Editor (TinyMCE)

> **File:** `test_wysiwyg_editor.py`
> **Technical Challenge:** The TinyMCE editor may display a `"TinyMCE is in read-only mode"` overlay when its API key limit is reached. `send_keys()` is blocked. The workaround is `execute_script("arguments[0].innerHTML = '...';")` to inject content directly into the `#tinymce` body inside the iframe. The toolbar lives in the **main document**, not inside the iframe.

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity |
| :--- | :--- | :--- | :--- | :--- |
| TC_WY_01 | `test_wysiwyg_js_injection_happy_path_tc1` – Happy Path: Switch to `mce_0_ifr` iframe, inject text via `execute_script("arguments[0].innerHTML = '...'")`, then read back innerHTML and verify. | `frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr"))` → `find_element(By.ID, "tinymce")` → `execute_script("arguments[0].innerHTML = arguments[1]", body, "<p>...</p>")` → read back `innerHTML` | `INJECT_TEXT` found in returned `innerHTML`; injection bypasses read-only intercept | CRITICAL |
| TC_WY_02 | `test_wysiwyg_readonly_alert_sad_path_tc2` – Sad/Robustness: Detect the `.tox-notification--warning` read-only overlay in the main document (5s wait). Assert it is visible if present; log clean exit if absent. | Navigate → `WebDriverWait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tox-notification--warning")))` | Overlay detected and `is_displayed()` = True; OR `TimeoutException` caught gracefully (API limit not hit) | High |
| TC_WY_03 | `test_wysiwyg_toolbar_visibility_happy_path_tc3` – Happy Path: In the **main document** context, locate and assert the Bold and Italic toolbar buttons are visible. | Wait for `.tox-toolbar__primary` → `find_element(By.XPATH, "//button[@aria-label='Bold']")` → `find_element(By.XPATH, "//button[@aria-label='Italic']")` | Both buttons `is_displayed()` = **True** in main document | High |
| TC_WY_04 | `test_wysiwyg_context_isolation_sad_path_tc4` – Sad Path: After switching into the iframe, attempt to `find_element` for the Bold toolbar button. Assert `NoSuchElementException` (toolbar is in main document, not iframe). | `switch_to.frame("mce_0_ifr")` → `find_element(By.XPATH, "//button[@aria-label='Bold']")` | `NoSuchElementException` raised — context isolation confirmed; toolbar invisible from inside iframe | Medium |

---

## Appendix: Test ID Prefix Reference

| Prefix | Feature |
| :--- | :--- |
| `TC_AB` | A/B Testing |
| `TC_ARE` | Add / Remove Elements |
| `TC_BA` | Basic Authentication |
| `TC_BI` | Broken Images |
| `TC_CB` | Checkboxes |
| `TC_CD` | Challenging DOM |
| `TC_CM` | Context Menu |
| `TC_DE` | Disappearing Elements |
| `TC_DD` | Drag and Drop / Dropdown |
| `TC_DA` | Digest Authentication |
| `TC_DC` | Dynamic Content |
| `TC_DY` | Dynamic Controls |
| `TC_DL` | Dynamic Loading |
| `TC_EA` | Entry Ad |
| `TC_FD` | File Download |
| `TC_FU` | File Upload |
| `TC_FM` | Floating Menu |
| `TC_FP` | Forgot Password |
| `TC_EI` | Exit Intent |
| `TC_FA` | Form Authentication |
| `TC_GEO` | Geolocation |
| `TC_HS` | Horizontal Slider |
| `TC_HV` | Hovers |
| `TC_IF` | iFrame |
| `TC_IS` | Infinite Scroll |
| `TC_IN` | Number Inputs |
| `TC_JA` | JS Alerts |
| `TC_JP` | JS Prompt |
| `TC_JE` | JavaScript Error |
| `TC_JQ` | JQuery UI Menus |
| `TC_KP` | Key Presses |
| `TC_LD` | Large & Deep DOM |
| `TC_NM` | Notification Messages |
| `TC_RL` | Redirect Link |
| `TC_SC` | Shifting Content / Status Codes |
| `TC_SD` | Shadow DOM |
| `TC_SR` | Slow Resources |
| `TC_ST` | Sortable Data Tables |
| `TC_TY` | Typos |
| `TC_WY` | WYSIWYG Editor (TinyMCE) |
