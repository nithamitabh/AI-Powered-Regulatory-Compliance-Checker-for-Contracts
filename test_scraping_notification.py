"""
Test script for scraping with notification
------------------------------------------
This script allows you to test the scraping functionality manually
to see if notifications are sent when changes are detected.
"""

import scrapping

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Scraping with Notification Feature")
    print("="*60 + "\n")
    
    print("This will:")
    print("1. Download all GDPR template PDFs")
    print("2. Extract clauses from each template")
    print("3. Compare with existing JSON files")
    print("4. Send email notification if changes detected")
    print("\nNote: Make sure your .env file has correct email credentials!\n")
    
    input("Press Enter to start the test...")
    
    # Run the scraping function
    scrapping.call_scrape_funtion()
    
    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)
    print("\nCheck your email inbox for notifications if changes were detected.")
