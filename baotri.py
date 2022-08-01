#!/usr/local/bin/python
# coding: utf-8
'''Tự động đăng nhập facebook
'''
import os
from platform import system
import sys

from time import sleep
from datetime import datetime

from configparser import ConfigParser
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

if system() == 'Windows':
    import winsound

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as firefox_options

from common_utils import (
    thiet_lap_logging, tam_ngung_va_tim, tam_ngung_den_khi,
    tam_ngung_va_tim_danh_sach,
)


TESTING = None
# URL = 'https://gleam.io/L8Tok/lixinft-giveaway'
NAME = 'tool_auto'
CONFIG_FILE = 'config.conf'
TELE_CONF = 'tele_config_2'
ALARM = False
TASK_ID = 1
SLEEP_TIME = 90


def chay_trinh_duyet(browser='chrome', headless=True):
    '''Mở trình duyệt và trả về driver
    '''
    headless = bool(headless)
    LOGGER.info('Chạy trình duyệt %s, headless=%s', browser, headless)
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option(
            'useAutomationExtension', False)
        options.add_argument(
            "--disable-blink-features=AutomationControlled")
        service = Service(ChromeDriverManager().install())
        _driver = webdriver.Chrome(
            options=options,
            service=service,
        )

    if browser == 'firefox':
        options = firefox_options()
        options.headless = headless
        service = Service(GeckoDriverManager().install())
        _driver = webdriver.Firefox(
            options=options,
            service=service,
        )

    # Đặt cửa sổ bằng nửa màn hình để debug
    if HEADLESS:
        _driver.maximize_window()
        size = _driver.get_window_size()
        _driver.set_window_size(size['width'] / 2, size['height'])
        _driver.set_window_position(
            0,
            0,
            windowHandle='current',
        )

    # Hàm đặt thời gian tải trang, dùng khi tải trang quá lâu
    # _driver.set_page_load_timeout(5)
    return _driver


