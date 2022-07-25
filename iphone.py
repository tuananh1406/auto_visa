#!/usr/local/bin/python
# coding: utf-8
'''Tự động đăng nhập facebook
'''
import os
import logging

from time import sleep

from datetime import datetime

from configparser import ConfigParser
from webdriver_manager.chrome import ChromeDriverManager
import sentry_sdk

import winsound

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class CustomLogFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'cookies_name'):
            record.cookies_name = EXTRA.get('cookies_name')
        return True


EXTRA = dict(cookies_name=None)
TESTING = None
# URL = 'https://gleam.io/L8Tok/lixinft-giveaway'
URL = 'https://online.immi.gov.au'
NAME = 'tool_auto'


def thiet_lap_logging(name):
    sentry_sdk.init(
        'https://2e084979867c4e8c83f0b3b8062afc5b@o1086935.'
        'ingest.sentry.io/6111285',
        traces_sample_rate=1.0,
    )

    log_format = ' - '.join([
        '%(asctime)s',
        '%(name)s',
        '%(levelname)s',
        # '%(cookies_name)s',
        '%(message)s',
    ])
    formatter = logging.Formatter(log_format)
    file_handles = logging.FileHandler(
        filename='%s.log' % (datetime.now().strftime("%d-%m-%Y")),
        mode='a',
        encoding='utf-8',
    )
    file_handles.setFormatter(formatter)

    syslog = logging.StreamHandler()
    syslog.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addFilter(CustomLogFilter())

    logger.addHandler(syslog)
    if not TESTING:
        logger.addHandler(file_handles)

    return logger


def tam_ngung_den_khi(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath
    '''
    _tam_ngung = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            _xpath,
        )),
    )
    return _tam_ngung


def tam_ngung_va_tim(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath và chọn xpath đó
    '''
    tam_ngung_den_khi(driver, _xpath)
    return driver.find_element(by='xpath', value=_xpath)


def chay_trinh_duyet(headless=True):
    '''Mở trình duyệt và trả về driver
    '''
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    LOGGER.info('Chạy trình duyệt, headless=%s', headless)
    _driver = webdriver.Chrome(
        options=options,
        service=service,
    )
    # Hàm đặt thời gian tải trang, dùng khi tải trang quá lâu
    # _driver.set_page_load_timeout(5)
    return _driver


def mo_website(_driver, url):
    '''Mở thử website
    '''
    if os.path.exists('tele.conf'):
        LOGGER.info('Load config')
        CONFIG = ConfigParser()
        CONFIG.read('tele.conf')
        BOT_TELE = CONFIG.get('config', 'BOT_TELE')
        CHAT_ID = CONFIG.get('config', 'CHAT_ID')

    # Mở trang
    _driver.get(url)

    # Dang nhap
    LOGGER.info('Load user config')
    user = CONFIG.get('user_1_config', 'USER')
    pass_ = CONFIG.get('user_1_config', 'PASS')
    username = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div/div[1]/div[1]/div/input',
    )
    username.send_keys(user)
    password = _driver.find_element(
        by='xpath',
        value='/html/body/form/div/div[1]/div[2]/div/input',
    )
    password.send_keys(pass_)
    login = _driver.find_element(
        by='xpath',
        value='/html/body/form/div/div[2]/button[2]',
    )
    login.click()
    nut_continue = tam_ngung_va_tim(_driver, '/html/body/form/div/div/button')
    nut_continue.click()
    nut_edit = tam_ngung_va_tim(
        _driver,
        '/html/body/form/section/div/div/div[3]/div/div[2]/div/div/div[2]/'
        'div/div[2]/div/div/div[2]/div/div/div[1]/div/div/button')
    nut_edit.click()
    nut_next = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/div[7]/'
        'div/div/div/div[2]/button/span/span')
    nut_next.click()
    nut_next = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/div[7]/'
        'div/div/div/div[2]/button')
    trang_hien_tai = _driver.find_element(
        by='xpath',
        value='/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
        'div[3]/div/div/div/span')
    LOGGER.info(trang_hien_tai.text)
    nut_next = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/div[7]/div'
        '/div/div/div[2]/button/span/span')
    nut_next.click()
    nut_next = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/div[7]/div'
        '/div/div/div[2]/button/span/span')
    trang_hien_tai = _driver.find_element(
        by='xpath',
        value='/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
        'div[3]/div/div/div/span')
    LOGGER.info(trang_hien_tai.text)
    nut_next.click()
    nut_next = tam_ngung_va_tim(
        _driver,
        '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/div[7]/div/'
        'div/div/div[2]/button/span/span')
    trang_hien_tai = _driver.find_element(
        by='xpath',
        value='/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
        'div[3]/div/div/div/span')
    LOGGER.info(trang_hien_tai.text)
    nut_next.click()
    while True:
        try:
            thong_bao = tam_ngung_va_tim(
                _driver,
                '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
                'div[2]/div/div/section/div/div')
            print(thong_bao.text)
            nut_next = tam_ngung_va_tim(
                _driver,
                '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
                'div[7]/div/div/div/div[2]/button/span/span')
            print('Đợi 90s thử lại')
            sleep(90)
            print('Thử lại')
            nut_next.click()
        except Exception:
            print('Mất thông báo')
            while True:
                LOGGER.info('Gửi thông báo qua telegram')
                tele_url = f'https://api.telegram.org/bot{BOT_TELE}/sendMessage'
                params = {
                    'chat_id': CHAT_ID,
                    'text': 'VISA_462_MỞ_CỔNG',
                    }
                requests.post(url=tele_url, data=params)

                LOGGER.info('Phat nhac')
                winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                LOGGER.info('xong')

    return _driver


