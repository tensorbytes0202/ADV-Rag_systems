import os
import pickle

INDEX_DIR = "app/services/bm25_indexes"

os.makedirs(INDEX_DIR, exist_ok=True)


def save_index(document_name, bm25, chunks):

    path = os.path.join(
        INDEX_DIR,
        f"{document_name}.pkl"
    )

    with open(path, "wb") as f:

        pickle.dump(
            {
                "bm25": bm25,
                "chunks": chunks
            },
            f
        )


def load_index(document_name):

    path = os.path.join(
        INDEX_DIR,
        f"{document_name}.pkl"
    )

    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:

        return pickle.load(f)