def qua_trang_5(_driver, url):
    '''Kiểm tra đến được trang 5
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

    # Ấn nút edit
    nut_edit = tam_ngung_va_tim(
        _driver,
        '/html/body/form/section/div/div/div[3]/div/div[2]/div/div/div[2]/'
        'div/div[2]/div/div/div[2]/div/div/div[1]/div/div/button')
    nut_edit.click()

    # Ấn nút next
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

    # Kiểm tra trang 5
    while True:
        try:
            thong_bao = tam_ngung_va_tim(
                _driver,
                '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
                'div[2]/div/div/section/div/div')
            LOGGER.info(thong_bao.text)
            nut_next = tam_ngung_va_tim(
                _driver,
                '/html/body/form/div[1]/div/div/div[1]/section/div/div/div/'
                'div[7]/div/div/div/div[2]/button/span/span')
            LOGGER.info('Đợi %ds thử lại', SLEEP_TIME)
            sleep(SLEEP_TIME)
            LOGGER.info('Thử lại')
            nut_next.click()
        except Exception:
            LOGGER.info('Mất thông báo')
            while True:
                LOGGER.info('Gửi thông báo qua telegram')
                PARAMS = {
                    'chat_id': CHAT_ID,
                    'text': 'VISA_462_MỞ_CỔNG',
                    }
                requests.post(url=TELE_URL, data=PARAMS)

                LOGGER.info('Phát nhạc')
                if system() == 'Windows':
                    winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                LOGGER.info('Xong')

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
                    PARAMS = {
                        'chat_id': CHAT_ID,
                        'text': 'Hết bảo trì',
                        }
                    requests.post(url=TELE_URL, data=PARAMS)
                    LOGGER.info('Phát nhạc')
                    if system() == 'Windows':
                        winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                    LOGGER.info('xong')
                except Exception as error:
                    LOGGER.exception(error)
                    break
        else:
            LOGGER.info('Đang bảo trì')
            LOGGER.info('Thử lại sau %ds', SLEEP_TIME,)
            sleep(SLEEP_TIME)
            LOGGER.info('Reload')
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

    # Kiểm tra location Việt Nam
    while True:
        stt_apply = 44
        for stt, khu_vuc in enumerate(ds_khu_vuc):
            if stt == stt_apply:
                ten_khu_vuc = khu_vuc.find_element(
                    by='xpath',
                    value='.//span[@id="'
                    f'ContentPlaceHolder1_countryRepeater_countryName_{stt}"]',
                )
                tinh_trang = khu_vuc.find_element(
                    by='xpath',
                    value='.//span[@id="ContentPlaceHolder1_countryRepeater'
                    f'_countryStatus_{stt}"]',
                )
                LOGGER.info(
                    '%s: %s (%s)',
                    stt,
                    ten_khu_vuc.text,
                    tinh_trang.text,
                )
                if tinh_trang.text.lower() != 'closed':
                    LOGGER.info('Việt nam mở')
                    while True:
                        LOGGER.info('Gửi thông báo qua telegram')
                        PARAMS = {
                            'chat_id': CHAT_ID,
                            'text': 'VIET_NAM_MỞ_CỔNG',
                            }
                        requests.post(url=TELE_URL, data=PARAMS)

                    LOGGER.info('Phát nhạc')
                    if system() == 'Windows':
                        winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                    LOGGER.info('Xong')
            else:
                LOGGER.info('Đợi %ds thử lại', SLEEP_TIME)
                sleep(SLEEP_TIME)
                LOGGER.info('Thử lại')
                _driver.refresh()

    input('Nhập enter để thoát: ')
    return _driver


def tu_dong_dien(_driver, url):
    '''Tự động điền trang 5 - 16
    '''
    # Mở trang
    _driver.get(url)

    # Nhập thông tin tài khoản
    LOGGER.info('Load user config')
    user = CONFIG.get('user_test', 'USER')
    pass_ = CONFIG.get('user_test', 'PASS')
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

    # Ấn nút edit
    nut_edit = tam_ngung_va_tim(
        _driver,
        '/html/body/form/section/div/div/div[3]/div/div[2]/div/div/div[2]/'
        'div/div[2]/div/div/div[2]/div/div/div[1]/div/div/button')
    nut_edit.click()

    # Ấn nút next
    nut_next = tam_ngung_va_tim(
        _driver,
        'id="_2a0b4d"',
    )
    nut_next.click()

    # Đợi hiện nút next thì tìm số trang
    nut_next = tam_ngung_va_tim(
        _driver,
        'id="_2a0bg4d"',
    )
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

    # Tự động điền trang 5

    input()
    return _driver


if __name__ == '__main__':
    THOI_GIAN_HIEN_TAI = datetime.now()
    LOGGER = thiet_lap_logging(NAME)
    LOGGER.info('*' * 50)
    LOGGER.info('Chạy chương trình')

    if len(sys.argv) > 1:
        CONFIG_FILE = sys.argv[1]

    if os.path.exists(CONFIG_FILE):
        LOGGER.info('Load config từ file: %s', CONFIG_FILE)
        CONFIG = ConfigParser()
        CONFIG.read(CONFIG_FILE)
        BOT_TELE = CONFIG.get(TELE_CONF, 'BOT_TELE')
        CHAT_ID = CONFIG.get(TELE_CONF, 'CHAT_ID')
        TASK_ID = int(CONFIG.get('tool_config', 'TASK_ID'))
        TELE_URL = f'https://api.telegram.org/bot{BOT_TELE}/sendMessage'
    DRIVER = None

    try:
        LOGGER.info('Chạy chương trình')
        if TASK_ID == 1:
            MESSAGE = 'Chạy kiểm tra qua được trang 5'
        if TASK_ID == 2:
            MESSAGE = 'Chạy kiểm tra trang bảo trì'
        if TASK_ID == 3:
            MESSAGE = 'Chạy auto apply visa newzealand'
        if TASK_ID == 4:
            MESSAGE = 'Chạy tự động điền từ trang 5'
        PARAMS = {
            'chat_id': CHAT_ID,
            'text': MESSAGE,
        }
        requests.post(url=TELE_URL, data=PARAMS)
        HEADLESS = CONFIG.get('tool_config', 'HEADLESS')

        DRIVER = chay_trinh_duyet(
            browser=CONFIG.get('tool_config', 'BROWSER'),
            headless=int(HEADLESS),
        )
        LOGGER.info('Mở trang web')
        if TASK_ID == 1:
            LOGGER.info('Chạy kiểm tra qua được trang 5')
            URL = 'https://online.immi.gov.au'
            DRIVER = qua_trang_5(DRIVER, URL)
        if TASK_ID == 2:
            LOGGER.info('Chạy kiểm tra trang bảo trì')
            URL = 'https://online.immi.gov.au'
            DRIVER = bao_tri(DRIVER, URL)
        if TASK_ID == 3:
            LOGGER.info('Chạy auto apply visa newzealand')
            URL = 'https://onlineservices.immigration.govt.nz/'
            DRIVER = visa2(DRIVER, URL)
        if TASK_ID == 4:
            LOGGER.info('Chạy tự động điền từ trang 5')
            URL = 'https://online.immi.gov.au'
            DRIVER = tu_dong_dien(DRIVER, URL)

        THOI_GIAN_XU_LY = datetime.now() - THOI_GIAN_HIEN_TAI
        LOGGER.info('Thời gian xử lý: %s', THOI_GIAN_XU_LY)

    except Exception as error:
        LOGGER.exception(error)
        if ALARM:
            while True:
                LOGGER.info('Gửi thông báo qua telegram')
                PARAMS = {
                    'chat_id': CHAT_ID,
                    'text': 'Không chạy được tool',
                    }
                requests.post(url=TELE_URL, data=PARAMS)

                LOGGER.info('Phát nhạc')
                if system() == 'Windows':
                    winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
                LOGGER.info('Xong')
    finally:
        if DRIVER:
            DRIVER.close()
