import json
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_embedding(question: str):

    key = f"embedding:{question}"

    data = redis_client.get(key)

    if data:

        print("✅ EMBEDDING CACHE HIT")

        return json.loads(data)

    print("❌ EMBEDDING CACHE MISS")

    return None


def set_embedding(question: str, embedding):

    key = f"embedding:{question}"

    redis_client.set(

        key,

        json.dumps(embedding),

        ex=86400

    )