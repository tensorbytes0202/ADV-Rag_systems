from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import time
import json

router = APIRouter()


@router.post("/query/stream")
def stream_answer():

    answer = """
A process is a program in execution. It requires CPU time,
memory, files and I/O resources to perform its task.

Processes are the basic unit of execution in an operating system.
"""

    def generate():

        words = answer.split()

        for word in words:

            yield json.dumps({

                "token": word + " "

            }) + "\n"

            time.sleep(0.04)

    return StreamingResponse(

        generate(),

        media_type="application/x-ndjson"

    )