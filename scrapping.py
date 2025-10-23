"""
scrapping.py
------------
Automated template scraping and update system
- Downloads GDPR agreement templates from official sources
- Extracts clauses using AI
- Detects changes in templates
- Sends email notifications when changes are detected
"""

import requests
import json
import os
import hashlib
import data_extraction
import time
from notification import send_email


def calculate_file_hash(filepath):
    """
    Calculate MD5 hash of a file to detect changes.
    
    Args:
        filepath (str): Path to the file
    
    Returns:
        str: MD5 hash of the file, or None if file doesn't exist
    """
    if not os.path.exists(filepath):
        return None
    
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating hash: {e}")
        return None


def scrape_data(url, name):
    """
    Download data from URL and save to file.
    
    Args:
        url (str): URL to download from
        name (str): Filename to save as
    
    Returns:
        bool: True if download successful, False otherwise
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Download Successful: {name} at {time.ctime()}")
            return True
        else:
            print(f"Failed to download: {name}, Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {name}: {e}")
        return False
    
def call_scrape_funtion():
    """
    Main scraping function that downloads templates, extracts clauses,
    and sends notifications if changes are detected.
    """
    # Document mapping with correct paths
    DOCUMENT_MAP = {
        "DPA": {
            "json_file": "json/DPA.json",
            "link": r"https://www.benchmarkone.com/wp-content/uploads/2018/05/GDPR-Sample-Agreement.pdf",
            "name": "Data Processing Agreement"
        },
        "JCA": {
            "json_file": "json/JCA.json",
            "link": r"https://www.surf.nl/files/2019-11/model-joint-controllership-agreement.pdf",
            "name": "Joint Controller Agreement"
        },
        "CCA": {
            "json_file": "json/CCA.json",
            "link": r"https://www.fcmtravel.com/sites/default/files/2020-03/2-Controller-to-controller-data-privacy-addendum.pdf",
            "name": "Controller-to-Controller Agreement"
        },
        "SCC": {
            "json_file": "json/SCC.json",
            "link": r"https://www.miller-insurance.com/assets/PDF-Downloads/Standard-Contractual-Clauses-SCCs.pdf",
            "name": "Standard Contractual Clauses"
        },
        "PSA": {
            "json_file": "json/PSA.json",
            "link": r"https://greaterthan.eu/wp-content/uploads/Personal-Data-Sub-Processor-Agreement-2024-01-24.pdf",
            "name": "Processor-to-Subprocessor Agreement"
        }
    }
    
    temp_agreement = "temp_agreement.pdf"
    changes_detected = []
    errors = []
    
    print(f"\n{'='*60}")
    print(f"Starting Template Update Process - {time.ctime()}")
    print(f"{'='*60}\n")
    
    for key, value in DOCUMENT_MAP.items():
        try:
            json_file = value["json_file"]
            link = value["link"]
            name = value["name"]
            
            print(f"Processing: {name} ({key})")
            
            # Calculate hash of existing JSON file (if exists)
            old_hash = calculate_file_hash(json_file)
            
            # Download the PDF template
            if not scrape_data(link, temp_agreement):
                errors.append(f"Failed to download {name}")
                continue
            
            # Extract clauses from the downloaded PDF
            print(f"  Extracting clauses from {name}...")
            clauses = data_extraction.Clause_extraction(temp_agreement)
            
            # Save to JSON file
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(clauses, f, indent=2, ensure_ascii=False)
            
            # Calculate hash of new JSON file
            new_hash = calculate_file_hash(json_file)
            
            # Check if content changed
            if old_hash is None:
                print(f"  ✓ New template created: {name}")
                changes_detected.append(f"**{name}**: New template created")
            elif old_hash != new_hash:
                print(f"  ✓ Changes detected in: {name}")
                changes_detected.append(f"**{name}**: Template updated with new clauses")
            else:
                print(f"  ✓ No changes in: {name}")
            
            # Clean up temp file
            if os.path.exists(temp_agreement):
                os.remove(temp_agreement)
                
        except Exception as e:
            error_msg = f"Error processing {name}: {str(e)}"
            print(f"  ✗ {error_msg}")
            errors.append(error_msg)
    
    print(f"\n{'='*60}")
    print(f"Template Update Process Completed - {time.ctime()}")
    print(f"{'='*60}\n")
    
    # Send notification email if there are changes or errors
    if changes_detected or errors:
        send_update_notification(changes_detected, errors)
        
        # Also send Slack notification if configured
        try:
            from slack_notification import send_template_update_notification
            send_template_update_notification(changes_detected, errors)
        except Exception as e:
            print(f"Note: Slack notification not sent: {e}")
    else:
        print("No changes detected. No notification sent.")


def send_update_notification(changes, errors):
    """
    Send email notification about template updates.
    
    Args:
        changes (list): List of changes detected
        errors (list): List of errors encountered
    """
    subject = "🔄 GDPR Template Update Notification"
    
    # Build email body
    body_parts = [
        "GDPR Compliance Checker - Template Update Report",
        "=" * 50,
        f"\nUpdate Time: {time.ctime()}\n"
    ]
    
    if changes:
        body_parts.append("\n📝 CHANGES DETECTED:")
        body_parts.append("-" * 50)
        for change in changes:
            body_parts.append(f"  • {change}")
        body_parts.append("")
    
    if errors:
        body_parts.append("\n⚠️ ERRORS ENCOUNTERED:")
        body_parts.append("-" * 50)
        for error in errors:
            body_parts.append(f"  • {error}")
        body_parts.append("")
    
    body_parts.extend([
        "\n" + "=" * 50,
        "\nThis is an automated notification from the GDPR Compliance Checker.",
        "The template standards have been updated to ensure accurate compliance checking."
    ])
    
    body = "\n".join(body_parts)
    
    # Send email notification
    print("\n📧 Sending notification email...")
    success = send_email(subject=subject, body=body)
    
    if success:
        print("✓ Notification sent successfully!")
    else:
        print("✗ Failed to send notification email.")


# For testing purposes - uncomment to run manually
# if __name__ == "__main__":
#     call_scrape_funtion()