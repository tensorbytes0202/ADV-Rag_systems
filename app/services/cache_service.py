import json
import hashlib
import redis

from app.core.settings import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


def make_cache_key(question: str):

    return hashlib.sha256(

        question.lower().strip().encode()

    ).hexdigest()


def get_cache(question: str):

    key = make_cache_key(question)

    data = redis_client.get(key)

    if data:

        print("✅ CACHE HIT")

        return json.loads(data)

    print("❌ CACHE MISS")

    return None


def set_cache(question: str, response):

    key = make_cache_key(question)

    redis_client.setex(

        key,

        settings.CACHE_TTL,

        json.dumps(response)

    )


def clear_cache(question: str):

    key = make_cache_key(question)

    redis_client.delete(key)