if __name__ == '__main__':
    THOI_GIAN_HIEN_TAI = datetime.now()
    LOGGER = thiet_lap_logging(NAME)
    LOGGER.info('Chạy chương trình')

    if os.path.exists('tele.conf'):
        LOGGER.info('Load config')
        CONFIG = ConfigParser()
        CONFIG.read('tele.conf')
        BOT_TELE = CONFIG.get('config', 'BOT_TELE')
        CHAT_ID = CONFIG.get('config', 'CHAT_ID')
        LOGGER.info('Gửi thông báo qua telegram')
        tele_url = f'https://api.telegram.org/bot{BOT_TELE}/sendMessage'
        params = {
            'chat_id': CHAT_ID,
            'text': f'Chạy tool auto: {THOI_GIAN_HIEN_TAI}',
        }
        requests.post(url=tele_url, data=params)
    DRIVER = None

    try:
        LOGGER.info('*' * 50)
        LOGGER.info('Chạy thử chương trình')
        LOGGER.info('*' * 50)
        HEADLESS = False

        DRIVER = chay_trinh_duyet(headless=HEADLESS)
        DRIVER.maximize_window()
        SIZE = DRIVER.get_window_size()
        DRIVER.set_window_size(SIZE['width'] / 2, SIZE['height'])
        DRIVER.set_window_position(
            0,
            0,
            windowHandle='current',
        )
        LOGGER.info('Mở trang web')
        DRIVER = mo_website(DRIVER, URL)
        THOI_GIAN_XU_LY = datetime.now() - THOI_GIAN_HIEN_TAI
        LOGGER.info('Thời gian xử lý: %s', THOI_GIAN_XU_LY)
        input("Ấn Enter để thoát: ")
        
    except Exception:
        print('Không vào được trang 1')
        while True:
            LOGGER.info('Gửi thông báo qua telegram')
            tele_url = f'https://api.telegram.org/bot{BOT_TELE}/sendMessage'
            params = {
                'chat_id': CHAT_ID,
                'text': 'VISA_462_MỞ_CỔNG',
                    }
            requests.post(url=tele_url, data=params)

            LOGGER.info('Phat nhac')
            winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
            LOGGER.info('xong')
    finally:
        if DRIVER:
            DRIVER.close()
