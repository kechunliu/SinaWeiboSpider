# -*- coding: cp936 -*-

from ctypes import *
from setting import LOGGER, ROOT_PATH


class YunDaMa:

    def __init__(self, username, password):
        self.YDMApi = windll.LoadLibrary(ROOT_PATH+'\\dll\\yundamaAPI-x64.dll')
        self.appId = 5064  # 软件id
        self.appKey = b'57f477ba2a00eeb3e2fcb392474305d4'  # 软件密钥
        LOGGER.info('app id：%d\r\napp key：%s' % (self.appId, self.appKey))
        self.username = username.encode()
        self.password = password.encode()
        print(self.username)
        print(self.password)
        self.code_type = 1005
        self.timeout = 60
        self.YDMApi.YDM_SetAppInfo(self.appId, self.appKey)
        self.uid = self.YDMApi.YDM_Login(self.username, self.password)
        balance = self.YDMApi.YDM_GetBalance(self.username, self.password)
        LOGGER.info('succeed to login in YunDaMa, balance : %d', balance)

    def recognize(self, filename):
        if not isinstance(filename, bytes):
            filename = filename.encode()
        print(filename)
        result = c_char_p(b"                              ")
        LOGGER.info('>>>正在登陆...')
        captcha_id = self.YDMApi.YDM_DecodeByPath(filename, self.code_type, result)

        return captcha_id, result.value