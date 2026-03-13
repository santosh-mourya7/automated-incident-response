import requests
import os
from notify_slack import send_slack_alert

def create_incident(short_desc: str, description: str, urgency: int = 2):
    instance  = os.environ["SNOW_INSTANCE"]
    username  = os.environ["SNOW_USERNAME"]
    password  = os.environ["SNOW_PASSWORD"]

    url = f"{instance}/api/now/table/incident"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "short_description": short_desc,
        "description": description,
        "urgency": str(urgency),          # 1=High, 2=Medium, 3=Low
        "impact": "2",
        "category": "software",
        "caller_id": "admin"
    }

    response = requests.post(
        url,
        auth=(username, password),
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    incident = response.json()["result"]
    incident_number = incident["number"]
    incident_sys_id = incident["sys_id"]

    print(f"Incident created: {incident_number}")

    # Notify Slack
    send_slack_alert(
        f"*Incident Created:* {incident_number}\n"
        f"*Summary:* {short_desc}\n"
        f"*Urgency:* {'High' if urgency==1 else 'Medium'}\n"
        f"*Details:* {description}"
    )

    return incident_sys_id, incident_number


if __name__ == "__main__":
    create_incident(
        short_desc="Service Downtime Detected",
        description="Health check failed. Automated response triggered.",
        urgency=1
    )