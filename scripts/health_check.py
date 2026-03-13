import requests
import os
import sys

def check_health(url: str) -> bool:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Health check passed: {url}")
            return True
        else:
            print(f"❌ Health check failed: status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False


if __name__ == "__main__":
    target_url = os.environ.get("MONITOR_URL", "https://your-app.onrender.com")
    is_healthy  = check_health(target_url)
    sys.exit(0 if is_healthy else 1)