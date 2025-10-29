"""
main.py
-------
Streamlit application for Contract Compliance Checking
- Handles file uploads
- Identifies agreement types
- Extracts clauses
- Compares against GDPR templates
- Displays compliance analysis
- Sends automatic notifications for compliance failures
"""

import json
import os
import time
import threading
from datetime import datetime
import streamlit as st
import schedule
import agreement_comparision
import data_extraction
import scrapping
import notification
import slack_notification


def run_scheduler():
    """
    Background scheduler to update template standards automatically.
    Runs scraping function every night at 12:00 AM.
    """
    # Call scraping function every night at 12:00 AM
    schedule.every().day.at("00:00").do(scrapping.call_scrape_funtion)

    # Testing options (commented out for production):
    # schedule.every(10).seconds.do(scrapping.call_scrape_funtion)
    # schedule.every(1).minutes.do(scrapping.call_scrape_funtion)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second


# Start scheduler in background thread so Streamlit does not block
threading.Thread(target=run_scheduler, daemon=True).start()


if __name__ == "__main__":
    
    # Map agreement types to their corresponding JSON template files
    AGREEMENT_JSON_MAP = {
        "Data Processing Agreement": "json/DPA.json",
        "Joint Controller Agreement": "json/JCA.json",
        "Controller-to-Controller Agreement": "json/CCA.json",
        "Processor-to-Subprocessor Agreement": "json/PSA.json",
        "Standard Contractual Clauses": "json/SCC.json"
    }
    
    st.title("Contract Compliance Checker")
    st.markdown("### Upload a contract to check GDPR compliance")
    
    # File upload widget
    uploaded_file = st.file_uploader(
        "Upload an agreement (PDF Only)", 
        type=["pdf"],
        help="Upload a contract document for GDPR compliance analysis"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_file_path = "temp_uploaded.pdf"
        
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.info("Processing your file...")
        
        try:
            # Step 1: Identify the type of agreement
            with st.spinner("Detecting document type..."):
                agreement_type = agreement_comparision.document_type(temp_file_path)
            
            st.success(f"**Detected Document Type:** {agreement_type}")
            
            if agreement_type in AGREEMENT_JSON_MAP:
                
                # Step 2: Extract clauses from the uploaded file
                with st.spinner("Extracting clauses..."):
                    # Use summarization for Data Processing Agreement
                    if agreement_type == "Data Processing Agreement":
                        unseen_data = data_extraction.clause_extraction_with_summarisation(temp_file_path)
                    else:
                        unseen_data = data_extraction.clause_extraction(temp_file_path)
                
                st.success("**Clause Extraction Completed**")
                
                # Step 3: Load the corresponding template JSON
                template_file = AGREEMENT_JSON_MAP[agreement_type]
                
                if not os.path.exists(template_file):
                    st.error(f"Template file not found: {template_file}")
                    st.info("Please ensure all template JSON files are generated in the 'json/' directory.")
                else:
                    with open(template_file, "r", encoding="utf-8") as f:
                        template_data = json.load(f)
                    
                    # Step 4: Compare agreements
                    with st.spinner("Analyzing compliance..."):
                        result = agreement_comparision.compare_agreements(
                            json.dumps(unseen_data) if isinstance(unseen_data, (dict, list)) else unseen_data,
                            json.dumps(template_data) if isinstance(template_data, (dict, list)) else template_data
                        )
                    
                    # Parse the result for structured data
                    parsed_result = agreement_comparision.parse_comparison_result(result)
                    
                    # Display results
                    st.subheader("Compliance Analysis Results")
                    st.markdown(result)
                    
                    # Step 5: Send automatic notifications if compliance issues detected
                    risk_score = parsed_result.get("risk_score", 0)
                    
                    if risk_score > 0:  # Send notification for any detected risk
                        with st.spinner("Sending compliance notifications..."):
                            # Prepare notification data
                            notification_data = {
                                "document_type": agreement_type,
                                "risk_score": risk_score,
                                "missing_clauses": parsed_result.get("missing_clauses", []),
                                "compliance_risks": parsed_result.get("compliance_risks", []),
                                "recommendations": parsed_result.get("recommendations", []),
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            # Send email notification
                            email_sent = notification.send_compliance_failure_notification(notification_data)
                            
                            # Send Slack notification (if configured)
                            slack_sent = False
                            if os.getenv("SLACK_WEBHOOK_URL"):
                                slack_sent = slack_notification.send_compliance_failure_alert(notification_data)
                            
                            # Show notification status
                            if email_sent or slack_sent:
                                st.success("✅ Compliance alert notifications sent successfully!")
                                if email_sent:
                                    st.info(f"📧 Email sent to {os.getenv('SMTP_RECEIVER_EMAIL')}")
                                if slack_sent:
                                    st.info("💬 Slack notification sent")
                            else:
                                st.warning("⚠️ Failed to send notifications. Check your .env configuration.")
                    else:
                        st.success("✅ No compliance issues detected - No notifications needed")
                    
            else:
                st.error(f"This document type is not covered under GDPR compliance checking.")
                st.info("Supported document types: DPA, JCA, C2C, PSA, SCC")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try uploading a different file or contact support.")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except:
                    pass  # Ignore cleanup errors
 