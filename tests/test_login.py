import sys
import os
import time
import unittest

# Đảm bảo đường dẫn gốc của project luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from base.base_test import BaseTest

class TestLogin(BaseTest):
    """
    Bộ 20 ca kiểm thử tự động cho chức năng Đăng nhập Văn phòng điện tử UTC
    Kế thừa từ BaseTest (quản lý vòng đời WebDriver tự động).
    Khớp chính xác với file kịch bản TestCases_VanPhongDienTu_UTC.xlsx
    """

    # =========================================================================
    # NHÓM 1: KIỂM THỬ CHỨC NĂNG CƠ BẢN (TC01 - TC07)
    # =========================================================================

    def test_tc01_empty_username(self):
        """TC01: Để trống Tên đăng nhập (chỉ nhập Mật khẩu)"""
        self.login_page.enter_password("1256")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC01_empty_username.png")
        self.assertIn("Bạn chưa nhập tên đăng nhập", error_msg, 
                      f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc02_empty_password(self):
        """TC02: Để trống Mật khẩu (chỉ nhập Tên đăng nhập)"""
        self.login_page.enter_username("huongnt")
        self.login_page.click_login()
        
        error_msg = self.login_page.get_error_message()
        self.login_page.capture_screenshot("TC02_empty_password.png")
        self.assertIn("Bạn chưa nhập mật khẩu", error_msg,
                      f"Thông báo lỗi không đúng kỳ vọng. Nhận được: '{error_msg}'")

    def test_tc03_correct_user_wrong_pass(self):

if __name__ == '__main__':
    unittest.main()
