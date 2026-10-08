import sys
import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Đảm bảo đường dẫn gốc của project luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from pages.login_page import LoginPage

class BaseTest(unittest.TestCase):
    """
    Lớp cha BaseTest kế thừa unittest.TestCase, đóng gói:
    - Quản lý vòng đời khởi tạo và hủy WebDriver (setUpClass, tearDownClass)
    - Chuẩn bị trạng thái trang trước mỗi kịch bản test (setUp)
    """

    driver = None
    login_page = None

    @classmethod
    def setUpClass(cls):
        """Khởi tạo trình duyệt một lần duy nhất cho toàn bộ test suite"""
        chrome_options = Options()
        if config.HEADLESS:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-notifications")
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(config.IMPLICIT_WAIT)

    @classmethod
    def tearDownClass(cls):
        """Đóng hoàn toàn trình duyệt sau khi kiểm thử xong"""
        if cls.driver:
            cls.driver.quit()

    def setUp(self):
        """Khởi tạo Page Object và mở trang đăng nhập trước mỗi Test Case"""
        self.login_page = LoginPage(self.driver)
        self.login_page.open()
        time.sleep(1)
