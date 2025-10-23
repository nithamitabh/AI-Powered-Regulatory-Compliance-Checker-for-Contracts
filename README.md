# 📋 Contract Compliance Checker

> 🔒 An AI-powered GDPR compliance verification system for legal contracts

## 🌟 Overview

The **Contract Compliance Checker** is an intelligent web application that automates the process of analyzing legal contracts for - 🕐 Runs daily at midnight (00:00)
- 📥 Scrapes latest templates from official sources
- 🔍 Compares new templates with existing ones using hash verification
- 📧 **Sends email notifications when changes are detected**
- 💬 **Sends Slack notifications (if configured)**
- ✅ Ensures compliance checks use current standards
- ⚠️ Reports any errors encountered during updatesompliance. It uses advanced AI models to detect document types, extract clauses, and compare them against regulatory standards.

## ✨ Features

- 📄 **Automated Document Classification** - Identifies 5 types of GDPR-related agreements
- 🔍 **Intelligent Clause Extraction** - Extracts and summarizes contract clauses using AI
- ⚖️ **Compliance Analysis** - Compares uploaded contracts against standard templates
- 🎯 **Risk Assessment** - Assigns risk scores (0-100) for compliance gaps
- 📊 **Detailed Reporting** - Provides missing clauses, risks, and recommendations
- 🔄 **Auto-Update System** - Scheduled scraping to keep templates up-to-date
- 🎨 **User-Friendly Interface** - Built with Streamlit for easy interaction

## 🗂️ Supported Document Types

The system can analyze the following contract types:

1. 📑 **Data Processing Agreement (DPA)**
2. 🤝 **Joint Controller Agreement (JCA)**
3. 🔗 **Controller-to-Controller Agreement (C2C)**
4. 🔄 **Processor-to-Subprocessor Agreement (PSA)**
5. 📜 **Standard Contractual Clauses (SCC)**

## 🏗️ Project Structure

```
project/
├── main.py                          # 🚀 Streamlit application entry point
├── agreement_comparision.py         # 🔍 Document classification & comparison
├── data_extraction.py               # 📝 Clause extraction with AI
├── scrapping.py                     # 🕷️ Template scraping & updates
├── pipeline.py                      # ⚙️ Automated processing pipeline
├── notification.py                  # 📧 Email notification module (SMTP)
├── slack_notification.py            # 💬 Slack notification module (Webhooks)
├── requirements.txt                 # 📦 Python dependencies
├── .env                             # 🔐 Environment variables (not in git)
├── .env.example                     # 📋 Template for environment variables
├── json/                            # 💾 Template standards
│   ├── DPA.json
│   ├── JCA.json
│   ├── CCA.json
│   ├── PSA.json
│   └── SCC.json
└── templates/                       # 📚 Reference documents
    ├── (DPA) appendix-gdpr-eea-uk-4-27-21.pdf
    ├── (JCA) model-joint-controllership-agreement.pdf
    ├── (C2C) 2-Controller-to-controller-data-privacy-addendum.pdf
    ├── (SCCs) Standard Contractual Clauses.pdf
    └── (PSA) Personal-Data-Sub-Processor-Agreement-2024-01-24.pdf
```

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.8 or higher
- 🔑 Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root (copy from `.env.example`):
   ```env
   # API Keys
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   
   # Email Configuration (for notifications)
   SMTP_SENDER_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password_here
   SMTP_RECEIVER_EMAIL=receiver_email@gmail.com
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   
   # Slack Configuration (optional)
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   ```
   
   **Note for Gmail Users:** Use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password. Enable 2-Step Verification first, then generate an app password from Google Account Security settings.

5. **Prepare template standards** (if not already present)
   
   Run the pipeline to generate JSON templates:
   ```bash
   python pipeline.py
   ```

### 🎯 Running the Application

Launch the Streamlit web application:

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage

1. **Upload Contract** 📤
   - Click "Browse files" or drag & drop a PDF contract
   - Supported format: PDF only

2. **Automatic Analysis** 🤖
   - The system detects the document type
   - Extracts all clauses automatically
   - Compares against GDPR standard templates

3. **Review Results** 📊
   - View missing or altered clauses
   - Check compliance risks
   - Review risk score and recommendations
   - Get actionable amendments

## 🛠️ Core Modules

### `main.py`
- 🎨 Streamlit web interface
- 📤 File upload handling
- 🔄 Background scheduler for auto-updates
- 📊 Results visualization

### `agreement_comparision.py`
- 🔍 Document type detection using AI
- ⚖️ Clause-by-clause comparison
- 🎯 Risk scoring and analysis
- 💡 Compliance recommendations

### `data_extraction.py`
- 📄 PDF text extraction
- 🤖 AI-powered clause extraction
- 📝 Summarization (for large documents)
- 💾 JSON output generation

### `scrapping.py`
- 🕷️ Automated template scraping from web sources
- 🔄 Scheduled updates (daily at 12:00 AM)
- 📥 Downloads latest standard agreements
- � Detects changes using file hash comparison
- 📧 Sends email notifications when templates are updated
- 🛡️ Error handling and reporting

### `pipeline.py`
- ⚙️ Orchestrates the entire workflow
- 🏗️ Builds template library
- 🔄 Runs end-to-end comparison pipeline

