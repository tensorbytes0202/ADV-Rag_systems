import json
import os
from app.core.settings import settings
from app.services.vector_store import client, COLLECTION_NAME
REGISTRY_FILE=settings.REGISTRY_FILE




def is_collection_available():

    collections = client.get_collections()

    names = [

        c.name

        for c in collections.collections

    ]

    return COLLECTION_NAME in names


def load_registry():

    if not os.path.exists(REGISTRY_FILE):

        return {}

    with open(REGISTRY_FILE, "r") as f:

        return json.load(f)


def save_registry(registry):

    with open(REGISTRY_FILE, "w") as f:

        json.dump(
            registry,
            f,
            indent=4
        )


def is_document_indexed(document_name):

    registry = load_registry()

    return document_name in registry


def register_document(
    document_name,
    pages,
    chunks
):

    registry = load_registry()

    registry[document_name] = {

        "pages": pages,

        "chunks": chunks

    }

    save_registry(registry)

    # First uploaded document becomes active
    set_active_document(document_name)


def get_documents():

    registry = load_registry()

    documents = []

    for name, info in registry.items():

        documents.append({

            "name": name,

            "pages": info["pages"],

            "chunks": info["chunks"]

        })

    return documents

ACTIVE_FILE= settings.ACTIVE_DOCUMENT_FILE


def set_active_document(document_name):

    with open(ACTIVE_FILE, "w") as f:

        json.dump(
            {
                "active_document": document_name
            },
            f,
            indent=4
        )


def get_active_document():

    if not os.path.exists(ACTIVE_FILE):
        print("No active document found")
        return None

    with open(ACTIVE_FILE, "r") as f:
        data = json.load(f)

    print("=" * 50)
    print("ACTIVE DOCUMENT FROM FILE")
    print(data)
    print("=" * 50)

    return data.get("active_document")