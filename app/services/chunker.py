from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_parent_child_chunks(text):
    """
    Creates Parent-Child chunks.

    Returns:

    [
        {
            "parent_id": 0,
            "parent_text": "...",
            "children": [
                {
                    "child_id": 0,
                    "text": "..."
                },
                {
                    "child_id": 1,
                    "text": "..."
                }
            ]
        }
    ]
    """

    # -----------------------------
    # Parent Splitter
    # -----------------------------
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=300,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    # -----------------------------
    # Child Splitter
    # -----------------------------
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    # -----------------------------
    # Split into Parent Chunks
    # -----------------------------
    parent_chunks = parent_splitter.split_text(text)

    documents = []

    # -----------------------------
    # Create Child Chunks
    # -----------------------------
    for parent_index, parent in enumerate(parent_chunks):

        child_chunks = child_splitter.split_text(parent)

        children = []

        for child_index, child in enumerate(child_chunks):

            children.append(
                {
                    "child_id": child_index,
                    "text": child
                }
            )

        documents.append(
            {
                "parent_id": parent_index,
                "parent_text": parent,
                "children": children
            }
        )

    return documents