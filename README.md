# SinaWeiboSpider
新浪微博爬虫，功能包括：爬取用户信息、关注、粉丝，爬取超级话题用户及粉丝相关信息

示例：爬取“创造101”超级话题#聚众赏花#的用户与粉丝信息

## 实现框架及细节

<p align="center">
<img src="https://github.com/kechunliu/SinaWeiboSpider/blob/master/SpiderFramework.jpg" width="750">
</p>

1)	获取微博cookie，模拟登录
在爬取微博网页的时候，需要模拟登录状态，因此需要获取微博登录的cookie。为了防止因访问过于频繁而被封，我注册了八个微博账号，轮流爬取微博网页。由于cookie可能会过期，所以在开始爬取网页前需要先运行redis_cookies.py来获取当时的微博cookie。

2)	初始化任务
在实现过程中，我利用asyncio和redis模块实现了多线程异步IO，其中asyncio是python的多线程模块，而redis则是一个key-value数据库，用于存储网页url和相应的任务名。
针对超级话题用户的爬虫任务，在初始化的时候将指定页数（默认为500页）的网页URL push到Redis中，任务名为topic。
针对超级话题粉丝的爬虫任务，在初始化的时候将指定页数（默认为500页）的网页URL push到Redis中，任务名为superfan。

3)	Kafka和爬虫
在爬虫爬取过程中，利用Redis实现类似栈的push和pop过程，在不同的任务中pop出指定任务名的网页URL，用户信息任务名为user，关注列表任务名为follower，粉丝列表任务名为fan。
在记录爬虫爬取到的内容的过程中，我使用了分布式消息系统Kafka，Kafka的结构图如下：
 <p align="center">
<img src="https://github.com/kechunliu/SinaWeiboSpider/blob/master/kafka.png" width="500">
</p>
在解析json文件获取到相应信息后，在weiboasync.py中由producer将数据发至指定topic的broker中，后在consumer.py中由consumer从指定topic的broker中获得相应数据存储成json文件，以供后续数据分析。
