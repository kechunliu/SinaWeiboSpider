import sys
from src.weibo_cn_async_f import WeiboCnSpider
import time

if __name__ == '__main__':
    args = sys.argv[1:]
    # args += 'u'     # 用户
    # args += 't' #话题帖子
    args += 'f' #用户的关注
    # args += 'o'  # 用户的粉丝
    # args += 'a' #话题名人堂
    WeiboCnSpider(tasks=2).start(args)
