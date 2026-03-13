import requests
import os

def send_slack_alert(message: str, color: str = "danger"):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    
    payload = {
        "attachments": [
            {
                "color": color,
                "title": "🚨 Incident Alert",
                "text": message,
                "footer": "Automated Incident Response System"
            }
        ]
    }
    
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
    print(f"Slack alert sent: {message}")