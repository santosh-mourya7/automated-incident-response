import requests
import os
from notify_slack import send_slack_alert

def resolve_incident(sys_id: str, incident_number: str):
    instance = os.environ["SNOW_INSTANCE"]
    username = os.environ["SNOW_USERNAME"]
    password = os.environ["SNOW_PASSWORD"]

    url = f"{instance}/api/now/table/incident/{sys_id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "state": "6",                          # 6 = Resolved in ServiceNow
        "close_code": "Solved (Permanently)",
        "close_notes": "Service recovered. Auto-resolved by monitoring system."
    }

    response = requests.patch(
        url,
        auth=(username, password),
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    print(f"Incident {incident_number} resolved")

    send_slack_alert(
        f"✅ *Incident Resolved:* {incident_number}\n"
        f"Service has recovered. Incident auto-closed.",
        color="good"
    )


if __name__ == "__main__":
    sys_id = os.environ.get("INCIDENT_SYS_ID", "")
    number = os.environ.get("INCIDENT_NUMBER", "")
    resolve_incident(sys_id, number)