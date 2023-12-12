from fastapi import FastAPI, Depends, HTTPException, Body
from redis import Redis, RedisError

app = FastAPI()

def get_redis():
    # Assuming you have a Redis container running on localhost:6379
    # return Redis(host="localhost", port=6379)
    # N.B. Fails due to: "Error 99 connecting to localhost:6379.
    # Cannot assign requested address.".
    # ChatGPT: Might be an issue with the connection to the Redis server in the Docker container.
    # This is likely due to the fact that the Redis server is running on the host machine,
    # but your Docker container is unable to reach it using localhost.
    # To resolve this, you can use the host machine's IP address instead of localhost.
    return Redis(host="192.168.23.242", port=6379)

def set_key_value(redis: Redis, key: str, value: str):
    try:
        redis.set(key, value)
        return {"message": f"Key '{key}' set to '{value}'"}
    except RedisError as e:
        return {"error": str(e)}

def get_value_by_key(redis: Redis, key: str):
    try:
        value = redis.get(key)
        if value:
            return {"message": f"Value for key '{key}': {value.decode('utf-8')}"}
        else:
            return {"message": f"Key '{key}' not found"}
    except RedisError as e:
        return {"error": str(e)}

def update_key_value(redis: Redis, key: str, value: str):
    try:
        # Check if the key exists before updating
        if not redis.exists(key):
            return {"error": f"Key '{key}' not found"}

        redis.set(key, value)
        return {"message": f"Key '{key}' updated to '{value}'"}
    except RedisError as e:
        return {"error": str(e)}

def delete_key(redis: Redis, key: str):
    try:
        # Check if the key exists before deleting
        if not redis.exists(key):
            return {"error": f"Key '{key}' not found"}

        redis.delete(key)
        return {"message": f"Key '{key}' deleted"}
    except RedisError as e:
        return {"error": str(e)}


@app.get("/")
def read_root(redis: Redis = Depends(get_redis)):
    return {"message": "Hello, Redis!"}

@app.get("/get/{key}")
def get_key(redis: Redis = Depends(get_redis), key: str = ""):
    return get_value_by_key(redis, key)

@app.post("/set/{key}/{value}")
def set_key(redis: Redis = Depends(get_redis), key: str = "", value: str = ""):
    return set_key_value(redis, key, value)

@app.post("/set/")
def set_key_from_body(redis: Redis = Depends(get_redis), key_value: dict = Body(...)):
    try:
        key = key_value["key"]
        value = key_value["value"]
        return set_key_value(redis, key, value)
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Key and value must be provided in the request body")

@app.put("/update/{key}")
def update_key(redis: Redis = Depends(get_redis), key: str = "", value: str = Body(...)):
    return update_key_value(redis, key, value)

@app.delete("/delete/{key}")
def delete_key_endpoint(redis: Redis = Depends(get_redis), key: str = ""):
    return delete_key(redis, key)
