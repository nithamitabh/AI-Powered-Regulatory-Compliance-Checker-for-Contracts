"""
SMTP Email Notification Module

This module sends email notifications using SMTP.
Credentials and configuration are loaded from environment variables.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_email(subject=None, body=None, receiver=None):
    """
    Send an email using SMTP.
    
    Args:
        subject (str, optional): Email subject. Defaults to "Test Email".
        body (str, optional): Email body content. Defaults to a test message.
        receiver (str, optional): Receiver email address. Defaults to env variable.
    
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        # Get credentials from environment variables
        sender = os.getenv("SMTP_SENDER_EMAIL")
        password = os.getenv("SMTP_PASSWORD")
        receiver = receiver or os.getenv("SMTP_RECEIVER_EMAIL")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        
        # Validate required credentials
        if not all([sender, password, receiver]):
            raise ValueError("Missing required email credentials in .env file")
        
        # Create message
        msg = MIMEMultipart()
        msg["Subject"] = subject or "Test Email"
        msg["From"] = sender
        msg["To"] = receiver
        
        # Attach body
        body_text = body or "Hello, this is a test email sent using SMTP in Python."
        msg.attach(MIMEText(body_text, "plain"))
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender, password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {receiver}!")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_compliance_failure_notification(report_data):
    """
    Send detailed notification about compliance failures.
    
    Args:
        report_data (dict): Dictionary containing compliance analysis results
            - document_type: Type of document analyzed
            - risk_score: Risk score (0-100)
            - missing_clauses: List or text of missing clauses
            - compliance_risks: List or text of compliance risks
            - recommendations: List or text of recommendations
            - timestamp: When analysis was performed (optional)
    
    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        # Extract data from report
        document_type = report_data.get("document_type", "Unknown Document")
        risk_score = report_data.get("risk_score", "N/A")
        missing_clauses = report_data.get("missing_clauses", "None detected")
        compliance_risks = report_data.get("compliance_risks", "None detected")
        recommendations = report_data.get("recommendations", "No recommendations available")
        timestamp = report_data.get("timestamp", "Not specified")
        
        # Determine risk level
        try:
            score_num = int(risk_score) if isinstance(risk_score, (int, float, str)) and str(risk_score).isdigit() else 0
            if score_num <= 25:
                risk_level = "LOW RISK ✅"
            elif score_num <= 50:
                risk_level = "MEDIUM RISK ⚠️"
            elif score_num <= 75:
                risk_level = "HIGH RISK 🔶"
            else:
                risk_level = "CRITICAL RISK 🔴"
        except:
            risk_level = "UNKNOWN RISK"
        
        # Format missing clauses
        if isinstance(missing_clauses, list):
            missing_clauses_text = "\n".join([f"  • {clause}" for clause in missing_clauses])
        else:
            missing_clauses_text = str(missing_clauses)
        
        # Format compliance risks
        if isinstance(compliance_risks, list):
            risks_text = "\n".join([f"  • {risk}" for risk in compliance_risks])
        else:
            risks_text = str(compliance_risks)
        
        # Format recommendations
        if isinstance(recommendations, list):
            recommendations_text = "\n".join([f"  • {rec}" for rec in recommendations])
        else:
            recommendations_text = str(recommendations)
        
        # Build email subject
        subject = f"⚠️ GDPR Compliance Alert: {document_type} - Risk Score {risk_score}/100"
        
        # Build email body with detailed formatting
        body = f"""
╔══════════════════════════════════════════════════════════════╗
║           GDPR COMPLIANCE FAILURE NOTIFICATION               ║
╚══════════════════════════════════════════════════════════════╝

📄 DOCUMENT INFORMATION
─────────────────────────────────────────────────────────────────
Document Type: {document_type}
Analysis Date: {timestamp}

⚠️ RISK ASSESSMENT
─────────────────────────────────────────────────────────────────
Risk Score:    {risk_score}/100
Risk Level:    {risk_level}

❌ MISSING CLAUSES
─────────────────────────────────────────────────────────────────
{missing_clauses_text}

🚨 COMPLIANCE RISKS IDENTIFIED
─────────────────────────────────────────────────────────────────
{risks_text}

✅ RECOMMENDATIONS
─────────────────────────────────────────────────────────────────
{recommendations_text}

─────────────────────────────────────────────────────────────────
🤖 This alert was automatically generated by the GDPR Compliance Checker.
Please review and take appropriate action to ensure compliance.

For questions or support, contact your compliance team.
"""
        
        # Send the email
        return send_email(subject=subject, body=body)
        
    except Exception as e:
        print(f"Failed to send compliance failure notification: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the email sending functionality
    send_email()
