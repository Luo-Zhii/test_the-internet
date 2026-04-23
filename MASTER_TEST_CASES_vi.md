# Đặc tả Ca Kiểm thử Master
### Dự án: The Internet – Bộ Tự động hóa Selenium
**Người chuẩn bị:** QA Automation Team  
**Ngày:** 22-04-2026  
**Tổng số tệp test:** 27 | **Tổng số ca kiểm thử:** 77+

---

## 1. Tóm tắt Tổng quan (Executive Summary)

Tài liệu này là đặc tả nguồn-sự-thật-duy-nhất (single-source-of-truth) cho toàn bộ bộ kiểm thử tự động Selenium đầu-cuối (end-to-end) nhắm vào [The Internet (Herokuapp)](https://the-internet.herokuapp.com). Khung kiểm thử (framework) được xây dựng dựa trên:

| Trụ cột Chiến lược | Chi tiết Triển khai |
| :--- | :--- |
| **Framework** | Python `unittest.TestCase` kết hợp với `webdriver_manager` để quản lý vòng đời trình điều khiển (driver) tự động |
| **Chiến lược Chờ** | Loại trừ hoàn toàn **Explicit Waits** (`WebDriverWait` + `expected_conditions`). Hành vi `time.sleep()` bị **nghiêm cấm**. |
| **Kiểm thử Phủ định** | Các kỹ thuật Hộp đen ISTQB: Phân tích Giá trị Biên (BVA), Đoán lỗi (Error Guessing), và Tiêm mã Bảo mật (SQLi/XSS) |
| **Phủ sóng Bảo mật** | XSS payloads (`<script>alert('XSS')</script>`), SQL Injection (`' OR 1=1 --`), và fuzzing ký tự đặc biệt |
| **Xử lý Race Condition** | Kiểm tra `staleness_of` trên các phần tử DOM trong quá trình tải lại trang để ngăn chặn các khẳng định (assertions) không ổn định |
| **Giả lập Vị trí** | Giao thức Chrome DevTools (CDP) thông qua `execute_cdp_cmd` để ghi đè các thông báo cấp hệ điều hành bằng tọa độ xác định |
| **HTML5 Drag & Drop** | Tiêm mã JavaScript (`execute_script`) để vượt qua các hạn chế kéo-và-thả HTML5 gốc của WebDriver |
| **Kiến trúc DRY** | Các phương thức `helper_*` nội bộ bên trong mỗi lớp test để trung tâm hóa các hành động lặp lại |
| **Tính quan sát** | Tất cả các luồng kiểm thử phủ định đều phát ra vết `print()` (Hành động / Kỳ vọng / Thực tế) để soát xét log CI một cách xác định |

---

## Module: A/B Testing

> **Tệp:** `test_ab_testing.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_AB_01 | `test_ab_testing_header_variation_tc1` – Happy Path: Tiêu đề h3 phải khớp với một trong hai biến thể A/B đã biết để ngăn chặn các khẳng định không ổn định. | Điều hướng tới `/abtest` → `EC.visibility_of_element_located((By.TAG_NAME, "h3"))` → đọc `h3.text` | `h3.text` **nằm trong** `["A/B Test Control", "A/B Test Variation 1"]` | Cao |
| TC_AB_02 | `test_ab_testing_paragraph_presence_tc2` – Kiểm tra Giao diện: Đoạn văn bản thông tin bên dưới tiêu đề phải luôn hiện diện bất kể biến thể A/B nào được phục vụ. | Điều hướng tới `/abtest` → tìm phần tử `<p>` chứa chuỗi *"Also known as split testing"* | Đoạn văn hiện diện và `is_displayed()` = **True** | Trung bình |
| TC_AB_03 | `test_ab_testing_optout_cookie_tc3` – Độ ổn định: Thêm cookie thoát (opt-out) A/B trước khi tải lại trang không được làm hỏng trang — tiêu đề vẫn phải tải được. | Điều hướng tới `/abtest` → `driver.add_cookie({'name': 'optimizelyOptOut', 'value': 'true'})` → `driver.refresh()` → đợi `h3` | Phần tử `h3` hiện diện và văn bản của nó nằm trong danh sách các biến thể đã biết | Trung bình |

---

## Feature: Add / Remove Elements

> **Tệp:** `test_add_remove_elements.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_ARE_01 | Thêm một phần tử duy nhất và xác minh nó xuất hiện trong DOM | Click "Add Element" một lần | Chính xác **1** nút Delete hiển thị | Cao |
| TC_ARE_02 | Thêm sau đó xóa ngay lập tức một phần tử duy nhất | Click Add → Click Delete | DOM trở về **0** nút Delete; xác nhận trạng thái staleness | Cao |
| TC_ARE_03 | Thêm nhiều phần tử trong thời gian ngắn liên tiếp | Click "Add Element" **5 lần** | Chính xác **5** nút Delete hiện diện | Trung bình |
| TC_ARE_04 | Xóa tất cả các phần tử từng cái một (biên trạng thái trống) | Thêm 3 → Xóa từng cái với xác nhận `staleness_of` | **0** nút Delete còn lại; DOM hoàn toàn sạch | Cao |

---

## Feature: Basic Authentication

> **Tệp:** `test_basic_auth.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_BA_01 | Xác thực HTTP Basic qua thông tin đăng nhập nhúng trong URL | URL: `https://admin:admin@...` | Trang hiển thị: *"Congratulations! You must have the proper credentials."* | NGHIÊM TRỌNG |

---

## Feature: Broken Images

> **Tệp:** `test_broken_images.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_BI_01 | Xác minh tổng số hình ảnh được kết xuất trên trang | Tìm tất cả các thẻ `<img>` | Ít nhất **3** hình ảnh hiện diện | Trung bình |
| TC_BI_02 | Nhận diện các hình ảnh bị hỏng qua kiểm tra phản hồi HTTP | HTTP GET từng `src`; kiểm tra mã trạng thái | Chính xác **2** hình ảnh trả về mã khác 200 (bị hỏng) | Cao |
| TC_BI_03 | Xác nhận có ít nhất một hình ảnh hợp lệ (200 OK) tồn tại | HTTP GET từng `src`; lọc các phản hồi 200 | Ít nhất **1** hình ảnh hợp lệ được xác nhận | Trung bình |

---

## Feature: Checkboxes

> **Tệp:** `test_checkbox.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_CB_01 | Xác minh trạng thái được chọn/không được chọn mặc định khi tải | Điều hướng tới trang; đọc `is_selected()` | CB1 = **không chọn**, CB2 = **đang chọn** | Cao |
| TC_CB_02 | Chọn checkbox ban đầu không được chọn | Click Checkbox 1 nếu chưa chọn | CB1 chuyển sang trạng thái **đã chọn** | Trung bình |
| TC_CB_03 | Bỏ chọn checkbox ban đầu đang được chọn | Click Checkbox 2 nếu đang chọn | CB2 chuyển sang trạng thái **chưa chọn** | Trung bình |
| TC_CB_04 | Kiểm tra tải việc chuyển đổi cả hai checkbox qua nhiều lần đảo trạng thái | Click CB1 hai lần; Click CB2 hai lần | Các trạng thái cuối cùng trở lại ban đầu (CB1=không chọn, CB2=đang chọn) | Trung bình |

---

## Feature: Challenging DOM

> **Tệp:** `test_challenging_dom.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_CD_01 | TC1_Dynamic_Buttons: Tìm nút Màu đỏ mà không dùng ID. Click và khẳng định. | Tìm nút bằng XPath tương đối hoặc CSS `.button.alert` | Click thành công; kiểm thử khẳng định nút còn lại hoặc trang tải lại | Cao |
| TC_CD_02 | TC2_Table_EP_Mid: (Equivalence Partitioning) Trích xuất và xác minh dữ liệu từ Hàng 5. | Đợi và tìm `//table/tbody/tr[5]` | Dữ liệu được trích xuất và xác thực so với giá trị kỳ vọng của Hàng 5 | Trung bình |
| TC_CD_03 | TC3_Table_BVA_Min: (Boundary Value Analysis) Trích xuất và xác minh dữ liệu từ Hàng 1. | Đợi và tìm `//table/tbody/tr[1]` | Dữ liệu được trích xuất và xác thực so với Biên Tối thiểu (hàng đầu tiên) | Cao |
| TC_CD_04 | TC4_Table_BVA_Max: (Boundary Value Analysis) Trích xuất và xác minh dữ liệu từ Hàng 10. | Đợi và tìm `//table/tbody/tr[10]` | Dữ liệu được trích xuất và xác thực so với Biên Tối đa (hàng cuối cùng) | Cao |
| TC_CD_05 | TC5_Table_Negative_OutOfBounds: Cố gắng tìm Hàng 11. | Khối `try-except` tìm Hàng 11 với thời gian chờ 2 giây | TimeoutException/NoSuchElementException được bắt một cách nhẹ nhàng | Cao |
| TC_CD_06 | TC6_Canvas_Verification: Xác minh sự hiện diện của phần tử Canvas. | Tìm CSS selector `canvas#canvas` hoặc `canvas` | Phần tử Canvas được xác nhận hiện diện trên trang | Trung bình |
| **TC_CD_07** | **Các liên kết Hành động trong Bảng (Sửa/Xóa)** | Tìm các liên kết 'edit'/'delete' ở Hàng 3 dùng XPath tương đối. Click chúng. | URL thêm chính xác các đoạn mã `#edit` hoặc `#delete`. | Trung bình |

---

## Module: Dynamic Loading

> **Tệp:** `test_dynamic_loading.py`

| Mã Ca Kiểm Thử | Tên Phương Thức | Kỹ thuật | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TC_DL_01 | `test_hidden_element_ep_tc1` | EP – Happy Path | Click Start ở Ví dụ 1 (phần tử ẩn). Đợi thanh tải biến mất, sau đó khẳng định 'Hello World!' hiển thị. | Điều hướng tới `/dynamic_loading/1` → Click nút `#start` → `EC.invisibility_of_element_located((By.ID, "loading"))` | Phần tử `#finish` hiển thị; văn bản = **"Hello World!"** | Cao |
| TC_DL_02 | `test_rendered_element_ep_tc2` | EP – Happy Path | Click Start ở Ví dụ 2 (phần tử được kết xuất sau khi tải). Đợi thanh tải biến mất, khẳng định 'Hello World!' được kết xuất và hiển thị. | Điều hướng tới `/dynamic_loading/2` → Click nút `#start` → `EC.invisibility_of_element_located((By.ID, "loading"))` | Phần tử `#finish` được kết xuất trong DOM và hiển thị; văn bản = **"Hello World!"** | Cao |
| TC_DL_03 | `test_double_click_sad_path_tc3` | Sad Path – Độ ổn định | Click đúp nhanh vào nút Start để kiểm tra trạng thái kích hoạt trùng lặp. Khẳng định kết quả cuối cùng vẫn đúng. | Điều hướng tới `/dynamic_loading/1` → Click đúp nút `#start` liên tiếp nhanh → Đợi quá trình tải kết thúc | Phần tử `#finish` cuối cùng hiển thị **"Hello World!"** mà không bị treo hay lỗi | Trung bình |
| TC_DL_04 | `test_missing_element_sad_path_tc4` | Sad Path – Phủ định | Cố gắng tìm một nút Start không tồn tại bằng selector sai `button#wrong-id`. Khẳng định `TimeoutException` được bắt nhẹ nhàng. | Điều hướng tới `/dynamic_loading/1` → `try-except` với `self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#wrong-id")))` | `TimeoutException` được kích hoạt và bắt được; gọi `self.fail()` nếu ngoại lệ KHÔNG xảy ra | Cao |
| TC_DL_05 | `test_short_timeout_bva_tc5` | BVA – Biên Thời gian chờ Ngắn | Click Start, sau đó đợi thanh tải biến mất dùng thời gian chờ cực ngắn 0.5 giây không thực tế. Khẳng định `TimeoutException` được bắt được. | Điều hướng tới `/dynamic_loading/1` → Click nút `#start` → `WebDriverWait(self.driver, 0.5).until(EC.invisibility_of_element_located((By.ID, "loading")))` | `TimeoutException` được kích hoạt và bắt được; gọi `self.fail()` nếu ngoại lệ KHÔNG xảy ra | Cao |

---

## Feature: Context Menu

> **Tệp:** `test_context_menu.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_CM_01 | Click chuột phải vào vùng hotspot để kích hoạt cảnh báo JS | `ActionChains.context_click()` trên `#hot-spot` | Cảnh báo xuất hiện với văn bản: *"You selected a context menu"* | Cao |
| TC_CM_02 | Phủ định: Xác minh click chuột trái KHÔNG kích hoạt cảnh báo | `ActionChains.click()` trên `#hot-spot` | **Không có cảnh báo** nào xuất hiện trong cửa sổ 2 giây chờ thất bại nhanh | Trung bình |

---

## Module: Digest Authentication

> **Tệp:** `test_digest_auth.py`
> **Ghi chú:** Selenium không thể tương tác với các hộp thoại xác thực HTTP 401 gốc. Thông tin đăng nhập được bỏ qua bằng cách nhúng chúng vào URL: `https://{user}:{pass}@the-internet.herokuapp.com/digest_auth`. Các ký tự đặc biệt trong thông tin đăng nhập PHẢI được mã hóa phần trăm bằng `urllib.parse.quote(credential, safe="")`.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DA_01 | `test_digest_auth_happy_path_tc1` – Happy Path: Điều hướng với thông tin hợp lệ. Khẳng định thông báo thành công hiển thị. | URL: `https://admin:admin@.../digest_auth` → `EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Congratulations')]"))` | `<p>` hiển thị; văn bản **chứa** *"Congratulations"* | NGHIÊM TRỌNG |
| TC_DA_02 | `test_digest_auth_invalid_creds_tc2` – Phủ định: Điều hướng với mật khẩu sai. Khẳng định thông báo thành công vắng mặt qua `TimeoutException`. | URL: `https://admin:wrong@.../digest_auth` → 2 giây `try-except TimeoutException` cho `<p>` thành công → `assertNotIn` trên `body.text` | `TimeoutException` được bắt; xác nhận văn bản thành công vắng mặt trong body | Cao |
| TC_DA_03 | `test_digest_auth_unauthorized_tc3` – Bảo mật: Điều hướng tới endpoint mà KHÔNG có thông tin đăng nhập. Khẳng định trang từ chối truy cập. | URL: `https://the-internet.herokuapp.com/digest_auth` (không có `user:pass`) → 2 giây `try-except TimeoutException` → đọc `body.text` | `TimeoutException` được bắt; văn bản thành công vắng mặt; body có thể hiển thị *"Not authorized"* | Cao |
| TC_DA_04 | `test_digest_auth_special_chars_tc4` – Độ ổn định: Dùng `urllib.parse.quote()` để mã hóa mật khẩu có ký tự đặc biệt (`admin@123`) trước khi nhúng vào URL. Khẳng định URL được xây dựng đúng (xác minh việc mã hóa) và trang phản hồi. | `urllib.parse.quote("admin@123", safe="")` → xác minh `%40` trong kết quả → điều hướng → khẳng định thành công vắng mặt (Heroku từ chối mật khẩu này, nhưng việc xây dựng URL được xác thực) | `assertIn("%40", encoded_pass)` vượt qua; trang từ chối chính xác thông tin sai | Trung bình |

---

## Feature: Disappearing Elements

> **Tệp:** `test_disappearing_elements.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DE_01 | Xác minh các liên kết điều hướng vĩnh viễn luôn hiển thị | Kiểm tra Home, About, Contact, Portfolio qua `LINK_TEXT` | Cả 4 liên kết đều hiển thị | Cao |
| TC_DE_02 | Xác minh liên kết "Gallery" biến mất ngẫu nhiên sẽ xuất hiện trong vòng 5 lần tải lại | Tải lại tối đa 5 lần cho đến khi thấy link Gallery; click nó | Link Gallery cuối cùng xuất hiện; click dẫn đến trang 404 kỳ vọng | Trung bình |

---

## Feature: Drag and Drop

> **Tệp:** `test_drag_and_drop.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DD_01 | Kéo Khối A lên Khối B và xác minh việc hoán đổi | Dùng JS tiêm lệnh `simulateHTML5DragAndDrop(colA → colB)` | Cột A hiển thị **"B"**, Cột B hiển thị **"A"** | Cao |
| TC_DD_02 | Kéo đúp để hoàn trả các khối về vị trí ban đầu | Kéo JS A→B, sau đó B→A | Các cột hoàn trả: A hiển thị **"A"**, B hiển thị **"B"** | Cao |

---

## Feature: Dropdown

> **Tệp:** `test_dropdown.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DD_01 | Xác thực trạng thái placeholder mặc định | Đọc `first_selected_option` khi tải | Văn bản = *"Please select an option"*; tùy chọn bị **vô hiệu hóa** (disabled) | Cao |
| TC_DD_02 | Chọn Option 1 bằng index | `select_by_index(1)` | Văn bản tùy chọn được chọn = **"Option 1"** | Trung bình |
| TC_DD_03 | Chọn Option 2 bằng văn bản hiển thị | `select_by_visible_text("Option 2")` | Văn bản tùy chọn được chọn = **"Option 2"** | Trung bình |
| TC_DD_04 | Chuyển đổi giữa các tùy chọn để xác nhận việc ghi đè | `select_by_value("1")` sau đó `select_by_value("2")` | Lựa chọn ghi đè chính xác từ Option 1 → Option 2 | Trung bình |

---

## Feature: Dynamic Content

> **Tệp:** `test_dynamic_content.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DC_01 | Xác minh 3 hàng hình ảnh và văn bản luôn hiển thị | Điều hướng tới URL gốc; đếm các hàng | Chính xác **3 hình ảnh** và **3 khối văn bản** hiện diện | Cao |
| TC_DC_02 | Xác nhận nội dung ngẫu nhiên hóa khi tải lại trang | Tải lại tối đa 3 lần; so sánh kết quả chụp `src`/văn bản | Ít nhất một hình ảnh **hoặc** khối văn bản thay đổi sau các lần tải lại | Trung bình |
| TC_DC_03 | Xác minh `?with_content=static` khóa hai hàng đầu tiên | Tải URL tĩnh; tải lại; so sánh 2 hàng đầu | 2 cặp hình ảnh+văn bản đầu tiên giữ **nguyên vẹn**; hàng thứ 3 có thể thay đổi | Cao |

---

## Feature: Dynamic Controls

> **Tệp:** `test_dynamic_controls.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_DY_01 | Xóa checkbox khỏi DOM qua click nút | Click "Remove"; đợi `staleness_of` | `#message` = *"It's gone!"*; số lượng `#checkbox` = 0 | Cao |
| TC_DY_02 | Thêm lại checkbox sau khi xóa | Xóa → sau đó click "Add" | `#message` = *"It's back!"*; `#checkbox` hiển thị | Cao |
| TC_DY_03 | Kích hoạt một ô nhập liệu đang bị vô hiệu hóa | Click "Enable"; đợi `element_to_be_clickable` | `#message` = *"It's enabled!"*; `input.is_enabled()` = True | Cao |
| TC_DY_04 | Vô hiệu hóa một ô nhập liệu đã được kích hoạt lại | Enable → click "Disable"; đợi `lambda is_enabled == False` | `#message` = *"It's disabled!"*; `input.is_enabled()` = False | Cao |

---

## Feature: Entry Ad (Modal)

> **Tệp:** `test_entry_ad.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_EA_01 | Đóng modal khi xuất hiện lần đầu | Xóa cookie → tải lại → đợi modal → click đóng | Modal trở nên **không hiển thị** (`invisibility_of_element`) | Cao |
| TC_EA_02 | Modal KHÔNG xuất hiện lại sau khi đã đóng (duy trì cookie) | Đóng modal → tải lại với cookie nguyên vẹn; đợi 3 giây thất bại nhanh | Modal vẫn **ẩn** trong lần truy cập tiếp theo | Trung bình |
| TC_EA_03 | Modal xuất hiện lại sau khi xóa sạch cookie | Đóng modal → xóa toàn bộ cookie → tải lại | Modal **hiển thị trở lại** (đặt lại bộ nhớ phiên) | Trung bình |

---
## Module: Exit Intent

> **Tệp:** `tests/test_exit_intent.py`
> **Ghi chú:** Modal chỉ kích hoạt khi chuột rời khỏi khung nhìn trình duyệt (cạnh trên).

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| **TC_EI_01** | **Hiển thị Modal - Happy Path** | Điều hướng tới `/exit_intent` -> Di chuyển chuột ra ngoài khung nhìn (trên). | Modal hiển thị; Tiêu đề = "THIS IS A MODAL WINDOW". | Cao |
| **TC_EI_02** | **Logic Kích hoạt Một lần** | Kích hoạt và đóng modal một lần -> Thử kích hoạt lại lần nữa. | Modal KHÔNG xuất hiện lại; logic chỉ cho phép kích hoạt một lần mỗi phiên. | Cao |
| **TC_EI_03** | **Không Kích hoạt Trong Biên** | Di chuyển chuột sang phải/dưới khung nhìn. | Modal vẫn ẩn; chỉ thoát-phía-trên mới kích hoạt ý định thoát. | Trung bình |
| **TC_EI_04** | **Kiểm tra Chặn Lớp Phủ (Overlay)** | Kích hoạt modal -> Thử click vào liên kết phía sau nó ("Elemental Selenium"). | Click bị chặn/bắt bởi lớp phủ của modal. | Trung bình |
---

## Feature: File Download

> **Tệp:** `test_file_download.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_FD_01 | Xác minh tệp đầu tiên có sẵn được tải xuống thành công | Click liên kết tải xuống đầu tiên; thăm dò `test_downloads/` trong 10 giây | Tệp xuất hiện trên đĩa không có phần mở rộng `.crdownload` (đã tải xong) | Cao |

---

## Feature: File Upload

> **Tệp:** `test_file_upload.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_FU_01 | Tải lên một tệp địa phương hợp lệ và xác nhận thành công | `send_keys(đường_dẫn_tuyệt_đối_tới_tệp)` → click Submit | Trang hiển thị *"File Uploaded!"*; tên tệp đã tải khớp với đầu vào | Cao |
| TC_FU_02 | **Phủ định:** Gửi form mà không chọn tệp nào | Click Submit với trường nhập tệp để trống | Trang điều hướng tới lỗi backend; H1 = *"Internal Server Error"* | Trung bình |

---

## Feature: Floating Menu

> **Tệp:** `test_floating_menu.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_FM_01 | Xác minh menu nổi hiển thị khi tải trang lần đầu | Điều hướng tới trang; tìm `#menu` | Phần tử menu `is_displayed()` = **True** | Trung bình |
| TC_FM_02 | Menu vẫn hiển thị sau khi cuộn mạnh xuống dưới cùng | `window.scrollTo(0, scrollHeight)` qua JS | `#menu` vẫn hiển thị; các liên kết Home và About vẫn thấy được | Cao |
| TC_FM_03 | Click liên kết neo và xác minh điều hướng hash | Click "Home" trong menu nổi | `current_url` chứa `#home` | Trung bình |

---

## Feature: Forgot Password

> **Tệp:** `test_forgot_password.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_FP_01 | Gửi một địa chỉ email hoàn toàn hợp lệ | Dữ liệu: `test_user_valid@example.com` | Trang xác nhận *"Your e-mail's been sent!"* hoặc xử lý endpoint 500 nhẹ nhàng | Cao |
| TC_FP_02 | **Phủ định:** Gửi trường email để trống | Dữ liệu: `""` (chuỗi rỗng) | Hệ thống từ chối; phản hồi chứa *"Internal Server Error"* | Trung bình |
| TC_FP_03 | **Phủ định:** Gửi chuỗi không phải định dạng email | Dữ liệu: `user_without_at_symbol_or_domain` | Hệ thống từ chối hoặc lỗi server; phản hồi được xác thực trạng thái lỗi | Trung bình |

---

## Feature: Form Authentication (Login)

> **Tệp:** `test_form_authentication.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_FA_01 | Happy path: thông tin hợp lệ điều hướng tới vùng an toàn | Username: `tomsmith` / Password: `SuperSecretPassword!` | URL chứa `/secure`; flash = *"You logged into a secure area!"* | NGHIÊM TRỌNG |
| TC_FA_02 | **Phủ định:** Sai mật khẩu | Username: `tomsmith` / Password: `wrongpassword` | Flash = *"Your password is invalid!"* | NGHIÊM TRỌNG |
| TC_FA_03 | **Phủ định:** Sai tên đăng nhập | Username: `wronguser` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | NGHIÊM TRỌNG |
| TC_FA_04 | **Phủ định:** Cả hai trường để trống | Username: `""` / Password: `""` | Flash = *"Your username is invalid!"* | Cao |
| TC_FA_05 | **Phủ định:** Đúng tên đăng nhập, trống mật khẩu | Username: `tomsmith` / Password: `""` | Flash = *"Your password is invalid!"* | Cao |
| TC_FA_06 | **Phủ định:** Trống tên đăng nhập, đúng mật khẩu | Username: `""` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | Cao |
| TC_FA_07 | Đăng xuất sau khi đăng nhập thành công | Login → Click nút logout | Flash = *"You logged out of the secure area!"*; URL = trang login | NGHIÊM TRỌNG |
| TC_FA_08 | **Phủ định:** Kiểm tra tên đăng nhập phân biệt hoa thường | Username: `TomSmith` / Password: `SuperSecretPassword!` | Flash = *"Your username is invalid!"* | Cao |
| TC_FA_09 | **Phủ định:** Kiểm tra mật khẩu phân biệt hoa thường | Username: `tomsmith` / Password: `supersecretpassword!` | Flash = *"Your password is invalid!"* | Cao |
| TC_FA_10 | **Bảo mật:** Ký tự đặc biệt trong tên đăng nhập (fuzzing) | Username: `!@#$%^&*` / Password: `SuperSecretPassword!` | Hệ thống từ chối an toàn; Flash = *"Your username is invalid!"* | NGHIÊM TRỌNG |

---

## Feature: Geolocation

> **Tệp:** `test_geolocation.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_GEO_01 | Tọa độ giả lập CDP đổ vào các trường lat/long | Giả lập CDP: Lat=`21.0285`, Long=`105.8542` (Hà Nội, VN) → Click *"Where am I?"* | `#lat-value` và `#long-value` chứa các con số thực hợp lệ | Cao |
| TC_GEO_02 | Link Google Maps được tạo với vĩ độ giả lập chính xác | Giả lập CDP tương tự → Click nút → kiểm tra `#map-link a[href]` | Href chứa *"google"* và đúng giá trị vĩ độ đã giả lập | Cao |

---

## Feature: Horizontal Slider

> **Tệp:** `test_horizontal_slider.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_HS_01 | Thanh trượt tăng 0.5 sau mỗi lần nhấn ARROW_RIGHT | Click thanh trượt → nhấn `ARROW_RIGHT` hai lần | Giá trị: `0.5` → `1.0` | Trung bình |
| TC_HS_02 | Biên tối đa: thanh trượt không thể vượt quá 5 | Nhấn `ARROW_RIGHT` 15 lần | `#range` = **"5"** (tối đa cứng) | Cao |
| TC_HS_03 | Biên tối thiểu: thanh trượt không thể xuống dưới 0 | Di chuyển sang phải 2× rồi sang trái 3× | `#range` = **"0"** (tối thiểu cứng) | Cao |

---

## Feature: Hovers

> **Tệp:** `test_hovers.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_HV_01 | Di chuột qua hình ảnh người dùng đầu tiên hiện chú thích | `ActionChains.move_to_element(figure[0])` | Chú thích H5 hiển thị **"name: user1"** | Trung bình |
| TC_HV_02 | Di chuột qua hình ảnh người dùng thứ hai hiện chú thích | `ActionChains.move_to_element(figure[1])` | Chú thích H5 hiển thị **"name: user2"** | Trung bình |
| TC_HV_03 | Di chuột qua hình ảnh người dùng thứ ba hiện chú thích | `ActionChains.move_to_element(figure[2])` | Chú thích H5 hiển thị **"name: user3"** | Trung bình |

---

## Module: Frames (Nested & iFrame)

> **Tệp:** `tests/test_frames.py`
> **Ghi chú Kỹ thuật:** Selenium xử lý các frame như các Mô hình Đối tượng Tài liệu (DOM) bị cô lập. Việc chuyển đổi ngữ cảnh (switching) là bắt buộc.
> **Ghi chú Lý thuyết Trò chơi:** Module này kiểm tra **Information Asymmetry** (Sự bất đối xứng thông tin). "Thế giới quan" của trình điều khiển bị giới hạn trong ngữ cảnh frame hiện tại.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| **TC_FR_01** | `test_iframe_happy_path_tc1` – **Happy Path**: Chuyển vào iFrame, tiêm văn bản và xác minh. | `driver.get("/iframe")` → `switch_to.frame("mce_0_ifr")` → `execute_script("innerHTML = '...'")` → `switch_to.default_content()` | Trình soạn thảo chứa văn bản đã tiêm; Driver trở về ngữ cảnh trang chính thành công. | Cao |
| **TC_FR_02** | `test_nested_frames_happy_path_tc2` – **Happy Path**: Duyệt qua toàn bộ 4 frame lồng nhau. | `driver.get("/nested_frames")` → `switch_to.frame("frame-top")` → `switch_to.frame("frame-left/middle/right")` → `switch_to.default_content()` → `switch_to.frame("frame-bottom")` | Mỗi văn bản duy nhất của mỗi frame ("LEFT", "MIDDLE", "RIGHT", "BOTTOM") được xác thực chính xác. | Cao |
| **TC_FR_03** | `test_frame_context_leak_sad_path_tc3` – **Sad Path (Cô lập)**: Thử tìm phần tử trang chính từ bên trong iFrame. | `switch_to.frame("mce_0_ifr")` → `find_element(By.TAG_NAME, "h3")` (Mục tiêu: Tiêu đề trang chính) | `NoSuchElementException` được kích hoạt; chứng minh Driver không thể "nhìn thấy" bên ngoài frame hiện tại. | Trung bình |
| **TC_FR_04** | `test_invalid_frame_access_sad_path_tc4` – **Sad Path (Độ ổn định)**: Thử chuyển sang một ID frame không tồn tại. | `driver.get("/iframe")` → `switch_to.frame("ghost_frame_99")` | `NoSuchFrameException` được bắt; script xử lý mục tiêu không hợp lệ một cách nhẹ nhàng. | Trung bình |
| **TC_FR_05** | `test_sibling_frame_isolation_sad_path_tc5` – **Sad Path (Phân cấp)**: Nhảy trực tiếp từ 'frame-left' sang 'frame-right'. | `switch_to.frame("frame-top")` → `switch_to.frame("frame-left")` → `switch_to.frame("frame-right")` (Trực tiếp) | `NoSuchFrameException` được kích hoạt; chứng minh Driver phải trở lại cha/root trước. | Trung bình |

---

## Feature: Infinite Scroll

> **Tệp:** `test_infinite_scroll.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_IS_01 | Xác minh ít nhất một đoạn nội dung tải mà không cần cuộn | Điều hướng tới trang; đếm các phần tử `.jscroll-added` | Số lượng ≥ **1** trong lần tải đầu tiên | Trung bình |
| TC_IS_02 | Cuộn xuống đáy 3 lần và xác minh các khối nội dung mới được tiêm vào | `window.scrollTo(0, scrollHeight)` × 3; đợi số lượng tăng sau mỗi lần | Số lượng đoạn văn bản cuối cùng > số lượng ban đầu (xác nhận tiêm động) | Cao |

---

## Feature: Number Inputs

> **Tệp:** `test_inputs.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_IN_01 | Chấp nhận các số nguyên dương và âm hợp lệ | `send_keys("500")` sau đó `send_keys("-35")` | Giá trị trường phản ánh chính xác `"500"` sau đó `"-35"` | Trung bình |
| TC_IN_02 | ARROW_UP tăng giá trị lên 1 | Nhập `"10"` → nhấn `ARROW_UP` | Giá trị trường = **"11"** | Trung bình |
| TC_IN_03 | ARROW_DOWN giảm giá trị đi 1 | Nhập `"10"` → nhấn `ARROW_DOWN` | Giá trị trường = **"9"** | Trung bình |
| TC_IN_04 | **Phủ định:** Các ký tự chữ cái bị từ chối bởi `input[type=number]` | `send_keys("abc")` | Giá trị trường = **""** (trình duyệt chặn nhập liệu không phải số) | Trung bình |

---

## Feature: JS Alerts

> **Tệp:** `test_js_alerts.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_JA_01 | Chấp nhận Cảnh báo JS (JS Alert) chuẩn và xác minh kết quả | Click nút Alert → `alert.accept()` | `#result` = *"You successfully clicked an alert"* | Cao |
| TC_JA_02 | Chấp nhận hộp thoại Xác nhận JS (JS Confirmation) | Click nút Confirm → `alert.accept()` | `#result` = *"You clicked: Ok"* | Cao |
| TC_JA_03 | **Phủ định:** Từ chối (Hủy) hộp thoại Xác nhận JS | Click nút Confirm → `alert.dismiss()` | `#result` = *"You clicked: Cancel"* | Trung bình |

---

## Feature: JS Prompt

> **Tệp:** `test_js_prompt.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_JP_01 | **Bảo mật:** Tiêm payload XSS vào prompt JS và xác minh phản chiếu an toàn | Đầu vào: `<script>alert('XSS')</script>` → Chấp nhận | `#result` = *"You entered: \<script\>alert('XSS')\</script\>"* (chuỗi được phản chiếu an toàn, không thực thi) | NGHIÊM TRỌNG |
| TC_JP_02 | **Phủ định:** Đóng prompt mà không nhập liệu | Mở prompt → `alert.dismiss()` | `#result` = *"You entered: null"* | Trung bình |

---

## Module: JavaScript Error

> **Tệp:** `test_javascript_error.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_JE_01 | `test_javascript_error_page_loads_tc1` – Happy Path: Điều hướng tới trang và khẳng định nó tải với tiêu đề `h3` đúng. | `driver.get("/javascript_error")` → `EC.presence_of_element_located((By.TAG_NAME, "h3"))` | `h3.text == "JavaScript Error"`; `is_displayed()` = **True** | Trung bình |
| TC_JE_02 | `test_javascript_error_console_log_tc2` – Độ ổn định: Trích xuất browser console logs via `get_log('browser')` và khẳng định bắt được lỗi JS mức SEVERE. | Điều hướng → `driver.get_log("browser")` → lọc `level == "SEVERE"` | Ít nhất 1 mục log SEVERE; nội dung thông báo chứa `"Cannot read"`, `"not defined"`, hoặc `"TypeError"` | Cao |

---

## Module: JQuery UI Menus

> **Tệp:** `test_jquery_ui_menus.py`
> **Ghi chú:** Việc điều hướng qua các menu lồng nhau yêu cầu `ActionChains` hover — lệnh `.click()` chuẩn không làm lộ các menu con.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_JQ_01 | `test_jquery_menu_hover_pdf_tc1` – Happy Path: Hover Enabled → Downloads → PDF. Khẳng định link PDF thấy được, sau đó click. | Đi tới `/jqueryui/menu` → `ActionChains.move_to_element(Enabled)` → hover `Downloads` → đợi link `PDF` hiện → click | Link PDF hiển thị trong menu con; click thành công | Cao |
| TC_JQ_02 | `test_jquery_menu_hover_excel_tc2` – Happy Path: Hover Enabled → Downloads → Excel. Khẳng định link Excel thấy được, sau đó click. | Hover chain tương tự → đợi link `Excel` hiện → click | Link Excel hiển thị trong menu con; click thành công | Cao |
| TC_JQ_03 | `test_jquery_menu_disabled_not_clickable_tc3` – Sad Path: Click vào mục 'Disabled'. Khẳng định URL không đổi (điều hướng bị chặn). | Tìm `li.ui-state-disabled a` → khẳng định class → click → so sánh `current_url` trước/sau | `url_trước == url_sau`; mục vô hiệu hóa không kích hoạt điều hướng | Trung bình |
| TC_JQ_04 | `test_jquery_menu_disabled_no_submenu_tc4` – Sad Path: Hover qua mục 'Disabled'. Khẳng định không có menu con hiện ra trong 2 giây. | Hover `li.ui-state-disabled a` → `WebDriverWait(2).until(EC.visibility_of_element_located(sub-menu))` | Bắt được `TimeoutException` — không có menu con nào hiện ra cho mục vô hiệu hóa | Trung bình |

---

## Feature: Key Presses

> **Tệp:** `test_key_presses.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_KP_01 | Các phím chức năng đặc biệt được phát hiện và đặt tên chính xác | Payloads: `SPACE`, `ENTER`, `TAB`, `ESCAPE`, `BACKSPACE`, `ALT` | Mỗi `#result` khớp với tên phím viết hoa kỳ vọng (ví dụ: *"You entered: SPACE"*) | Cao |
| TC_KP_02 | Các phím chữ và số được phản chiếu với ánh xạ nhãn/viết hoa đúng | Payloads: `"a"→A`, `"Z"→Z`, `"7"→7`, `"@"→COMMERCIAL_AT` | Mỗi `#result` ánh xạ chính xác đến nhãn viết hoa kỳ vọng | Trung bình |

---

## Module: Large & Deep DOM

> **Tệp:** `test_large_deep_dom.py`
> **Ghi chú:** Trang tạo ra một lưới 50×50 gồm các phần tử `<div>` với ID định dạng `large-{row}-{col}`. BVA nhắm vào ô biên `large-50-50`.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_LD_01 | `test_large_dom_deep_sibling_tc1` – Happy Path: Tìm một phần tử nằm sâu cụ thể bằng ID (`large-2-5`) và xác minh văn bản. | Đi tới `/large` → `EC.presence_of_element_located((By.ID, "large-2-5"))` → đọc `.text` | Tìm thấy phần tử; văn bản **chứa** `"2.5"` | Cao |
| TC_LD_02 | `test_large_dom_boundary_cell_tc2` – Happy Path (BVA Max): Tìm ô biên `large-50-50` và xác minh văn bản. | `EC.presence_of_element_located((By.ID, "large-50-50"))` → đọc `.text` | Tìm thấy phần tử; văn bản **chứa** `"50.50"` | Cao |
| TC_LD_03 | `test_large_dom_invalid_id_sad_path_tc3` – Sad Path: Thử tìm một phần tử không tồn tại `#large-999-999`. Khẳng định thất bại nhẹ nhàng. | `WebDriverWait(2).until(EC.presence_of_element_located((By.ID, "large-999-999")))` | Bắt được `TimeoutException` — phần tử vắng mặt chính xác | Trung bình |
| TC_LD_04 | `test_large_dom_invalid_xpath_sad_path_tc4` – Sad Path: Thử tìm một ô sâu qua XPath không hợp lệ (cột 51 ngoài lưới). Khẳng định thất bại nhẹ nhàng. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//div[@id='large-0-0']//td[51]")))` | Bắt được `TimeoutException` — mục tiêu XPath vắng mặt chính xác | Trung bình |

---

## Module: Notification Messages

> **Tệp:** `test_notification_messages.py`
> **Ghi chú:** Các tin nhắn Flash được chọn ngẫu nhiên. Dùng `assertIn(flash_text, VALID_MESSAGES)` để ngăn các test lỗi không ổn định. Các tin nhắn hợp lệ: `"Action successful"`, `"Action unsuccessful, please try again"`.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_NM_01 | `test_notification_single_click_ep_tc1` – Happy Path: Click 'Click here' một lần và khẳng định tin nhắn flash nằm trong list hợp lệ. | Điều hướng tới `/notification_message` → click link → đợi `#flash` | `flash.text` **nằm trong** `VALID_MESSAGES` | Cao |
| TC_NM_02 | `test_notification_multi_click_ep_tc2` – Happy Path: Click link 5 lần; mỗi phản hồi phải là một tin nhắn hợp lệ. | Lặp 5 lần: điều hướng → click → xác minh văn bản `#flash` | Tất cả 5 tin nhắn flash đều **trong** `VALID_MESSAGES` | Trung bình |
| TC_NM_03 | `test_notification_no_unexpected_message_tc3` – Sad Path: Khẳng định flash không bao giờ rỗng và không bao giờ chứa từ "error". | Click một lần → đọc `#flash` → `assertNotIn("error", text.lower())` | Flash không rỗng; **không** chứa từ `"error"` | Trung bình |
| TC_NM_04 | `test_notification_direct_render_robustness_tc4` – Độ ổn định: Điều hướng trực tiếp tới `/notification_message_rendered`. Khẳng định một flash hợp lệ được hiển thị. | `driver.get("/notification_message_rendered")` → đợi `#flash` | Văn bản Flash **nằm trong** `VALID_MESSAGES` khi kết xuất trực tiếp | Trung bình |

---

## Module: Redirect Link

> **Tệp:** `test_redirect_link.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_RL_01 | `test_redirect_link_url_change_tc1` – Happy Path: Click link chuyển hướng và khẳng định URL đổi sang đích Status Codes. | Đi tới `/redirector` → click `a[href='redirect']` → `EC.url_contains("status_codes")` | `current_url` đổi thành `https://the-internet.herokuapp.com/status_codes` | Cao |
| TC_RL_02 | `test_redirect_link_destination_content_tc2` – Happy Path: Theo dõi chuyển hướng và xác minh tiêu đề trang đích. | Điều hướng → click link chuyển hướng → đợi `h3` tại đích | `h3.text` **chứa** `"Status Codes"` | Cao |
| TC_RL_03 | `test_redirect_invalid_endpoint_tc3` – Sad Path: Điều hướng trực tiếp tới một endpoint chuyển hướng không tồn tại. Khẳng định không thấy trang Status Codes. | `driver.get("/redirect/nonexistent_page_404")` → đọc `body.text` | Body KHÔNG chứa `"Status Codes"`; đường dẫn không hợp lệ được xử lý | Trung bình |
| TC_RL_04 | `test_redirect_link_absent_on_wrong_page_tc4` – Sad Path: Xác nhận liên kết chuyển hướng vắng mặt trên trang đích (chuyển hướng một chiều). | Đi tới `/status_codes` → `WebDriverWait(2).until(EC.presence_of_element_located(a[href='redirect']))` | Bắt được `TimeoutException` — link chuyển hướng vắng mặt chính xác trên đích | Trung bình |

---

## Module: Shadow DOM

> **Tệp:** `test_shadow_dom.py`
> **Ghi chú:** Shadow DOM tạo ra các cây DOM con được đóng gói. XPath chuẩn từ root document **không thể** xuyên qua ranh giới shadow. Truy cập yêu cầu thuộc tính `.shadow_root` của Selenium 4 hoặc JavaScript `element.shadowRoot.querySelector()`.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_SD_01 | `test_shadow_dom_access_via_shadow_root_tc1` – Happy Path: Truy cập shadow host `my-paragraph` qua Selenium 4 `.shadow_root`, sau đó tìm `<p>` bên trong và xác minh văn bản. | Đi tới `/shadowdom` → `EC.presence_of_element_located((By.CSS_SELECTOR, "my-paragraph"))` → `.shadow_root` → `.find_element(By.CSS_SELECTOR, "p")` | `<p>` bên trong có thể truy cập; văn bản không rỗng và chứa `"shadow"` | Cao |
| TC_SD_02 | `test_shadow_dom_access_via_js_tc2` – Happy Path: Xuyên qua shadow root via `execute_script("element.shadowRoot.querySelector('p')")`. Khẳng định nội dung được trả về. | Điều hướng → JS: `document.querySelector('my-paragraph').shadowRoot.querySelector('p').textContent` | Trả về văn bản không null, không rỗng từ bên trong shadow root | Cao |
| TC_SD_03 | `test_shadow_dom_xpath_cannot_pierce_tc3` – Sad Path: Thử dùng XPath `//my-paragraph//p` chuẩn từ root document (không thể xuyên qua ranh giới shadow). Khẳng định thất bại. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//my-paragraph//p[...]")))` | `TimeoutException` hoặc `NoSuchElementException` — XPath chính xác bị chặn bởi sự đóng gói shadow | Trung bình |

---

## Feature: Shifting Content

> **Tệp:** `test_shifting_content.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_SC_01 | Xác minh tọa độ pixel của phần tử menu dịch chuyển một cách xác định giữa URL gốc và URL ép-buộc-dịch-chuyển | Tải URL gốc → chụp `location`; tải `?mode=random&pixel_shift=100` → chụp lại | Độ lệch tuyệt đối ở X hoặc Y > **10 pixels** | Trung bình |

---

## Module: Slow Resources

> **Tệp:** `test_slow_resources.py`
> **Ghi chú:** Trang Slow Resources cố tình trì hoãn việc tải trang. Các mốc thời gian chờ BVA (0s, 1s) được dùng để xác minh `TimeoutException` được kích hoạt và bắt nhẹ nhàng.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_SR_01 | `test_slow_resources_full_load_tc1` – Happy Path: Điều hướng tới Slow Resources và chờ hào phóng (30s) cho tiêu đề trang xuất hiện. | `driver.get("/slow")` → `WebDriverWait(30).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | Tiêu đề hiển thị; văn bản không rỗng | Cao |
| TC_SR_02 | `test_slow_resources_short_timeout_bva_tc2` – Sad Path (BVA): Dùng thời gian chờ 1s sau khi điều hướng. Khẳng định `TimeoutException` được bắt — trang không thể tải nhanh thế. | Điều hướng → `WebDriverWait(1).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | Bắt được `TimeoutException`; gọi `self.fail()` nếu phần tử xuất hiện trong vòng 1s | Cao |
| TC_SR_03 | `test_slow_resources_zero_timeout_boundary_tc3` – Sad Path (BVA Min): Dùng thời gian chờ 0s — biên tối thiểu tuyệt đối phải luôn hết hạn ngay lập tức. | Điều hướng → `WebDriverWait(0).until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))` | Bắt được `TimeoutException` ngay lập tức; biên 0s luôn thất bại cho trang chậm | Trung bình |

---

## Module: Sortable Data Tables

> **Tệp:** `test_sortable_data_tables.py`
> **Ghi chú:** Dữ liệu bảng được trích xuất vào các danh sách Python và so sánh với `sorted()` để khẳng định thứ tự sắp xếp cột.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_ST_01 | `test_sortable_tables_sort_lastname_asc_tc1` – Happy Path: Click tiêu đề 'Last Name' một lần để sắp xếp tăng dần. Trích xuất cột, so sánh với `sorted(actual)`. | Đi tới `/tables` → `table1 th[Last Name]`.click() → trích xuất giá trị cột 1 | `actual == sorted(actual)` — Last Name được sắp xếp theo bảng chữ cái tăng dần | Cao |
| TC_ST_02 | `test_sortable_tables_sort_lastname_desc_tc2` – Happy Path: Click đúp tiêu đề 'Last Name' để sắp xếp giảm dần. So sánh với `sorted(actual, reverse=True)`. | Click `th[Last Name]` hai lần → trích xuất giá trị cột 1 | `actual == sorted(actual, reverse=True)` — Last Name được sắp xếp giảm dần | Cao |
| TC_ST_03 | `test_sortable_tables_unsortable_column_tc3` – Sad Path: Cột Email của Bảng 2 không có chỉ báo sắp xếp `<span>`. Khẳng định `TimeoutException` khi tìm kiếm nó. | `WebDriverWait(2).until(EC.presence_of_element_located((By.XPATH, "//table[@id='table2']//th[span[text()='Email']]")))` | Bắt được `TimeoutException` — cột không thể sắp xếp không có điều khiển sắp xếp | Trung bình |
| TC_ST_04 | `test_sortable_tables_out_of_bounds_column_tc4` – Sad Path: Trích xuất chỉ số cột 99 (vượt ngoài phạm vi bảng). Khẳng định trả về danh sách rỗng nhẹ nhàng. | `_get_column_values("table1", col_index=99)` dùng XPath `td[99]` | Trả về danh sách rỗng `[]` — chỉ số cột ngoài phạm vi không mang lại phần tử nào | Trung bình |

---

## Feature: Status Codes

> **Tệp:** `test_status_codes.py`

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ/Ưu tiên |
| :--- | :--- | :--- | :--- | :--- |
| TC_SC_01 | Xác minh điều hướng 200 OK và tin nhắn phản hồi | Click link "200" | Văn bản trang chứa: *"This page returned a 200 status code."* | Cao |
| TC_SC_02 | Xác minh điều hướng 301 Moved Permanently | Click link "301" | Văn bản trang chứa: *"This page returned a 301 status code."* | Cao |
| TC_SC_03 | Xác minh điều hướng 404 Not Found | Click link "404" | Văn bản trang chứa: *"This page returned a 404 status code."* | Cao |
| TC_SC_04 | Xác minh điều hướng 500 Internal Server Error | Click link "500" | Văn bản trang chứa: *"This page returned a 500 status code."* | Cao |

---

## Module: Typos

> **Tệp:** `test_typos.py`
> **Ghi chú:** Trang này phục vụ ngẫu nhiên hai biến thể A/B: một biến thể đúng `"won't"` và một có lỗi `"won,t"`. Các test phải xử lý đầu ra ngẫu nhiên bằng vòng lặp tải lại và phân loại kết quả.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_TY_01 | `test_typos_refresh_until_correct_tc1` – Happy Path: Tải lại trang tối đa 10 lần cho đến khi văn bản đúng `"won't"` xuất hiện. Khẳng định nó cuối cùng sẽ được phục vụ. | `for i in range(10): driver.get(URL)` → đọc `<p>` thứ hai → ngắt nếu thấy `"won't"` | Văn bản đúng xuất hiện trong vòng 10 lần tải lại; `found_correct == True` | Trung bình |
| TC_TY_02 | `test_typos_detect_known_typo_tc2` – Phát hiện lỗi A/B: Trong một lần chạy, phân loại và log biến thể. Nếu `"won,t"` xuất hiện, log lỗi A/B; nếu `"won't"`, log là đúng. | Lặp cho đến khi tìm thấy một trong hai biến thể → log `"⚠ A/B BUG DETECTED"` hoặc `"Correct variant"` tương ứng | Cả hai biến thể được phân loại và log chính xác; test vượt qua trong cả hai trường hợp (đây là test phát hiện) | Cao |
| TC_TY_03 | `test_typos_page_structure_robustness_tc3` – Độ ổn định: Khẳng định trang luôn có chính xác 2 phần tử `<p>` bất kể biến thể A/B nào. | `driver.get(URL)` → `EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example p"))` | `len(paragraphs) == 2`; văn bản đoạn thứ hai khớp với một trong hai chuỗi biến thể đã biết | Trung bình |

