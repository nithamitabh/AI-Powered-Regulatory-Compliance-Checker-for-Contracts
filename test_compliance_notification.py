"""
test_compliance_notification.py
--------------------------------
Test script to verify automatic compliance failure notifications
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import notification
import slack_notification

# Load environment variables
load_dotenv()


def test_email_notification():
    """Test email notification with sample compliance failure data"""
    print("\n" + "="*70)
    print("Testing Email Compliance Notification")
    print("="*70 + "\n")
    
    # Sample compliance failure data
    sample_data = {
        "document_type": "Data Processing Agreement",
        "risk_score": 75,
        "missing_clauses": [
            "Data Subject Rights - Article 15-22 GDPR",
            "Data Breach Notification - Article 33 GDPR",
            "Data Protection Impact Assessment (DPIA) - Article 35 GDPR"
        ],
        "compliance_risks": [
            "Inadequate data subject rights provisions may violate GDPR Articles 15-22",
            "Missing breach notification clause creates regulatory risk under Article 33",
            "Absence of DPIA requirements may expose organization to fines"
        ],
        "recommendations": [
            "Add comprehensive data subject rights clause covering all GDPR Articles 15-22",
            "Include data breach notification procedures with 72-hour timeline",
            "Add DPIA requirements for high-risk processing activities"
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send email
    result = notification.send_compliance_failure_notification(sample_data)
    
    if result:
        print("✅ Email notification sent successfully!")
        print(f"📧 Check inbox: {os.getenv('SMTP_RECEIVER_EMAIL')}")
    else:
        print("❌ Failed to send email notification")
        print("💡 Check your .env file for correct SMTP credentials")
    
    return result


def test_slack_notification():
    """Test Slack notification with sample compliance failure data"""
    print("\n" + "="*70)
    print("Testing Slack Compliance Notification")
    print("="*70 + "\n")
    
    # Check if Slack is configured
    if not os.getenv("SLACK_WEBHOOK_URL"):
        print("⚠️ Slack webhook not configured - Skipping Slack test")
        print("💡 Add SLACK_WEBHOOK_URL to .env file to enable Slack notifications")
        return False
    
    # Sample compliance failure data
    sample_data = {
        "document_type": "Joint Controller Agreement",
        "risk_score": 55,
        "missing_clauses": [
            "Joint controller responsibilities - Article 26 GDPR",
            "Data sharing protocols",
            "Liability allocation between controllers"
        ],
        "compliance_risks": [
            "Unclear joint controller relationship may violate Article 26",
            "Missing data sharing protocols create compliance gaps",
            "Undefined liability allocation increases legal risk"
        ],
        "recommendations": [
            "Define clear joint controller responsibilities per Article 26",
            "Establish detailed data sharing protocols and safeguards",
            "Allocate liability proportionally between joint controllers"
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send Slack notification
    result = slack_notification.send_compliance_failure_alert(sample_data)
    
    if result:
        print("✅ Slack notification sent successfully!")
        print("💬 Check your Slack channel")
    else:
        print("❌ Failed to send Slack notification")
        print("💡 Check your SLACK_WEBHOOK_URL in .env file")
    
    return result


def test_low_risk_scenario():
    """Test notification with low risk score"""
    print("\n" + "="*70)
    print("Testing Low Risk Scenario (should still notify)")
    print("="*70 + "\n")
    
    sample_data = {
        "document_type": "Standard Contractual Clauses",
        "risk_score": 15,
        "missing_clauses": [
            "Minor formatting inconsistency in Annex II"
        ],
        "compliance_risks": [
            "Minor non-compliance with SCC template formatting"
        ],
        "recommendations": [
            "Update Annex II formatting to match official SCC template"
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    result = notification.send_compliance_failure_notification(sample_data)
    
    if result:
        print("✅ Low risk notification sent successfully!")
    else:
        print("❌ Failed to send low risk notification")
    
    return result


def test_critical_risk_scenario():
    """Test notification with critical risk score"""
    print("\n" + "="*70)
    print("Testing Critical Risk Scenario")
    print("="*70 + "\n")
    
    sample_data = {
        "document_type": "Controller-to-Controller Agreement",
        "risk_score": 95,
        "missing_clauses": [
            "Legal basis for processing - Article 6 GDPR",
            "Data subject rights - Articles 15-22 GDPR",
            "Security measures - Article 32 GDPR",
            "Cross-border transfer safeguards - Chapter V GDPR",
            "Data retention and deletion policies"
        ],
        "compliance_risks": [
            "CRITICAL: No legal basis for processing violates Article 6 - Major fine risk",
            "CRITICAL: Missing data subject rights creates severe non-compliance",
            "HIGH: Inadequate security measures violate Article 32",
            "HIGH: No cross-border transfer safeguards violate Chapter V",
            "MEDIUM: Missing data retention policy creates compliance risk"
        ],
        "recommendations": [
            "URGENT: Establish legal basis for all processing activities (Article 6)",
            "URGENT: Add comprehensive data subject rights provisions",
            "HIGH PRIORITY: Implement technical and organizational security measures",
            "HIGH PRIORITY: Add appropriate transfer mechanisms (SCCs, BCRs, or adequacy decisions)",
            "PRIORITY: Define clear data retention schedules and deletion procedures"
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Send both email and Slack
    email_result = notification.send_compliance_failure_notification(sample_data)
    slack_result = False
    
    if os.getenv("SLACK_WEBHOOK_URL"):
        slack_result = slack_notification.send_compliance_failure_alert(sample_data)
    
    if email_result or slack_result:
        print("✅ Critical risk notifications sent!")
        if email_result:
            print("   📧 Email sent")
        if slack_result:
            print("   💬 Slack sent")
    else:
        print("❌ Failed to send critical risk notifications")
    
    return email_result or slack_result


if __name__ == "__main__":
    print("\n" + "🚀 "*35)
    print("GDPR Compliance Notification System - Test Suite")
    print("🚀 "*35)
    
    # Run tests
    email_passed = test_email_notification()
    slack_passed = test_slack_notification()
    low_risk_passed = test_low_risk_scenario()
    critical_passed = test_critical_risk_scenario()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Email Notification:        {'✅ PASSED' if email_passed else '❌ FAILED'}")
    print(f"Slack Notification:        {'✅ PASSED' if slack_passed else '⚠️ SKIPPED (not configured)'}")
    print(f"Low Risk Scenario:         {'✅ PASSED' if low_risk_passed else '❌ FAILED'}")
    print(f"Critical Risk Scenario:    {'✅ PASSED' if critical_passed else '❌ FAILED'}")
    print("="*70)
    
    total_tests = 4
    passed_tests = sum([email_passed, slack_passed, low_risk_passed, critical_passed])
    
    print(f"\nTests Passed: {passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Notification system is working correctly.")
    elif email_passed or critical_passed:
        print("⚠️ Some tests passed. Check configuration for failed tests.")
    else:
        print("❌ Tests failed. Please check your .env configuration.")
    
    print("\n" + "="*70)
    print("📝 NOTE: Check your email inbox and Slack channel for notifications")
    print("="*70 + "\n")
