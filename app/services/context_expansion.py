from app.services.chunk_store import get_parent_chunks


def expand_context(results, window_size=1):
    """
    Expand retrieved parent chunks by including
    previous and next parent chunks.

    window_size = 1

    Parent-1
    Parent
    Parent+1
    """

    parents = get_parent_chunks()

    if not parents:
        return []

    # Fast lookup
    parent_map = {}

    for index, parent in enumerate(parents):
        parent_map[parent["parent_id"]] = index

    expanded_context = []

    added = set()

    for result in results:

        payload = result.payload

        parent_id = payload.get("parent_id")

        if parent_id not in parent_map:
            continue

        current_index = parent_map[parent_id]

        start = max(
            0,
            current_index - window_size
        )

        end = min(
            len(parents),
            current_index + window_size + 1
        )

        for i in range(start, end):

            pid = parents[i]["parent_id"]

            if pid in added:
                continue

            added.add(pid)

            expanded_context.append(
                parents[i]["parent_text"]
            )

    return expanded_context