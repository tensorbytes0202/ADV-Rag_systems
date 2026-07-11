# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse

# from app.api.query import QueryRequest

# from app.services.query_rewriter import rewrite_query
# from app.services.query_classifier import classify_query

# from app.services.retrieval_service import retrieve_context
# from app.services.context_expansion import expand_context
# from app.services.context_compression import compress_context

# from app.services.generation_service import stream_answer

# router = APIRouter()


# @router.post("/query/stream")
# async def query_stream(request: QueryRequest):

#     rewritten_question = rewrite_query(
#         request.question
#     )

#     query_type = classify_query(
#         rewritten_question
#     )

#     retrieved = retrieve_context(
#         rewritten_question
#     )

#     expanded = expand_context(
#         retrieved
#     )

#     compressed = compress_context(
#         expanded
#     )

#     context = "\n\n".join(

#         chunk["text"]

#         for chunk in compressed

#     )

#     def generate():

#         for token in stream_answer(

#             rewritten_question,

#             context,

#             query_type

#         ):

#             yield token

#     return StreamingResponse(

#         generate(),

#         media_type="text/plain"

#     )