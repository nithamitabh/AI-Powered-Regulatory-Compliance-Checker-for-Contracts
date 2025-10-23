import agreement_comparision
import data_extraction
import json
import os


# Map agreement type to filenames
PDF_TEMPLATES = {
    "Data Processing Agreement": "DPA.pdf",
    "Joint Controller Agreement": "JCA.pdf",
    "Controller-to-Controller Agreement": "CCA.pdf",
    "Processor-to-Subprocessor Agreement": "PSA.pdf",
    "Standard Contractual Clauses": "SCC.pdf",
}

JSON_TEMPLATES = {
    "Data Processing Agreement": "DPA.json",
    "Joint Controller Agreement": "JCA.json",
    "Controller-to-Controller Agreement": "CCA.json",
    "Processor-to-Subprocessor Agreement": "PSA.json",
    "Standard Contractual Clauses": "SCC.json",
}


def build_template_library():
    """
    Run once to generate JSON standards for all PDFs in templates/.
    Stores them in standards/ folder.
    """
    os.makedirs("standards", exist_ok=True)

    for doc_type, pdf_name in PDF_TEMPLATES.items():
        pdf_path = os.path.join("templates", pdf_name)
        json_path = os.path.join("standards", JSON_TEMPLATES[doc_type])

        if os.path.exists(json_path):
            print(f"✅ {doc_type} already exists at {json_path}, skipping.")
            continue

        print(f"📄 Extracting standard for {doc_type}...")

        # use summarization for Data Processing Agreement, normal for others
        extractor = (
            data_extraction.clause_extraction_with_summarization
            if doc_type == "Data Processing Agreement"
            else data_extraction.clause_extraction
        )

        extracted_data = extractor(pdf_path)

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(extracted_data)

        print(f"✅ Saved {doc_type} standard → {json_path}")


def run_pipeline(unseen_file: str):
    """
    Compare an unseen agreement against its corresponding standard template.
    """

    # Step 1: Detect type
    agreement_type = agreement_comparision.document_type(unseen_file)
    print(f"\n📄 Detected Document Type: {agreement_type}")

    # Step 2: Extract clauses from unseen doc
    extractor = (
        data_extraction. clause_extraction_with_summarisation
        if agreement_type == "Data Processing Agreement"
        else data_extraction.clause_extraction
    )
    unseen_data = extractor(unseen_file)

    # Step 3: Load standard JSON
    template_file = os.path.join("json", JSON_TEMPLATES[agreement_type])
    if not os.path.exists(template_file):
        raise FileNotFoundError(
            f"❌ Standard template JSON for {agreement_type} not found! Run build_template_library() first."
        )

    with open(template_file, "r", encoding="utf-8") as f:
        template_data = json.load(f)

    # Step 4: Compare
    print(f"\n🔎 Comparing unseen doc with standard {agreement_type} ...")
    result = agreement_comparision.compare_agreements(unseen_data, template_data)
    print("\n✅ Comparison Complete")

    return result


if __name__ == "__main__":
    # Step 1 (run once): build template library
    # build_template_library()

    # Step 2: run pipeline for a new document
    unseen_file = "Data-Processing-Agreement-Template.pdf"
    comparison_result = run_pipeline(unseen_file)
    print(comparison_result)
