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


if __name__ == "__main__":
    # Test the email sending functionality
    send_email()
