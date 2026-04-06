# py-kill-anydesk-2-webhook

A Python script that continuously polls a webhook URL and terminates AnyDesk when the webhook returns `{"action": "kill_anydesk"}`.

## Configuration

Open `kill_anydesk_webhook.py` and set the following variables at the top of the file:

- `WEBHOOK_URL` – the full URL of your webhook endpoint.
- `AUTH_USER` / `AUTH_PASS` – Basic Auth credentials (leave both as empty strings `""` to disable authentication).

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install requests psutil
```

## Running as a background process

**Linux / macOS**

```bash
nohup python3 kill_anydesk_webhook.py &
```

Or with `disown` to fully detach from the terminal:

```bash
python3 kill_anydesk_webhook.py &
disown
```

**Windows**

```powershell
Start-Process pythonw -ArgumentList "kill_anydesk_webhook.py" -WindowStyle Hidden
```

The script polls the webhook every 10 seconds and remains running even if the endpoint is temporarily unreachable.