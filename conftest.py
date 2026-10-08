import os
import sys
import pytest
import config

# Đảm bảo thư mục gốc dự án luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Hook chạy trước khi bắt đầu toàn bộ suite kiểm thử:
    Tự động chuẩn bị cấu hình môi trường (environment.properties) và phân loại lỗi (categories.json) cho Allure Report.
    """
    results_dir = os.path.join(config.BASE_DIR, "allure-results")
    os.makedirs(results_dir, exist_ok=True)

    # 1. Ghi thông tin môi trường thực thi (Environment widget trong Allure Dashboard)
    env_file = os.path.join(results_dir, "environment.properties")
    try:
        import platform
        import selenium
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("Application.Name=He Thong Van Phong Dien Tu UTC\n")
            f.write(f"Base.URL={config.BASE_URL}\n")
            f.write("Browser=Google Chrome\n")
            f.write(f"Headless={'True' if config.HEADLESS else 'False'}\n")
            f.write(f"Operating.System={platform.system()} {platform.release()}\n")
            f.write(f"Python.Version={platform.python_version()}\n")
            f.write(f"Selenium.Version={selenium.__version__}\n")
            f.write(f"Pytest.Version={pytest.__version__}\n")
            f.write("Framework=Page Object Model (POM) + Allure Report\n")
    except Exception as e:
        print(f"[Warning] Khong the ghi environment.properties: {e}")

    # 2. Ghi cấu hình phân loại lỗi thông minh (Categories tab trong Allure Dashboard)
    categories_file = os.path.join(results_dir, "categories.json")
    categories_content = """[
  {
    "name": "Lỗi xác thực & Nghiệp vụ (Product / Validation Defect)",
    "matchedStatuses": ["failed"]
  },
  {
    "name": "Lỗi hạ tầng / Timeout / Ngoại lệ (Test Defects)",
    "matchedStatuses": ["broken"]
  },
  {
    "name": "Kịch bản bỏ qua (Skipped Tests)",
    "matchedStatuses": ["skipped"]
  }
]"""
    try:
        with open(categories_file, "w", encoding="utf-8") as f:
            f.write(categories_content)
    except Exception as e:
        print(f"[Warning] Khong the ghi categories.json: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook lắng nghe kết quả từng test case:
    Nếu test case thất bại (Failure), tự động chụp ảnh màn hình và đính kèm trực tiếp vào Allure Report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Nếu test case kế thừa từ BaseTest có chứa driver
        test_instance = getattr(item, "instance", None)
        if test_instance and hasattr(test_instance, "driver"):
            driver = getattr(test_instance, "driver", None)
            if driver:
                try:
                    import allure
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"FAILURE_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception:
                    pass