---

## Module: WYSIWYG Editor (TinyMCE)

> **Tệp:** `test_wysiwyg_editor.py`
> **Thách thức Kỹ thuật:** Trình soạn thảo TinyMCE có thể hiển thị lớp phủ `"TinyMCE is in read-only mode"` khi giới hạn API key bị chạm. Lệnh `send_keys()` bị chặn. Cách xử lý là dùng `execute_script("arguments[0].innerHTML = '...';")` để tiêm nội dung trực tiếp vào body `#tinymce` bên trong iframe. Toolbar nằm ở **tài liệu chính**, không phải trong iframe.

| Mã Ca Kiểm Thử | Mô tả Kịch bản | Dữ liệu Đầu vào / Hành động | Kết quả Mong đợi | Mức độ |
| :--- | :--- | :--- | :--- | :--- |
| TC_WY_01 | `test_wysiwyg_js_injection_happy_path_tc1` – Happy Path: Chuyển sang iframe `mce_0_ifr`, tiêm văn bản qua `execute_script("arguments[0].innerHTML = arguments[1]", body, "<p>...</p>")`, sau đó đọc lại innerHTML và xác minh. | `frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr"))` → `find_element(By.ID, "tinymce")` → `execute_script(...)` → đọc lại `innerHTML` | `INJECT_TEXT` được tìm thấy trong `innerHTML` trả về; việc tiêm mã vượt qua được lớp chặn read-only | NGHIÊM TRỌNG |
| TC_WY_02 | `test_wysiwyg_readonly_alert_sad_path_tc2` – Sad/Độ ổn định: Phát hiện lớp phủ cảnh báo read-only `.tox-notification--warning` trong tài liệu chính (đợi 5 giây). Khẳng định nó hiển thị nếu có; log thoát sạch nếu không. | Điều hướng → `WebDriverWait(5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tox-notification--warning")))` | Lớp phủ được phát hiện và `is_displayed()` = True; HOẶC bắt được `TimeoutException` nhẹ nhàng (chưa chạm giới hạn API) | Cao |
| TC_WY_03 | `test_wysiwyg_toolbar_visibility_happy_path_tc3` – Happy Path: Trong ngữ cảnh **tài liệu chính**, tìm và khẳng định các nút Bold và Italic trên toolbar hiển thị rõ ràng. | Đợi `.tox-toolbar__primary` → `find_element(By.XPATH, "//button[@aria-label='Bold']")` → `find_element(By.XPATH, "//button[@aria-label='Italic']")` | Cả hai nút `is_displayed()` = **True** trong tài liệu chính | Cao |
| TC_WY_04 | `test_wysiwyg_context_isolation_sad_path_tc4` – Sad Path: Sau khi chuyển vào iframe, thử `find_element` cho nút Bold trên toolbar. Khẳng định `NoSuchElementException` (toolbar ở trang chính, không phải trong iframe). | `switch_to.frame("mce_0_ifr")` → `find_element(By.XPATH, "//button[@aria-label='Bold']")` | `NoSuchElementException` được kích hoạt — xác nhận việc cô lập ngữ cảnh; không thấy toolbar từ bên trong iframe | Trung bình |

---

## Phụ lục: Tham chiếu Tiền tố Mã Test

| Tiền tố | Tính năng / Feature |
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
