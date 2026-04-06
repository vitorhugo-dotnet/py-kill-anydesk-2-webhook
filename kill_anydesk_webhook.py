import time
import requests
import psutil

WEBHOOK_URL = "https://your-webhook-url-here"
POLL_INTERVAL = 10
AUTH_USER = ""
AUTH_PASS = ""

def kill_anydesk():
    target_names = {"anydesk", "anydesk.exe"}
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() in target_names:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def poll():
    while True:
        try:
            auth = (AUTH_USER, AUTH_PASS) if AUTH_USER else None
            response = requests.get(WEBHOOK_URL, auth=auth, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("action") == "kill_anydesk":
                kill_anydesk()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
                ValueError):
            pass
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll()
