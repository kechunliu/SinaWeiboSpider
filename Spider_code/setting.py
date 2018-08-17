import yaml
import platform
import logging
import logging.config
import os

# 多线程线程数
THREAD_NUM = 2


def logger_conf():
    """
    load basic logger configure
    :return: configured logger
    """

    if platform.system() == 'Windows':
        logging.config.fileConfig(os.path.split(os.path.realpath(__file__))[0]+'\\conf\\logging.conf')
    elif platform.system() == 'Linux':
        logging.config.fileConfig(os.path.split(os.path.realpath(__file__))[0]+'/conf/logging.conf')
    elif platform.system() == 'Darwin':
        logging.config.fileConfig(os.path.split(os.path.realpath(__file__))[0] + '/conf/logging.conf')
    logger = logging.getLogger('simpleLogger')

    return logger

if __name__ == 'setting':
    ROOT_PATH = os.path.split(os.path.realpath(__file__))[0]
    LOGGER = logger_conf()
    PROPERTIES = yaml.load(open(os.path.split(os.path.realpath(__file__))[0] + '/conf/account.yaml'))
    ACCOUNTS = PROPERTIES.get('accounts')