### `notification.py`
- 📧 Email notification system using SMTP
- 🔐 Secure credential management via environment variables
- ✅ Configurable sender, receiver, and message content
- 🛡️ Error handling and validation

### `slack_notification.py`
- 💬 Slack notification system using webhooks
- 📊 Rich formatted messages with blocks
- 🎯 Compliance report formatting
- 🔄 Template update notifications
- 🔐 Secure webhook URL management

## 🧪 Example Workflows

### Document Analysis Pipeline
```python
# Run pipeline for a new document
from pipeline import run_pipeline

result = run_pipeline("your-contract.pdf")
print(result)
```

### Email Notifications
```python
# Send email notification
from notification import send_email

# Use defaults from .env
send_email()

# Send custom notification
send_email(
    subject="Compliance Report Ready",
    body="Your GDPR compliance analysis is complete. Risk Score: 45/100",
    receiver="team@company.com"
)
```

### Test Notification Module
```bash
python notification.py
```

### Test Slack Notification
```bash
python slack_notification.py
```

### Test Scraping with Notifications
```bash
python test_scraping_notification.py
```

This will manually trigger the scraping process and send notifications if changes are detected.

## 🔐 Security & Privacy

- 🔒 Temporary files are automatically cleaned up
- 🗑️ Uploaded files are deleted after processing
- 🔑 API keys and credentials stored securely in `.env` file
- 🚫 No data is stored permanently on the server
- 🔐 `.env` file excluded from version control via `.gitignore`
- 🛡️ Gmail App Passwords used instead of regular passwords
- ✅ Environment variables for all sensitive configuration

## 🤖 Technology Stack

- **Frontend:** Streamlit
- **AI Model:** Google Gemini 2.5 Flash
- **PDF Processing:** PyPDF2, pypdf
- **Data Validation:** Pydantic
- **Scheduling:** schedule
- **Environment:** python-dotenv

## 📊 Risk Score Interpretation

- **0-25:** ✅ Low Risk - Minor issues
- **26-50:** ⚠️ Medium Risk - Attention needed
- **51-75:** 🔶 High Risk - Significant gaps
- **76-100:** 🔴 Critical Risk - Major compliance issues

## 🔄 Auto-Update System

The application includes a background scheduler that:
- 🕐 Runs daily at midnight (00:00)
- 📥 Scrapes latest templates from official sources
- � Compares new templates with existing ones using hash verification
- 📧 **Sends email notifications when changes are detected**
- ✅ Ensures compliance checks use current standards
- ⚠️ Reports any errors encountered during updates

### What Gets Notified?
- ✅ New templates created
- ✅ Existing templates updated with new clauses
- ⚠️ Download or processing errors

Notifications are sent via:
- 📧 **Email** (SMTP)
- 💬 **Slack** (Webhooks - if configured)

### Notification Example
When templates are updated, you'll receive an email like:
```
Subject: 🔄 GDPR Template Update Notification

📝 CHANGES DETECTED:
  • Data Processing Agreement: Template updated with new clauses
  • Standard Contractual Clauses: New template created
```

See `SCRAPING_NOTIFICATION_GUIDE.md` for detailed information.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📝 License

This project is licensed under the MIT License.

## 👥 Support

For questions or support, please contact the development team.

## 🎯 Future Enhancements

- [ ] 🌍 Multi-language support
- [x] 📧 Email notifications for compliance reports ✅
- [ ] 📈 Historical comparison tracking
- [ ] 🔗 Integration with document management systems
- [ ] 📱 Mobile-responsive interface
- [ ] 🎨 Custom template creation
- [ ] 📊 Advanced analytics dashboard
- [ ] 🔔 Webhook support for real-time notifications
- [ ] 📱 SMS notifications

## 📝 Recent Updates

### October 2025 - Security & Notification Enhancements

#### 📧 Scraping Notification System
- **Automatic change detection** for template updates
- Sends email notifications when GDPR templates are updated
- Uses MD5 hash comparison for accurate change detection
- Reports both successful updates and errors
- Fixed JSON file paths (`json_files/` → `json/`)
- Added comprehensive logging and error handling

#### ✅ Notification Module Refactored
- **notification.py** completely rewritten with security best practices
- Moved all hardcoded credentials to `.env` file
- Added reusable `send_email()` function with flexible parameters
- Implemented proper error handling and input validation
- Added comprehensive documentation

#### 🔐 Security Improvements
- All sensitive credentials now in `.env` file:
  - Email credentials (SMTP sender, password, receiver)
  - API keys (Gemini, Groq)
  - Server configuration
- Created `.env.example` as a safe template for team members
- Verified `.gitignore` excludes `.env` from version control

#### 🎯 Code Quality
- Eliminated security risks of hardcoded credentials
- Improved code maintainability and reusability
- Added detailed inline documentation
- Fixed typos and improved code structure
- Follows Python PEP 8 standards

#### 📚 Documentation
- Updated README.md with notification module usage
- Added Gmail App Password setup instructions
- Included environment variable configuration guide
- Provided example workflows for email notifications

---

Made with ❤️ for GDPR Compliance | Powered by 🤖 Google Gemini AI
