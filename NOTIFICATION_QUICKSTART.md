# 🚀 Quick Start: Automatic Compliance Notifications

## Setup (One-time)

### 1. Configure Email in `.env`:
```env
SMTP_SENDER_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_RECEIVER_EMAIL=receiver@example.com
```

### 2. (Optional) Configure Slack in `.env`:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

## How It Works

```
User uploads contract → System analyzes → Risk detected → Notifications sent automatically
                                              ↓
                                    📧 Email + 💬 Slack
```

**That's it! No manual work required.**

---

## Test Your Setup

```bash
# Test everything
python project/test_compliance_notification.py

# Test email only
python project/notification.py

# Test Slack only
python project/slack_notification.py
```

---

## Run Your App

```bash
streamlit run project/main.py
```

Upload a contract → Get results → **Notifications sent automatically!**

---

## Notification Triggers

✅ **Automatic notifications sent when:**
- Risk score > 0 (any compliance issues detected)
- Missing clauses identified
- GDPR compliance risks found

✅ **Includes:**
- Document type
- Risk score (0-100)
- Missing clauses
- Compliance risks
- Recommendations
- Timestamp

---

## File Changes Made

### New Files:
- `test_compliance_notification.py` - Test notifications
- `NOTIFICATION_GUIDE.md` - Complete documentation

### Updated Files:
- `notification.py` - Added `send_compliance_failure_notification()`
- `slack_notification.py` - Added `send_compliance_failure_alert()`
- `agreement_comparision.py` - Added `parse_comparison_result()`
- `main.py` - Integrated automatic notifications

---

## Quick Examples

### Send Email Notification:
```python
from notification import send_compliance_failure_notification

data = {
    "document_type": "DPA",
    "risk_score": 75,
    "missing_clauses": ["Clause 1", "Clause 2"],
    "compliance_risks": ["Risk 1", "Risk 2"],
    "recommendations": ["Fix 1", "Fix 2"],
    "timestamp": "2025-10-29 14:30:00"
}

send_compliance_failure_notification(data)
```

### Send Slack Notification:
```python
from slack_notification import send_compliance_failure_alert

send_compliance_failure_alert(data)  # Same data format
```

---

## Troubleshooting

### Email not working?
1. Use Gmail App Password (not regular password)
2. Enable 2FA on Google Account
3. Test: `python project/notification.py`

### Slack not working?
1. Check webhook URL in `.env`
2. Ensure webhook is active in Slack
3. Test: `python project/slack_notification.py`

---

## 📖 Full Documentation

See `NOTIFICATION_GUIDE.md` for complete details!
