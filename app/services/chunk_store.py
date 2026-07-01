# ==========================================================
# CHILD CHUNKS
# ==========================================================

all_chunks = []

# ==========================================================
# PARENT CHUNKS
# ==========================================================

parent_chunks = []


# ==========================================================
# SAVE CHILD CHUNKS
# ==========================================================

def save_chunks(chunks):

    global all_chunks

    all_chunks.extend(chunks)


# ==========================================================
# GET CHILD CHUNKS
# ==========================================================

def get_chunks():

    return all_chunks


# ==========================================================
# SAVE PARENT CHUNKS
# ==========================================================

def save_parent_chunks(parents):

    global parent_chunks

    parent_chunks.extend(parents)


# ==========================================================
# GET PARENT CHUNKS
# ==========================================================

def get_parent_chunks():

    return parent_chunks


# ==========================================================
# GET PARENT BY ID
# ==========================================================

def get_parent(parent_id):

    for parent in parent_chunks:

        if parent["parent_id"] == parent_id:
            return parent

    return None