def get_parent_chunks(results):
    """
    Converts retrieved child chunks into parent chunks.

    Removes duplicate parents.

    Returns:
        List[str]
    """

    parents = []

    seen = set()

    for result in results:

        payload = result.payload

        parent_id = payload.get("parent_id")

        parent_text = payload.get("parent_text")

        if parent_id in seen:
            continue

        if parent_text is None:
            continue


        seen.add(parent_id)

        parents.append(parent_text)
    return parents