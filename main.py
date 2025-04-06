from redis_main import r, call_redis
from fastapi import FastAPI
from contextlib import asynccontextmanager
import httpx
import json

async def startup_event(app):
    print("Application startup logic here...")
    # Initialize resources, connect to databases, etc.
    app.state.redis = r
    call_redis()
    app.state.http_client = httpx.AsyncClient()

async def shutdown_event(app):
    print("Application shutdown logic here...")
    # Clean up resources, close connections, etc.
    app.state.redis.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event(app)
    yield
    await shutdown_event(app)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Caching with Redis": "Caching data to speed up rate of response using redis"}

@app.get("/entries")
async def read_items():
    try:
        value = json.loads(app.state.redis.get("joke"))
    except:
        response = await app.state.http_client.get("https://official-joke-api.appspot.com/random_joke")
        value = response.json()
        data_str = json.dumps(value)
        app.state.redis.set("joke", data_str)
    
    return value
