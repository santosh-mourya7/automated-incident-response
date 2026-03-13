# 🚨 Automated Incident Response System

> A production-grade incident response pipeline that automatically detects service failures, creates ServiceNow incidents, and delivers real-time Slack alerts — all powered by GitHub Actions.

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ServiceNow](https://img.shields.io/badge/ServiceNow-00C853?style=for-the-badge&logo=servicenow&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
<img width="373" height="67" alt="image" src="https://github.com/user-attachments/assets/db770181-fbb4-4578-9a34-8bf55d6e16e8" />


---

## 📋 Table of Contents

•	Overview
•	Architecture
•	Features
•	Tech Stack
•	Project Structure
•	Getting Started
•	Configuration
•	Workflows
•	API Reference
•	Testing

---

## 📌 Overview

This project automates the full incident response lifecycle — from detection to resolution. When a service goes down, the system:

1. **Detects** the failure via scheduled health checks
2. **Creates** a ServiceNow incident automatically
3. **Alerts** the on-call team via Slack instantly
4. **Resolves** the incident automatically when service recovers

Detection and alerting are fully automated.
Incident resolution is one-click via GitHub Actions workflow.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Actions                        │
│                                                         │
│   ┌─────────────┐      Fails      ┌──────────────────┐  │
│   │ health_     │ ─────────────►  │ create_          │  │
│   │ check.py    │                 │ incident.py      │  │
│   └─────────────┘                 └────────┬─────────┘  │
│   (Every 15 mins)                          │            │
└───────────────────────────────────────────-│────────────┘
                                             │
                    ┌────────────────────────┤
                    │                        │
                    ▼                        ▼
        ┌───────────────────┐    ┌───────────────────────┐
        │    ServiceNow     │    │        Slack          │
        │  Incident Created │    │   Alert Delivered     │
        │  INC0010001 🎫   │     │  #incidents 🔔       │
        └───────────────────┘    └───────────────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │  resolve_         │
        │  incident.py      │
        │  (Manual trigger) │
        └───────────────────┘
                    │
                    ▼
        ┌───────────────────┐
        │  Incident Closed  │
        │  ✅ Resolved      │
        └───────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Automated Health Monitoring** | Scheduled checks every 15-minute intervals via GitHub Actions |
| 🎫 **ServiceNow Integration** | Auto-creates incidents via REST API with priority and categorization |
| 🔔 **Slack Alerts** | Real-time notifications with incident details delivered to team channels |
| ✅ **Auto-Resolution** | One-click workflow to resolve incidents and notify team of recovery |
| 🔒 **Secure Secrets Management** | All credentials stored as GitHub Secrets — never hardcoded |
| 🧪 **Automated Testing** | pytest unit tests for all core functions |
| 🚀 **CI/CD Pipeline** | Full GitHub Actions pipeline with zero infrastructure management |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Automation** | GitHub Actions | Workflow orchestration |
| **Backend** | Python 3.11 | Core scripting and API integration logic |
| **ITSM** | ServiceNow PDI | Incident creation, tracking, and resolution |
| **Notifications** | Slack Webhooks | Real-time team alerts |
| **Hosting** | Render (Free Tier) | Monitored web service endpoint |
| **REST Client** | requests 2.31.0 | HTTP calls to ServiceNow and Slack APIs |
| **Testing** | pytest 9.0.2 | Unit testing for all Python scripts |

---

## 📁 Project Structure

```
automated-incident-response/
│
├── .github/
│   └── workflows/
│       ├── monitor.yml           # Scheduled health check + incident creation
│       └── resolve.yml           # Manual incident resolution workflow
│
├── scripts/
│   ├── create_incident.py        # ServiceNow incident creation via REST API
│   ├── resolve_incident.py       # ServiceNow incident resolution via REST API
│   ├── notify_slack.py           # Slack webhook notification handler
│   └── health_check.py           # HTTP health check for monitored service
│
├── tests/
│   └── test_incidents.py         # pytest unit tests
│
├── docs/
│   └── architecture.txt         # System architecture diagram
│
├── app.py                        # Flask health endpoint (deployed on Render)
├── render.yaml                   # Render deployment configuration
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- GitHub account
- ServiceNow Personal Developer Instance → [developer.servicenow.com](https://developer.servicenow.com)
- Slack workspace with Incoming Webhooks enabled
- Render account → [render.com](https://render.com)
- Python 3.11+

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/automated-incident-response.git
cd automated-incident-response
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure GitHub Secrets** *(see Configuration section below)*

**4. Deploy the monitored app on Render**
```bash
# Push to GitHub → connect repo on Render → deploy automatically
git push origin main
```

---

## ⚙️ Configuration

All sensitive credentials are stored as **GitHub Repository Secrets**.

Go to: `Settings → Secrets and Variables → Actions → New Repository Secret`

| Secret Name | Description | Example |
|---|---|---|
| `SNOW_INSTANCE` | ServiceNow instance base URL | `https://devXXXXXX.service-now.com` |
| `SNOW_USERNAME` | ServiceNow admin username | `admin` |
| `SNOW_PASSWORD` | ServiceNow admin password | `your-password` |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL | `https://hooks.slack.com/services/XXX/YYY/ZZZ` |
| `MONITOR_URL` | URL of the service to monitor | `https://your-app.onrender.com` |

---

## ⚡ Workflows

### 1. Health Monitor & Incident Creator
**File:** `.github/workflows/monitor.yml`

**Triggers:**
- ⏰ Automatically every 15 minutes (`cron: '*/15 * * * *'`)
- 🖱️ Manually via `workflow_dispatch`

**Flow:**
```
Run Health Check
      │
      ├── ✅ PASS → No action taken
      │
      └── ❌ FAIL → Create ServiceNow Incident + Send Slack Alert
```

---

### 2. Auto Resolve Incident
**File:** `.github/workflows/resolve.yml`

**Triggers:**
- 🖱️ Manually via `workflow_dispatch` with inputs

**Required Inputs:**
```
incident_sys_id   → ServiceNow internal SYS ID
incident_number   → Human-readable incident number (e.g. INC0010001)
```

**Flow:**
```
Receive SYS ID + Incident Number
      │
      ▼
Patch ServiceNow Incident → State: Resolved
      │
      ▼
Send Slack Recovery Alert ✅
```

---

## 📡 API Reference

### ServiceNow REST API

**Create Incident**
```
POST {SNOW_INSTANCE}/api/now/table/incident
Authorization: Basic Auth
Content-Type: application/json

{
  "short_description": "Service Downtime Detected",
  "description": "Health check failed. Automated response triggered.",
  "urgency": "1",
  "impact": "2",
  "category": "software",
  "caller_id": "admin"
}
```

**Resolve Incident**
```
PATCH {SNOW_INSTANCE}/api/now/table/incident/{sys_id}
Authorization: Basic Auth
Content-Type: application/json

{
  "state": "6",
  "close_code": "Solved (Permanently)",
  "close_notes": "Service recovered. Auto-resolved by monitoring system."
}
```

### Slack Webhook
```
POST https://hooks.slack.com/services/XXX/YYY/ZZZ
Content-Type: application/json

{
  "attachments": [{
    "color": "danger",
    "title": "🚨 Incident Alert",
    "text": "Incident Created: INC0010001"
  }]
}
```

---

## 🧪 Testing

Run unit tests locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Expected output:
# test_health_check_success PASSED
# test_health_check_failure PASSED
# test_health_check_timeout PASSED
```

---

## 📊 How It Looks in Action

**ServiceNow Incident Created:**
```
Number        : INC0010001
Short Desc    : Service Downtime Detected
State         : New
Urgency       : 1 - High
Category      : Software
Opened        : 2026-03-12 21:00:00
```

**Slack Alert Received:**
```
🚨 Incident Alert
─────────────────────────────
Incident Created: INC0010001
Summary: Service Downtime Detected
Urgency: High
Details: Health check failed. Automated response triggered.
─────────────────────────────
Automated Incident Response System
```

---

## 🙌 Author

Built as a portfolio project demonstrating enterprise-grade automation using ServiceNow, GitHub Actions, Python REST APIs, and Slack integrations.
