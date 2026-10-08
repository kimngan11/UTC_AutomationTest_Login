# Automation Test Hệ Thống Văn Phòng Điện Tử UTC

Dự án kiểm thử tự động (Automation Testing) toàn diện cho phân hệ Đăng nhập của **Hệ thống Văn phòng điện tử - Trường Đại học Giao thông Vận tải**.
- **URL kiểm thử:** [https://vanphongdientu.utc.edu.vn/Login](https://vanphongdientu.utc.edu.vn/Login)
- **Mô hình kiến trúc:** Page Object Model (POM) kết hợp BasePage & BaseTest chuẩn công nghiệp
- **Công nghệ sử dụng:** Python 3, Selenium WebDriver, OpenPyXL, Pytest / Unittest.
- **Tài liệu kịch bản & Báo cáo:** [TestCases_VanPhongDienTu_UTC.xlsx](TestCases_VanPhongDienTu_UTC.xlsx)

---

## 1. Cấu trúc thư mục dự án chuẩn hóa

```text
AutomationTest/
├── base/
│   ├── __init__.py
│   └── base_test.py                    # Lớp cha BaseTest kế thừa unittest.TestCase (quản lý WebDriver)
├── pages/
│   ├── __init__.py
│   ├── base_page.py                    # Lớp cha BasePage đóng gói các thao tác Selenium dùng chung
│   └── login_page.py                   # Lớp LoginPage kế thừa BasePage (chứa locators & nghiệp vụ Login UTC)
├── tests/
│   ├── __init__.py
│   └── test_login.py                   # Bộ 20 Test Cases kế thừa BaseTest theo chuẩn unittest/pytest
├── screenshots/                        # Thư mục lưu 20 ảnh chụp màn hình minh chứng
│   ├── TC01_empty_username.png
│   ├── ...
│   └── TC20_footer_links.png
├── config.py                           # Cấu hình URL, thời gian chờ, tài khoản kiểm thử
├── requirements.txt                    # Danh sách thư viện cần thiết
├── run_tests.py                        # Script thực thi toàn bộ kiểm thử và tự cập nhật Excel
└── TestCases_VanPhongDienTu_UTC.xlsx   # File Excel kịch bản & báo cáo tổng quan kiểm thử
```

---

## 2. Chi tiết phân chia trách nhiệm các lớp (OOP & POM)

- **`pages/base_page.py` (`BasePage`)**:
  - Đóng gói các hàm tiện ích Selenium WebDriver: `open_url()`, `find_element()`, `enter_text()`, `click()`, `get_text()`, `get_attribute()`, `execute_script()`, `capture_screenshot()`, v.v.
- **`pages/login_page.py` (`LoginPage`)**:
  - Kế thừa `BasePage`.
  - Khai báo Locators trang Đăng nhập UTC và các hàm nghiệp vụ riêng của trang: `enter_username()`, `enter_password()`, `set_remember_me()`, `click_login()`, `get_error_message()`, `is_password_masked()`, `navigate_with_tab_key()`, v.v.
- **`base/base_test.py` (`BaseTest`)**:
  - Kế thừa `unittest.TestCase`.
  - Quản lý vòng đời khởi tạo và dọn dẹp trình duyệt: `setUpClass()` mở Chrome, `tearDownClass()` đóng Chrome, `setUp()` khởi tạo `self.login_page = LoginPage(self.driver)` và mở trang trước mỗi test.
- **`tests/test_login.py` (`TestLogin`)**:
  - Kế thừa `BaseTest`.
  - Triển khai 20 Test Cases từ `test_tc01` đến `test_tc20` ngắn gọn, rõ ràng, không lặp lại code cấu hình WebDriver.

---

## 3. Bảng ma trận 20 Test Cases bao quát toàn diện Login

| STT | Mã TC | Phân nhóm kiểm thử | Tên kịch bản kiểm thử | Dữ liệu kiểm thử | Kết quả mong đợi |
|:---:|:---:|:---|:---|:---|:---|
| 1 | **TC01** | Negative | Để trống Tên đăng nhập (chỉ nhập Mật khẩu) | User: `[Trống]`, Pass: `1256` | Báo lỗi: *"Bạn chưa nhập tên đăng nhập"* |
| 2 | **TC02** | Negative | Để trống Mật khẩu (chỉ nhập Tên đăng nhập) | User: `huongnt`, Pass: `[Trống]` | Báo lỗi: *"Bạn chưa nhập mật khẩu"* |
| 3 | **TC03** | Negative | Đúng định dạng User, sai Mật khẩu | User: `huongnt`, Pass: `utc@235` | Báo lỗi: *"Tài khoản hoặc mật khẩu không đúng."* |
| 4 | **TC04** | Negative | Sai Tên đăng nhập, đúng định dạng Mật khẩu | User: `huongthunguyen`, Pass: `123456@utc` | Báo lỗi: *"Tài khoản hoặc mật khẩu không đúng."* |
| 5 | **TC05** | Positive | Đăng nhập có chọn "Giữ tôi luôn đăng nhập" | User: `huongnt`, Pass: `123456@utc`, Checkbox: `Checked` | Đăng nhập thành công vào trang chủ |
| 6 | **TC06** | Positive | Đăng nhập không chọn "Giữ tôi luôn đăng nhập" | User: `huongnt`, Pass: `123456@utc`, Checkbox: `Unchecked` | Đăng nhập thành công vào trang chủ |
| 7 | **TC07** | Negative | Để trống cả Tên đăng nhập và Mật khẩu | User: `[Trống]`, Pass: `[Trống]` | Báo lỗi: *"Bạn chưa nhập tên đăng nhập"* |
| 8 | **TC08** | UI & Security | Kiểm tra tính năng ẩn mật khẩu (Masked) | Input: `Abc@123456` | Thuộc tính `type='password'`, ký tự dạng `•` / `*` |
| 9 | **TC09** | Liên kết SSO | Kiểm tra liên kết "Đăng nhập bằng e-mail UTC" | Click liên kết | Trỏ tới SSO Google OAuth UTC (`accounts.google.com`) |
| 10 | **TC10** | Liên kết chức năng | Kiểm tra liên kết "Bạn quên mật khẩu đăng nhập ?" | Click liên kết | Chuyển hướng tới `/Login/GetPass` (*Lấy lại mật khẩu*) |
| 11 | **TC11** | Bàn phím | Đăng nhập bằng cách nhấn phím Enter từ bàn phím | Pass: `1256` + phím `Enter` | Gửi form thành công và kiểm tra validate đầu vào |
| 12 | **TC12** | Khoảng trắng | Tên đăng nhập chỉ chứa toàn khoảng trắng | User: `"   "`, Pass: `123456` | Hệ thống từ chối khoảng trắng và báo lỗi |
| 13 | **TC13** | Khoảng trắng | Mật khẩu chỉ chứa toàn khoảng trắng | User: `huongnt`, Pass: `"   "` | Hệ thống từ chối khoảng trắng và báo lỗi |
| 14 | **TC14** | Bảo mật SQLi | Kiểm tra chống tấn công SQL Injection cơ bản | User: `' OR '1'='1`, Pass: `123456` | Hệ thống an toàn (không crash/lỗi 500), từ chối an toàn |
| 15 | **TC15** | Bảo mật XSS | Kiểm tra chống tấn công XSS Script Injection | User: `<script>alert(1)</script>`, Pass: `123456` | Không thực thi script, xử lý chuỗi an toàn |
| 16 | **TC16** | Giá trị biên | Tên đăng nhập độ dài cực đại (300 ký tự) | User: Chuỗi 300 ký tự, Pass: `123456` | Hệ thống không tràn bộ nhớ/vỡ layout, báo lỗi an toàn |
| 17 | **TC17** | Ký tự đặc biệt | Tên đăng nhập chứa ký tự đặc biệt | User: `admin!@#$%^&*()`, Pass: `123456` | Xử lý an toàn và từ chối tài khoản không tồn tại |
| 18 | **TC18** | Giao diện UI | Kiểm tra văn bản gợi ý mờ (Placeholder) | Kiểm tra `placeholder` | Hiển thị đúng: *"Tên đăng nhập"* & *"Mật khẩu"* |
| 19 | **TC19** | Phím Tab | Kiểm tra điều hướng con trỏ bằng phím `Tab` | Phím `Tab` từ ô username | Con trỏ nhảy chính xác sang ô Mật khẩu (`userpwd`) |
| 20 | **TC20** | Liên kết Footer | Kiểm tra tính đúng đắn của liên kết chân trang | Kiểm tra thuộc tính `href` | Link "Trung tâm trợ giúp" và mailto "Ý kiến phản hồi" |

*Lưu ý về TC05 & TC06:* Nếu dùng tài khoản mẫu `huongnt`/`123456@utc`, web trường sẽ báo sai tài khoản (đúng với thực tế do CSDL trường không có tài khoản này). Bạn có thể cấu hình tài khoản thật trong `config.py` để test thành công.

---

## 4. Hướng dẫn chạy kiểm thử

### Cách 1: Chạy bằng `run_tests.py` (Khuyên dùng)
Tự động chạy, in báo cáo tiếng Việt trực quan, chụp ảnh màn hình và cập nhật kết quả vào Excel:
```powershell
# Chạy trực quan có trình duyệt Chrome mở lên:
python run_tests.py

# Chạy chế độ ngầm (Headless):
python run_tests.py --headless
```

### Cách 2: Chạy trực tiếp qua `unittest` hoặc `pytest`
```powershell
# Chạy bằng unittest:
python -m unittest tests/test_login.py -v

# Chạy bằng pytest:
pytest tests/test_login.py -v
```
