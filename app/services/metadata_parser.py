import re


OS_BOOK = "Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf"


def extract_metadata(question: str):

    metadata = {
        "page": None,
        "document_name": None
    }

    question_lower = question.lower()

    # ==========================================
    # PAGE DETECTION
    # ==========================================

    page_patterns = [

        r"page\s+(\d+)",

        r"pg\s+(\d+)",

        r"page\s*:\s*(\d+)",

        r"page#(\d+)",

    ]

    for pattern in page_patterns:

        match = re.search(
            pattern,
            question_lower
        )

        if match:

            metadata["page"] = int(
                match.group(1)
            )

            break

    # ==========================================
    # DOCUMENT DETECTION
    # ==========================================

    if any(keyword in question_lower for keyword in [

        "operating system",

        "operating systems",

        "os book",

        "silberschatz",

        "abraham"

    ]):

        metadata["document_name"] = OS_BOOK

    # ==========================================
    # Direct PDF Name Detection
    # ==========================================

    pdf_match = re.search(

        r'([A-Za-z0-9_\- ]+\.pdf)',

        question,

        re.IGNORECASE

    )

    if pdf_match:

        metadata["document_name"] = pdf_match.group(1)

    return metadata