"""
data_extraction.py
-------------------
Handles contract analysis (Phase 1 & Phase 2):
- Extracts clauses (full or summarised)
- Detects document type (DPA, JCA, etc.)
- Saves output in JSON inside `json/` folder
"""

import os
import re
import json
from dotenv import load_dotenv
from pypdf import PdfReader
from pydantic import BaseModel
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Ensure output folder exists
JSON_DIR = "json"
os.makedirs(JSON_DIR, exist_ok=True)


# -------------------------------
# Helpers
# -------------------------------

def clean_json(raw_text: str) -> str:
    """Cleans LLM output to ensure valid JSON."""
    raw_text = re.sub(r"^```(?:json)?", "", raw_text, flags=re.IGNORECASE).strip()
    raw_text = re.sub(r"```$", "", raw_text).strip()

    try:
        parsed = json.loads(raw_text)
        return json.dumps(parsed, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        print("⚠️ Warning: Response is not valid JSON. Returning raw output.")
        return raw_text


def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads a PDF and extracts text from all pages."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def get_genai_client() -> genai.Client:
    """Returns a configured Gemini API client."""
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# -------------------------------
# Clause Extraction
# -------------------------------

def clause_extraction(pdf_path: str) -> str:
    """Extracts clauses with full text (no summarisation)."""
    text = extract_text_from_pdf(pdf_path)

    class ClauseExtraction(BaseModel):
        clause_id: str
        heading: str
        text: str

    prompt = f"""
    You are an expert in legal contract analysis.
    Extract all clauses from the following contract text.

    Response format:
    [
        {{
            "clause_id": "<id>",
            "heading/title": "<heading>",
            "full text": "<clause text>"
        }}
    ]
    Input: {text}
    """

    client = get_genai_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[ClauseExtraction],
            temperature=0,
        ),
    )

    return clean_json(response.text)


def clause_extraction_with_summarisation(pdf_path: str) -> str:
    """Extracts clauses with summarised text."""
    text = extract_text_from_pdf(pdf_path)

    class ClauseExtraction(BaseModel):
        clause_id: str
        heading: str
        summarised_text: str

    prompt = f"""
    You are an expert in legal contract analysis.
    Extract all clauses and provide a summary.

    Response format:
    [
        {{
            "clause_id": "<id>",
            "heading/title": "<heading>",
            "summarised_text": "<summary>"
        }}
    ]
    Input: {text}
    """

    client = get_genai_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[ClauseExtraction],
            temperature=0,
        ),
    )

    return clean_json(response.text)


# -------------------------------
# Save Analysis
# -------------------------------

def save_analysis(result: str, filename: str) -> str:
    """Saves analysis JSON to `json/filename`."""
    out_path = os.path.join(JSON_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"✅ Analysis saved to {out_path}")
    return out_path


# -------------------------------
# Script Entry
# -------------------------------
if __name__ == "__main__":
    # Example: process ONE template PDF
    pdf_file = "templates/(Subprocessing Contract) Personal-Data-Sub-Processor-Agreement-2024-01-24.pdf"       # change this file per run
    json_file = "PSA.json"               # choose matching json name

    print(f"📄 Processing {pdf_file}...")
    result = clause_extraction_with_summarisation(pdf_file)
    save_analysis(result, json_file)
