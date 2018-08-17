import asyncio
import aioredis
import json
from setting import LOGGER
from pybloom_live import ScalableBloomFilter
import redis

class RedisJob(object):
    _pool = None

    url_filter = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)

    def __init__(self, **kwargs):
        self._host = kwargs['host'] if 'host' in kwargs else 'redis://localhost:6379'
        self._db = kwargs['db'] if 'db' in kwargs else 1
        self._minsize = kwargs['minsize'] if 'minsize' in kwargs else 5
        self._maxsize = kwargs['maxsize'] if 'maxsize' in kwargs else 10
        self._pool_now = None

    async def init_pool(self):
        LOGGER.info("init redis pool (host: %s, db: %d, minsize: %d, maxsize: %d)" %
                    (self._host, self._db, self._minsize, self._maxsize))
        self._pool = await aioredis.create_pool(
            self._host, db=self._db,
            minsize=self._minsize, maxsize=self._maxsize)

    def init_pool_now(self):
        LOGGER.info("init redis pool (host: %s, db: %d, minsize: %d, maxsize: %d)" %
                    (self._host, self._db, self._minsize, self._maxsize))
        self._pool_now= redis.ConnectionPool(host='localhost', port=6379, db=1)

    async def push_job(self, job_type, job_info):
        if not self._pool:
            await self.init_pool()
        url = job_info.get('url', '')
        if url and url in self.url_filter:
            LOGGER.warn("%s job filtered. %s" % (job_type, str(job_info)))
            return
        else:
            self.url_filter.add(url)
        with await self._pool as conn:
            await conn.execute('lpush', str(job_type), json.dumps(job_info))
            LOGGER.info("push %s job into redis: %s" % (job_type, str(job_info)))

    async def fetch_job(self, job_type):
        if not self._pool:
            await self.init_pool()
        with await self._pool as conn:
            job_info = await conn.execute('rpop', job_type)
            if job_info:
                LOGGER.info('fetched job: %s' % job_info)
                return json.loads(job_info)
            else:
                return None

    def fetch_job_now(self, job_type):
        if self._pool_now is None:
            self.init_pool_now()
        with self._pool_now as conn:
            job_info = conn.lpop(job_type)
            if job_info:
                LOGGER.info('fetched job: %s' % job_info)
                return json.loads(job_info)
            else:
                return None

    async def clean(self):
        if not self._pool:
            await self.init_pool()
        with await self._pool as conn:
            keys = await conn.execute('keys', '*')
            for key in keys:
                LOGGER.info("del %s" % key)
                await conn.execute('del', key)


class RedisCookie(object):
    _pool = None

    def __init__(self, **kwargs):
        self._host = kwargs['host'] if 'host' in kwargs else 'redis://localhost:6379'
        self._db = kwargs['db'] if 'db' in kwargs else 0
        self._minsize = kwargs['minsize'] if 'minsize' in kwargs else 5
        self._maxsize = kwargs['maxsize'] if 'maxsize' in kwargs else 10

    async def init_pool(self):
        LOGGER.info("init redis pool (host: %s, db: %d, minsize: %d, maxsize: %d)" %
                    (self._host, self._db, self._minsize, self._maxsize))
        self._pool = await aioredis.create_pool(
            self._host, db=self._db,
            minsize=self._minsize, maxsize=self._maxsize)

    async def fetch_cookies(self):
        if not self._pool:
            await self.init_pool()
        with await self._pool as conn:
            user = await conn.execute('spop', 'users')
            cookies_info = await conn.execute('hget', 'account', user)
            if cookies_info:
                user_cookies = cookies_info.decode('utf-8')
                user_cookies_json = json.loads(user_cookies)
                conn.execute('sadd', 'users', user)
                conn.close()
                return user_cookies_json

    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

    async def test(self):
        print(await self.fetch_cookies())
        print(await self.fetch_cookies())
        await self.close()

