import fitz


def extract_pdf_data(pdf_path):

    document = fitz.open(pdf_path)

    metadata = document.metadata

    pages = []

    for page_num in range(len(document)):

        page = document.load_page(page_num)

        pages.append({
            "page_number": page_num + 1,
            "text": page.get_text()
        })

    result = {
        "metadata": metadata,
        "total_pages": len(document),
        "pages": pages
    }

    document.close()

    return result