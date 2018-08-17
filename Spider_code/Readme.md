**Init** 
	
	初始化，（会清零redis上的内存，除了cookies)，之后会把找帖子里面的用户的任务添进redis(话题帖子的1-500页）（t|a)

**Start**

	1.可以修改， 有u的话，爬用户，有f的话，爬用户的follow，有t的话，爬topic的帖子，有a的话，爬topic的名人堂

	2.爬用户会把用户的很多信息爬出来，并且开始把该用户的关注任务给添进redis,在kafka上输出用户信息,kafka输出的都为json,
	  用户输出的type对应的value为user_info,source会说明该用户是来自哪里,comment是来自topic的帖子区，super是来自名人堂
	  
	3.爬f，会输出该用户的follow_list,值在fans_id里面，fans_id也是一个dict,fans_id里面的key的value为关注的用户的id,
	  follow_list的uid为被爬用户的id
	  
	4.爬topic的帖子的话，会自动把帖子的用户给添加进redis,（只设置了爬帖子的1-500页，可以修改）
	
	5.爬topic的名人堂与4类似
	
	6.主要代码在/src/weibo_cn_async里面
	
/src/redis_cookies - 为串行实现redis操作，及cookies操作的代码

/src/weibo_redis   - 为并行实现redis操作，及cookies操作的代码

consumer.py - 可以从零开始获取kafka的数据，数据存在/json/data.json里面

consumer_with_offset - 通过groupID来获取kafka的数据（再次使用该代码的时候，会从上次结束的地方开始）

code_recognize   -   实现获取验证码的代码，用的云打码（每次验证要1分钱左右）

/conf/account.yaml 存了微博密码与云打码的密码


当微博用户多的时候，start.py的task可以增多
大概100个的时候，可以开10个吧

## Usage

1.先打开zkserver
*cmd:
zkserver*

2.再打开kafka-server
*cmd:
cd /d G:\爬虫\kafka\kafka_2.10-0.10.2.1
.\bin\windows\kafka-server-start.bat .\config\server.properties*

上面两个用之前请设置好
可参照https://www.cnblogs.com/mrblue/p/6425309.html
（1-3步就行，但是他2和3步的dataDir与log.dirs的值不应该是\而是/）

3.运行/src/redis_cookies.py  获取cookies

4.运行 init.py

5.运行 start.py

6.运行 consumer或者consumer_with_offset（可以和5同时）

可以修改的地方：
consumer存了比较多的json的时候可以换个文件来存，看需求了
用户爬出来的信息比较多，可以适当减少
weibo_cn_async很多代码没有用上





	
