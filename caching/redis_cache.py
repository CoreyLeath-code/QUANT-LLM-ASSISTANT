import redis
import hashlib
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def generate_key(query):
    return hashlib.sha256(query.encode()).hexdigest()

def get_cached(query):
    key = generate_key(query)
    result = redis_client.get(key)
    return json.loads(result) if result else None

def set_cache(query, response):
    key = generate_key(query)
    redis_client.setex(key, 300, json.dumps(response))
