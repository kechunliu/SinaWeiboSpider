import base64
import json
import os
import random
from time import sleep

import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    InvalidElementStateException

import setting
import user_agents
from code_recognize import YunDaMa
from setting import LOGGER, PROPERTIES


# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# driver = webdriver.PhantomJS(desired_capabilities=dcap)


class WeiboLogin:

    def __init__(self):
        self.yun_da_ma = YunDaMa(username=PROPERTIES['yundama']['user'], password=PROPERTIES['yundama']['password'])

    @staticmethod
    def get_cookie_from_login_sina_com_cn(account, password):
        """ 获取一个账号的Cookie """
        login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
        headers = {
            'Referer': 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)',
            'Upgrade-Insecure-Requests': '1',
            'Host': 'login.sina.com.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        post_data = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(login_url, headers=headers, data=post_data, verify=False)
        json_str = r.content.decode("gbk")
        info = json.loads(json_str)
        LOGGER.info('get cookies for %s' % account)
        if info["retcode"] == "0":
            LOGGER.info("Get Cookie Success!( Account:%s )" % account)

            cookies = session.cookies.get_dict()
            for k, v in cookies.items():
                print(k, v)
            return cookies
        else:
            LOGGER.warning("Get Cookie failed!( Account:%s )" % account)
            LOGGER.warning(info)
            return None

    @staticmethod
    def get_cookies_ffrom_weibo_cn(username, password):
        head = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '254',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'passport.weibo.cn',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?'
                       'entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
            'User-Agent': user_agents.USER_AGENTS[random.randint(0, len(user_agents.USER_AGENTS) - 1)]
        }
        setting.LOGGER.info(username + ' login')
        args = {
            'username': username,
            'password': password,
            'savestate': 1,
            'ec': 1,
            'r': 'http://weibo.cn/?featurecode=20000320&luicode=20000174&lfid=hotword',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'hff': '',
            'hfp': ''
        }
        session = requests.Session()
        response = session.post(setting.LOGIN_URL, data=args, headers=head, verify=False)
        print(response.text)
        cookies = {}
        for cookie in session.cookies:
            print(cookie.name, cookie.value)
            cookies[cookie.name] = cookie.value
        return cookies

    @staticmethod
    def save_verify_code_img(browser, weibo_user):

        screen_shot_path = 'D:\\ImageTemp\\img\\%s-screenshot.png' % weibo_user
        code_img_path = 'D:\\ImageTemp\\img\\%s-verify_code.png' % weibo_user
        LOGGER.info('get verify code img for %s' % weibo_user)
        browser.save_screenshot(screen_shot_path)
        code_img = browser.find_element_by_xpath('//img[@node-type="verifycode_image"]')
        left = code_img.location['x']
        top = code_img.location['y']
        right = code_img.location['x'] + code_img.size['width']
        bottom = code_img.location['y'] + code_img.size['height']
        # print(left, top, right, bottom)
        picture = Image.open(screen_shot_path)
        picture = picture.crop((1525, 360, 1646, 404))
        #picture = picture.crop((left, top, right, bottom))
        picture.save(code_img_path)
        os.remove(screen_shot_path)
        LOGGER.info('code img saved(%s)' % code_img_path)
        return code_img_path

    def login_by_selenium(self, weibo_user, weibo_password):
        browser = webdriver.Firefox()
        browser.maximize_window()
        try_time = 10
        cookie_got = False
        browser.get('https://weibo.com/login.php')
        username = browser.find_element_by_id("loginname")
        username.clear()
        username.send_keys(weibo_user)
        psd = browser.find_element_by_xpath('//input[@type="password"]')
        psd.clear()
        psd.send_keys(weibo_password)
        commit_btn = browser.find_element_by_xpath('//a[@node-type="submitBtn"]')
        commit_btn.click()
        # 没那么快登录成功

        while try_time:
            try:
                # 如果登录不成功是有验证码框的
                browser.find_element_by_xpath('//div[@node-type="verifycode_box"]')
                code_input = browser.find_element_by_xpath('//input[@node-type="verifycode"]')
                LOGGER.info("need input verify code")
                code_input.send_keys('  ')
                img_path = self.save_verify_code_img(browser, weibo_user)

                while not os.path.exists(img_path):
                    LOGGER.info(img_path + "not exist")
                    sleep(1)
                    LOGGER.info(img_path)

                captcha_id, code_text = self.yun_da_ma.recognize(img_path)
                # os.remove(img_path)
                code_str = bytes.decode(code_text)
                LOGGER.info('recognize result: %s' % code_str)

                code_input.clear()
                code_input.send_keys(code_str)
                commit_btn = browser.find_element_by_xpath('//a[@node-type="submitBtn"]')
                commit_btn.click()
                # 稍等一会
                sleep(3)
                try_time -= 1
            except (StaleElementReferenceException, NoSuchElementException):

                cookie_got = True
                print('login success')
                break
            except InvalidElementStateException:
                sleep(2)
                try_time -= 1
            # except ElementNotInteractableException:
            #     sleep(2)
            #     try_time -= 1
        if cookie_got:
            sleep(2)
            LOGGER.info('get https://weibo.cn/1316949123/info')
            browser.get('https://weibo.cn/1316949123/info')
            sleep(2)
            cookies_dict = {}
            for elem in browser.get_cookies():
                cookies_dict[elem['name']] = elem['value']
                print(elem["name"], elem["value"])
            # RedisCookies.save_cookies(weibo_user, cookies_dict)
            browser.close()
            return cookies_dict
        else:
            browser.close()
            LOGGER.error("get cookie failed :%s" % weibo_user)
            return None