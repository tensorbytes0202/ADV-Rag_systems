import ollama


from app.core.settings import settings
MODEL_NAME = settings.LLM_MODEL


def chat(

    messages,

    stream=False,

    temperature=0,

    **kwargs

):

    options = {

        "temperature": temperature

    }

    options.update(kwargs)

    return ollama.chat(

        model=MODEL_NAME,

        messages=messages,

        options=options,

        stream=stream

    )