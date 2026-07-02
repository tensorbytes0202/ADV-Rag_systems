def get_retrieval_config(query_type):
    """
    Returns retrieval parameters
    based on query type.
    """

    configs = {

        "definition": {

            "dense_top_k": 5,

            "bm25_top_k": 5,

            "compression_top_k": 5,

            "window_size": 1

        },

        "comparison": {

            "dense_top_k": 15,

            "bm25_top_k": 15,

            "compression_top_k": 10,

            "window_size": 2

        },

        "summarization": {

            "dense_top_k": 20,

            "bm25_top_k": 20,

            "compression_top_k": 12,

            "window_size": 2

        },

        "reasoning": {

            "dense_top_k": 20,

            "bm25_top_k": 20,

            "compression_top_k": 15,

            "window_size": 3

        }

    }

    return configs.get(
    query_type.lower(),
    configs["definition"]
)