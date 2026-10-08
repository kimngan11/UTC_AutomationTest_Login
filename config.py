import os

# Cấu hình hệ thống kiểm thử tự động
BASE_URL = "https://vanphongdientu.utc.edu.vn/Login"
FORGOT_PASS_URL = "https://vanphongdientu.utc.edu.vn/Login/GetPass"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "TestCases_VanPhongDienTu_UTC.xlsx")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

# Chế độ chạy trình duyệt: False để hiển thị Chrome trực quan, True để chạy ngầm
HEADLESS = False

# Thời gian chờ (giây)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 25

# -----------------------------------------------------------------------------
# TÀI KHOẢN ĐĂNG NHẬP CHO TC05 VÀ TC06 (POSITIVE TESTS)
# Mặc định là tài khoản giả định trong đề bài: 'huongnt' / '123456@utc'
# LƯU Ý: Do hệ thống vanphongdientu.utc.edu.vn là hệ thống THẬT của trường,
# nếu tài khoản này không có trong CSDL thật của trường thì web sẽ báo:
# "Tài khoản hoặc mật khẩu không đúng." -> TC05/TC06 sẽ trả về FAIL (chính xác với thực tế).
# Nếu bạn có tài khoản thật, hãy điền vào bên dưới để test thành công vào trang chủ.
# -----------------------------------------------------------------------------
VALID_USERNAME = "huongnt"
VALID_PASSWORD = "123456@utc"
