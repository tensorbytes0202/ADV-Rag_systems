import ollama
from groq import Groq

from app.core.settings import settings


# ==========================================================
# Config
# ==========================================================

LLM_PROVIDER = settings.LLM_PROVIDER.lower()
DEFAULT_MODEL = settings.LLM_MODEL


# ==========================================================
# Clients
# ==========================================================

groq_client = None

if LLM_PROVIDER == "groq":

    groq_client = Groq(
        api_key=settings.GROQ_API_KEY
    )


# ==========================================================
# Universal Chat Function
# ==========================================================

def chat(

    messages,

    stream=False,

    temperature=0,

    model=None,

    **kwargs

):

    model_name = model or DEFAULT_MODEL

    # ======================================================
    # OLLAMA
    # ======================================================

    if LLM_PROVIDER == "ollama":

        options = {

            "temperature": temperature

        }

        options.update(kwargs)

        return ollama.chat(

            model=model_name,

            messages=messages,

            options=options,

            stream=stream

        )

    # ======================================================
    # GROQ
    # ======================================================

    elif LLM_PROVIDER == "groq":

        completion = groq_client.chat.completions.create(

            model=model_name,

            messages=messages,

            temperature=temperature,

            stream=stream

        )

        # Return raw stream object
        if stream:

            return completion

        # Normal response
        return {

            "message": {

                "content": completion.choices[0].message.content

            }

        }

    # ======================================================
    # Unsupported Provider
    # ======================================================

    else:

        raise ValueError(

            f"Unsupported LLM Provider: {LLM_PROVIDER}"

        )