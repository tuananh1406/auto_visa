#!/usr/local/bin/python
# coding: utf-8
'''Tự động đăng nhập facebook
'''
import os

from time import sleep
from datetime import datetime

from configparser import ConfigParser
from webdriver_manager.chrome import ChromeDriverManager

# import winsound

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from common_utils import (
    thiet_lap_logging, tam_ngung_va_tim, tam_ngung_den_khi,
    tam_ngung_va_tim_danh_sach,
)


TESTING = None
# URL = 'https://gleam.io/L8Tok/lixinft-giveaway'
# URL = 'https://online.immi.gov.au'
URL = 'https://onlineservices.immigration.govt.nz/'
NAME = 'tool_auto'
CONFIG_FILE = 'config.conf'
TELE_CONF = 'tele_config_2'
ALARM = False


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


def bao_tri(_driver, url):
    '''Mở website và xem khi nào hết bảo tri
    '''
    # Mở trang
    _driver.get(url)

    # Nhập thông tin tài khoản
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
    # Đăng nhập
    login = _driver.find_element(
        by='xpath',
        value='/html/body/form/div/div[2]/button[2]',
    )
    login.click()

    # Ấn nút continue
    nut_continue = tam_ngung_va_tim(_driver, '/html/body/form/div/div/button')
    nut_continue.click()

    # Kiểm tra trang bảo trì
    while True:
        trang_thong_bao = tam_ngung_va_tim(
            _driver,
            '/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr/td/h2',
        )
        LOGGER.info(trang_thong_bao.text)
        thong_bao_bao_tri = 'ImmiAccount is currently unavailable for' \
            ' planned system maintenance'
        if thong_bao_bao_tri not in trang_thong_bao.text:
            LOGGER.info('Mất thông báo')
            while True:
                LOGGER.info('Gửi thông báo qua telegram')
                try:
                    requests.post(url=TELE_URL, data=PARAMS)
                    LOGGER.info('Phát nhạc')
                    # winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                    LOGGER.info('xong')
                except Exception as error:
                    LOGGER.exception(error)
                    break
        else:
            LOGGER.info('Đang bảo trì')
            LOGGER.info('15s reload')
            sleep(15)
            LOGGER.info('reload')
            _driver.refresh()
            continue

    return _driver


def visa2(_driver, url):
    '''Trang đăng ký visa new zealand
    '''
    # Mở trang
    _driver.get(url)

    # Nhập thông tin tài khoản
    LOGGER.info('Load user config')
    user = CONFIG.get('user_3_config', 'USER')
    pass_ = CONFIG.get('user_3_config', 'PASS')
    username = tam_ngung_va_tim(
        _driver,
        '//input[@name="username"]',
    )
    username.send_keys(user)
    password = _driver.find_element(
        by='xpath',
        value='//input[@name="password"]',
    )
    password.send_keys(pass_)
    # Đăng nhập
    login = _driver.find_element(
        by='xpath',
        value='//input[@type="submit"]',
    )
    login.click()

    # Đợi đến khi hiển trị trang apply online
    tam_ngung_den_khi(_driver, '//div[@class="block-form"]')

    # Lấy các danh mục được apply
    cac_danh_muc = _driver.find_elements(
        by='xpath',
        value='//div[@class="block-form-content"]',
    )
    LOGGER.info('Chọn danh mục cần apply')
    for stt, danh_muc in enumerate(cac_danh_muc):
        tieu_de = danh_muc.find_element(
            by='xpath',
            value='h3',
        )
        LOGGER.info('%d - %s', stt, tieu_de.text)

    # Tự chọn danh mục cần apply
    # while True:
    #     stt_apply = input('Nhập số danh mục cần apply: ')
    #     if not str(stt_apply).isdigit():
    #         LOGGER.info('STT phải là 1 số nguyên')
    #         continue

    #     stt_apply = int(stt_apply)
    #     if stt_apply < 0 or stt_apply + 1 > len(cac_danh_muc):
    #         LOGGER.info(
    #             'STT phải trong khoảng 0 đến %d',
    #             len(cac_danh_muc) - 1,
    #         )
    #         continue

    #     break

    danh_muc = cac_danh_muc[1]
    tieu_de = danh_muc.find_element(
        by='xpath',
        value='h3',
    )
    duong_dan = danh_muc.find_element(
        by='xpath',
        value='a',
    )
    LOGGER.info('Apply vào: %s', tieu_de.text)
    duong_dan.click()

    # Lấy thông tin khu vực được phép apply
    ds_khu_vuc = tam_ngung_va_tim_danh_sach(
        _driver,
        '//div[@class="category-item"]',
    )
    LOGGER.info('Tìm được %d khu vực', len(ds_khu_vuc))

    LOGGER.info('Bảng danh sách tình trạng các khu vực:')
    for stt, khu_vuc in enumerate(ds_khu_vuc):
        ten_khu_vuc = khu_vuc.find_element(
            by='xpath',
            value='.//span[@id="'
            f'ContentPlaceHolder1_countryRepeater_countryName_{stt}"]',
        )
        tinh_trang = khu_vuc.find_element(
            by='xpath',
            value='.//span[@id="'
            f'ContentPlaceHolder1_countryRepeater_countryStatus_{stt}"]',
        )
        LOGGER.info('%s: %s (%s)', stt, ten_khu_vuc.text, tinh_trang.text)

    input('Nhập enter để thoát: ')
    return _driver


if __name__ == '__main__':
    THOI_GIAN_HIEN_TAI = datetime.now()
    LOGGER = thiet_lap_logging(NAME)
    LOGGER.info('*' * 50)
    LOGGER.info('Chạy chương trình')

    if os.path.exists(CONFIG_FILE):
        LOGGER.info('Load config')
        CONFIG = ConfigParser()
        CONFIG.read(CONFIG_FILE)
        BOT_TELE = CONFIG.get(TELE_CONF, 'BOT_TELE')
        CHAT_ID = CONFIG.get(TELE_CONF, 'CHAT_ID')
        LOGGER.info('Gửi thông báo qua telegram')
        TELE_URL = f'https://api.telegram.org/bot{BOT_TELE}/sendMessage'
        PARAMS = {
            'chat_id': CHAT_ID,
            'text': f'Chạy tool auto: {THOI_GIAN_HIEN_TAI}',
        }
        requests.post(url=TELE_URL, data=PARAMS)
    DRIVER = None

    try:
        LOGGER.info('Chạy thử chương trình')
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
        # DRIVER = bao_tri(DRIVER, URL)
        DRIVER = visa2(DRIVER, URL)
        THOI_GIAN_XU_LY = datetime.now() - THOI_GIAN_HIEN_TAI
        LOGGER.info('Thời gian xử lý: %s', THOI_GIAN_XU_LY)

    except Exception as error:
        LOGGER.exception(error)
        if ALARM:
            while True:
                LOGGER.info('Gửi thông báo qua telegram')
                requests.post(url=TELE_URL, data=PARAMS)

                LOGGER.info('Phat nhac')
                # winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                LOGGER.info('xong')
    finally:
        if DRIVER:
            DRIVER.close()
