all_chunks = []


def save_chunks(
    chunks
):

    global all_chunks

    all_chunks.extend(
        chunks
    )


def get_chunks():

    return all_chunks