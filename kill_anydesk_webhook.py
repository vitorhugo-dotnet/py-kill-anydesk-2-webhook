import shutil
import subprocess
import time

import psutil
import requests

WEBHOOK_URL = "..."
POLL_INTERVAL = 10
AUTH_USER = "..."
AUTH_PASS = "..."
RESTART_DELAY = 2


def find_anydesk_executable():
    candidates = [
        shutil.which("AnyDesk.exe"),
        r"F:\Program Files (x86)\AnyDesk\AnyDesk.exe",
    ]
    for path in candidates:
        if path:
            return path
    return None


def kill_anydesk():
    target_names = {"AnyDesk.exe"}
    killed = False
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"] in target_names:
                proc.kill()
                killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return killed


def open_anydesk():
    executable = find_anydesk_executable()
    if not executable:
        return False
    try:
        subprocess.Popen([executable])
        return True
    except OSError:
        return False


def restart_anydesk():
    if kill_anydesk():
        time.sleep(RESTART_DELAY)
    open_anydesk()


def poll():
    previous_status = None
    while True:
        try:
            auth = (AUTH_USER, AUTH_PASS) if AUTH_USER else None
            response = requests.get(WEBHOOK_URL, auth=auth, timeout=10)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")

            if status == "KILL" and previous_status != "KILL":
                restart_anydesk()

            previous_status = status
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException,
            ValueError,
        ):
            pass

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    poll()
