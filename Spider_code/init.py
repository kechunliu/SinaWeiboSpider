import sys
from src.weibo_cn_async import WeiboCnSpider,JobType
import time
import redis

if __name__ == '__main__':
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
    r = redis.Redis(connection_pool=redis_pool)
    for jobtype in JobType:
        r.delete(jobtype.value)
    args = sys.argv[1:]
    args += 'i'
    # args += 'n'
    WeiboCnSpider(tasks=1).start(args)

