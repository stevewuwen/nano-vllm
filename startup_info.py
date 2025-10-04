import os
import shutil
import sys
import socket
import platform
import datetime
import subprocess
import urllib.request
import pwd
import urllib.error
from zoneinfo import ZoneInfo

def get_current_datetime():
    return datetime.datetime.now(ZoneInfo("Asia/Chongqing")).strftime("%Y-%m-%d %H:%M:%S")

def get_system_info():
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }

def get_user_info():
    return {
        "User": pwd.getpwuid(os.getuid()).pw_name,
        "Home Directory": os.path.expanduser("~"),
        "Current Working Directory": os.getcwd(),
    }

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """使用 DNS 查询检查网络连通性（不依赖 HTTP）"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def check_google_access(timeout=5):
    """尝试访问 google.com，检查是否可访问"""
    try:
        urllib.request.urlopen("https://www.google.com", timeout=timeout)
        return True
    except (urllib.error.URLError, socket.timeout):
        return False

def has_nvidia_gpu():
    if shutil.which("nvidia-smi") is None:
        return False
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"])
        return len(output.strip()) > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("=" * 60)
    print("🚀 程序启动信息")
    print("=" * 60)

    # 当前日期和时间
    print(f"📅 当前日期和时间: {get_current_datetime()}")

    # 用户信息
    user_info = get_user_info()
    print(f"👤 用户: {user_info['User']}")
    print(f"🏠 主目录: {user_info['Home Directory']}")
    print(f"📂 当前工作目录: {user_info['Current Working Directory']}")

    # 系统信息
    sys_info = get_system_info()
    print("\n💻 系统信息:")
    for key, value in sys_info.items():
        print(f"  {key}: {value}")

    # 网络检查
    print("\n🌐 网络连接检查:")
    if check_internet_connection():
        print("  ✅ 基本网络连接正常")
        if check_google_access():
            print("  ✅ 可访问 Google")
        else:
            print("  ❌ 无法访问 Google（可能被屏蔽或网络问题）")
    else:
        print("  ❌ 无网络连接")
    
    # 显卡检查
    print("\n🖴 显卡检查")
    if has_nvidia_gpu():
        print("检测到 NVIDIA GPU")
    else:
        print("未检测到 NVIDIA GPU 或驱动未安装")
    

    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}", file=sys.stderr)
        sys.exit(1)