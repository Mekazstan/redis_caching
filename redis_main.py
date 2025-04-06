import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def call_redis():
    try:
        r.ping()
        print("Successfully connected to Redis!")
        # Your caching logic here
    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}")
    