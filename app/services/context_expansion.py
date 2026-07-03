def expand_context(results, window_size=1):

    expanded_context = []

    seen = set()

    for result in results:

        payload = result.payload

        parent_text = payload.get("parent_text")

        if not parent_text:
            continue

        if parent_text in seen:
            continue

        seen.add(parent_text)

        expanded_context.append(parent_text)

    return expanded_context