import os
import sys
import shutil
import subprocess
import argparse

# Đảm bảo UTF-8 cho console Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
REPORT_DIR = os.path.join(BASE_DIR, "allure-report")

IS_WINDOWS = sys.platform.startswith("win")

def get_allure_command():
    """Xác định đường dẫn chính xác của file thực thi Allure CLI trên hệ thống"""
    # 1. Thử tìm qua PATH
    allure_path = shutil.which("allure") or shutil.which("allure.cmd")
    if allure_path:
        return allure_path

    # 2. Thử tìm qua thư mục global npm trên Windows
    if IS_WINDOWS:
        npm_allure = os.path.expandvars(r"%APPDATA%\npm\allure.cmd")
        if os.path.exists(npm_allure):
            return npm_allure

    return "allure"

def check_allure_cli():
    """Kiểm tra Allure CLI đã được cài đặt trên hệ thống hay chưa"""
    cmd = get_allure_command()
    try:
        res = subprocess.run([cmd, "--version"], shell=IS_WINDOWS, capture_output=True, text=True, check=True)
        return True, res.stdout.strip(), cmd
    except Exception:
        return False, None, cmd

def main():
    parser = argparse.ArgumentParser(description="Trình thực thi kiểm thử và tạo báo cáo Allure Report tự động")
    parser.add_argument("--headless", action="store_true", help="Chạy kiểm thử với trình duyệt Chrome ẩn (Headless)")
    parser.add_argument("--clean", action="store_true", default=True, help="Dọn dẹp kết quả kiểm thử cũ trước khi chạy (mặc định: True)")
    parser.add_argument("-k", "--filter", type=str, default="", help="Chỉ chạy test case chỉ định (ví dụ: -k test_tc01)")
    parser.add_argument("--serve", action="store_true", help="Khởi động Allure Web Server và tự động mở trình duyệt (allure serve)")
    parser.add_argument("--no-open", action="store_true", help="Chỉ tạo báo cáo HTML tĩnh, không tự động mở trình duyệt")
    args = parser.parse_args()

    print("=" * 80)
    print(" KHỞI ĐỘNG CHƯƠNG TRÌNH KIỂM THỬ VÀ XUẤT ALLURE REPORT ")
    print("=" * 80)

    # 1. Kiểm tra Allure CLI
    has_cli, version, allure_cmd = check_allure_cli()
    if has_cli:
        print(f"[✓] Đã tìm thấy Allure Command-line phiên bản: {version} ({allure_cmd})")
    else:
        print("[!] Không tìm thấy lệnh 'allure' trong PATH.")
        print("    Bạn có thể cài đặt bằng lệnh: npm install -g allure-commandline")
        print("    Hoặc: choco install allure-commandline / scoop install allure")

    # 2. Dọn dẹp thư mục kết quả cũ nếu được yêu cầu
    if args.clean and os.path.exists(RESULTS_DIR):
        print(f"[*] Dọn dẹp thư mục kết quả cũ: {RESULTS_DIR}")
        try:
            shutil.rmtree(RESULTS_DIR)
        except Exception as e:
            print(f"[!] Không thể xóa sạch thư mục kết quả cũ: {e}")

    # 3. Chuẩn bị lệnh Pytest
    pytest_cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_login.py",
        f"--alluredir={RESULTS_DIR}",
        "-v"
    ]

    if args.filter:
        pytest_cmd.extend(["-k", args.filter])

    if args.headless:
        os.environ["HEADLESS"] = "true"

    print("\n" + "-" * 80)
    print(f"[*] Đang thực thi kiểm thử với Pytest: {' '.join(pytest_cmd)}")
    print("-" * 80 + "\n")

    # 4. Thực thi Pytest
    test_result = subprocess.run(pytest_cmd)
    
    print("\n" + "=" * 80)
    print(f"[*] Kiểm thử hoàn tất (Exit code: {test_result.returncode})")
    print(f"[*] Dữ liệu thô Allure đã lưu tại: {RESULTS_DIR}")
    print("=" * 80)

    # 5. Tạo báo cáo HTML Allure Report
    if has_cli:
        if args.serve:
            print("\n[*] Đang khởi chạy Allure HTTP Server (Nhấn Ctrl+C để dừng)...")
            subprocess.run([allure_cmd, "serve", RESULTS_DIR], shell=IS_WINDOWS)
        else:
            print(f"\n[*] Đang biên dịch báo cáo tĩnh sang thư mục: {REPORT_DIR} ...")
            gen_result = subprocess.run([allure_cmd, "generate", RESULTS_DIR, "-o", REPORT_DIR, "--clean"], shell=IS_WINDOWS)
            if gen_result.returncode == 0:
                print(f"\n[✓] Báo cáo HTML đã tạo thành công tại: {REPORT_DIR}")
                print(f"    Bạn có thể xem bất kỳ lúc nào bằng lệnh: {allure_cmd} open {REPORT_DIR}")
                
                if not args.no_open:
                    print("\n[*] Đang mở báo cáo trên trình duyệt mặc định...")
                    try:
                        subprocess.run([allure_cmd, "open", REPORT_DIR], shell=IS_WINDOWS)
                    except KeyboardInterrupt:
                        print("\n[✓] Đã đóng máy chủ báo cáo.")
            else:
                print("[!] Lỗi khi biên dịch báo cáo HTML.")
    else:
        print("\n[!] Không thể biên dịch Allure Report do thiếu Allure CLI.")
        print(f"    Dữ liệu kết quả JSON vẫn được lưu đầy đủ tại: {RESULTS_DIR}")

if __name__ == "__main__":
    main()
