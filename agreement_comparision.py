from google import genai
from google.genai import types
from pydantic import BaseModel
from enum import Enum
from dotenv import load_dotenv
import PyPDF2
import json
import os

# Load environment variables
load_dotenv()


# ********   Phase 2   ******** #

def document_type(file_path: str) -> str:
    """
    Detect the type of contract document.
    Possible values:
      1. Data Processing Agreement
      2. Joint Controller Agreement
      3. Controller-to-Controller Agreement
      4. Processor-to-Subprocessor Agreement
      5. Standard Contractual Clauses
    """

    class DocumentType(str, Enum):
        DPA = "Data Processing Agreement"
        JCA = "Joint Controller Agreement"
        C2C = "Controller-to-Controller Agreement"
        SubProcessor = "Processor-to-Subprocessor Agreement"
        SCC = "Standard Contractual Clauses"

    class FindDocumentType(BaseModel):
        document_type: DocumentType

    # Extract text from PDF
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    # Initialize Gemini client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Prompt for classification
    prompt = f"""
    You are a legal document classification assistant.

    Task: Identify the type of contract from the list below:
    1. Data Processing Agreement
    2. Joint Controller Agreement
    3. Controller-to-Controller Agreement
    4. Processor-to-Subprocessor Agreement
    5. Standard Contractual Clauses

    Input: {text}

    Respond ONLY in valid JSON format:
    [
      {{
        "document_type": "<one_of_the_above_values>"
      }}
    ]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disable "thinking"
            response_mime_type="application/json",
            response_schema=list[FindDocumentType],
        ),
    )

    # Parse and return the detected document type
    json_object = json.loads(response.text)
    return json_object[0]["document_type"]


def compare_agreements(unseen_data: str, template_data: str) -> str:
    """
    Compare two agreements:
    - Identify missing/altered clauses.
    - Flag GDPR compliance risks.
    - Assign a risk score (0-100).
    - Suggest amendments for compliance.
    """

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
    You are an AI legal assistant specialized in contract review and compliance.

    Compare the two documents below:

    Template (regulatory standard reference):
    {template_data}

    New contract to review:
    {unseen_data}

    ### Tasks:
    1. Identify missing or altered clauses compared to the template.
    2. Flag potential compliance risks under GDPR.
    3. Assign a risk score between 0 and 100 (0 = no risk, 100 = max risk).
    4. Provide reasoning for the risk score.
    5. Suggest amendments/recommendations for compliance.

    ### Response Format:
    - Missing Clauses: [...]
    - Potential Compliance Risks: [...]
    - Risk Score (0-100): ...
    - Reasoning: [...]
    - Recommendations: [...]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disable "thinking"
            temperature=0.3,
        ),
    )

    return response.text


if __name__ == "__main__":
    # Example usage
    doc_type = document_type("GDPR-Sample-Agreement.pdf")
    print(f"📄 Document Type: {doc_type}")

    # Example comparison (replace with actual data)
    unseen = "New contract text goes here..."
    template = "Template contract text goes here..."
    comparison_result = compare_agreements(unseen, template)
    print(comparison_result)
