import redis as r
import os

from redis.client import Redis

REDIS_HOST_ENV = 'CACHE_HOST'
REDIS_PORT_ENV = 'CACHE_PORT'
REDIS_PASS_ENV = 'CACHE_PASS'
REDIS_EXP_ENV = os.environ['CACHE_EXPIRATION_SECONDS']


def get_redis_client() -> Redis:
    host = os.environ[REDIS_HOST_ENV]
    passwd = os.environ[REDIS_PASS_ENV]
    port = os.environ[REDIS_PORT_ENV]
    return r.Redis(host=host, port=int(port), password=passwd)


# class CacheService:
#     db_client = None
#
#     def push(self, key, value):
#         pass
#
#     def read(self, key):
#         pass
#
#     def if_exist(self, key):
#         pass
#
#     def check_healt(self):
#         pass
#
#     def close(self):
#         pass


class RedisCache:
    db_client = get_redis_client()

    def push(self, key, value):
        self.db_client.set(key, value, ex=int(REDIS_EXP_ENV))
        return

    def if_exist(self, key):
        return self.db_client.exists(key)

    def read(self, key):
        return self.db_client.get(key)

    def check_healt(self):
        try:
            self.db_client.ping()
            return True, 'Redis cache service is healthy'
        except r.ConnectionError:
            return False, 'Unable to connect to Redis cache service'

    def close(self):
        self.db_client.close()
