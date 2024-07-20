import json
from typing import Union
import redis

from ai_health.root.settings import Settings


settings = Settings()


class RedisManager:
    def __init__(self) -> None:
        self.redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def cache_json_item(self, key: str, value: dict, ttl: int = 3600):
        """
        Caches a JSON Item for some time set with the ttl- time to live.

        After the TTL, it is cleared from the Redis Db.
        Its Expiration date is 3600s (1 Hr) by default
        """
        value_as_string = json.dumps(value)

        self.redis_client.set(name=key, value=value_as_string, ex=ttl)

    def get_cached_json_item(self, key: str) -> Union[dict, None]:
        value = self.redis_client.get(name=key)

        if value is None:
            return None

        # value_decoded = json.loads(str(value))
        value_decoded = json.loads(value)

        return value_decoded

    def delete_key(self, key: str):
        self.redis_client.delete(key)


redis_manager = RedisManager()
