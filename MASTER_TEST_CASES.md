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

## Feature: Context Menu

> **File:** `test_context_menu.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_CM_01 | Right-click the hotspot to trigger JS alert | `ActionChains.context_click()` on `#hot-spot` | Alert appears with text: *"You selected a context menu"* | High |
| TC_CM_02 | Negative: Verify left-click does NOT trigger the alert | `ActionChains.click()` on `#hot-spot` | **No alert** appears within 2-second fast-fail window | Medium |

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

## Feature: iFrame (TinyMCE Editor)

> **File:** `test_iframe.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_IF_01 | Switch into iframe, clear editor, type new text, switch out | `switch_to.frame("mce_0_ifr")` → `Ctrl+A` + `DELETE` → `send_keys("Standard Selenium Frame Input Test")` → `switch_to.default_content()` | Editor contains injected text; H3 on parent page contains *"An iFrame"* | High |

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

## Feature: Key Presses

> **File:** `test_key_presses.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_KP_01 | Special/non-printable keyboard keys are detected and named correctly | Payloads: `SPACE`, `ENTER`, `TAB`, `ESCAPE`, `BACKSPACE`, `ALT` | Each `#result` matches the expected uppercase key name (e.g., *"You entered: SPACE"*) | High |
| TC_KP_02 | Alphanumeric keys are reflected with correct uppercase/label mapping | Payloads: `"a"→A`, `"Z"→Z`, `"7"→7`, `"@"→COMMERCIAL_AT` | Each `#result` accurately maps to the expected uppercase label | Medium |

---

## Feature: Shifting Content

> **File:** `test_shifting_content.py`

| Test Case ID | Scenario Description | Input Data / Actions | Expected Result | Severity/Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC_SC_01 | Verify menu element pixel coordinates shift deterministically between base and forced-shift URLs | Load base URL → capture `location`; load `?mode=random&pixel_shift=100` → recapture | Absolute difference in X or Y > **10 pixels** | Medium |

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

## Appendix: Test ID Prefix Reference

| Prefix | Feature |
| :--- | :--- |
| `TC_ARE` | Add / Remove Elements |
| `TC_BA` | Basic Authentication |
| `TC_BI` | Broken Images |
| `TC_CB` | Checkboxes |
| `TC_CM` | Context Menu |
| `TC_DE` | Disappearing Elements |
| `TC_DD` | Drag and Drop / Dropdown |
| `TC_DC` | Dynamic Content |
| `TC_DY` | Dynamic Controls |
| `TC_EA` | Entry Ad |
| `TC_FD` | File Download |
| `TC_FU` | File Upload |
| `TC_FM` | Floating Menu |
| `TC_FP` | Forgot Password |
| `TC_FA` | Form Authentication |
| `TC_GEO` | Geolocation |
| `TC_HS` | Horizontal Slider |
| `TC_HV` | Hovers |
| `TC_IF` | iFrame |
| `TC_IS` | Infinite Scroll |
| `TC_IN` | Number Inputs |
| `TC_JA` | JS Alerts |
| `TC_JP` | JS Prompt |
| `TC_KP` | Key Presses |
| `TC_SC` | Shifting Content / Status Codes |
