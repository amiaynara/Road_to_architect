import subprocess

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
CACHE_TTL_SECONDS = 30


def db_get(key: str) -> str | None:
    result = subprocess.run(
        ["bash", "-c", f"source slow_db.sh; db_get {key}"],
        capture_output=True, text=True,
    )
    value = result.stdout.strip()
    return value or None


def db_set(key: str, value: str) -> None:
    subprocess.run(
        ["bash", "-c", f"source slow_db.sh; db_set {key} {value}"],
        check=True,
    )


def cached_get(key: str) -> str | None:
    # TODO (the crucial part): implement cache-aside reads.
    # 1. Ask redis for the key.
    value = r.get(key)
    # 2. On a hit, print "CACHE HIT" and return it.
    if value:
        print("CACHE HIT")
    # 3. On a miss, print "CACHE MISS", fall back to db_get, populate redis
    else:
        # with r.set(key, value, ex=CACHE_TTL_SECONDS), then return it.
        print("CACHE MISS")
        value = db_get(key)
        r.set(key, value, ex=CACHE_TTL_SECONDS)
    return value



def cached_set(key: str, value: str) -> None:
    # TODO (the crucial part): implement cache-aside writes.
    # writing to cache is also the responsibility of the application code
    db_set(key, value)
    # invalidating the older value of the key is also responsiblity of the application code
    r.delete(key)
    pass


if __name__ == "__main__":
    cached_set("123", "amiay-v1")
    cached_get("123")   # expect: CACHE MISS, then amiay-v1
    cached_get("123")   # expect: CACHE HIT, amiay-v1
    cached_set("123", "amiay-v2")
    cached_get("123")   # expect: CACHE MISS (invalidated), amiay-v2
