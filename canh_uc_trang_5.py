#!/usr/local/bin/python
# coding: utf-8
'''Tự động đăng nhập facebook
'''
import os
import sys

from time import sleep
from datetime import datetime

from configparser import ConfigParser

from common_utils import (
    thiet_lap_logging, tam_ngung_va_tim,
    chay_trinh_duyet, gui_thong_bao_tele,
    phat_nhac_canh_bao,
)


def qua_trang_5(_driver, url):
    '''Kiểm tra đến được trang 5
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
        if '<h1 class="panelHeading">Login</h1>' in _driver.page_source:
            _driver = qua_trang_5(_driver, url)
            return _driver

        if 'the system is currently unavailable' in _driver.page_source.lower():
            LOGGER.info(
                'Trang bị lỗi hoặc mất mạng, thử lại sau %ds',
                SLEEP_TIME,
            )
            sleep(SLEEP_TIME)
            LOGGER.info('Thử lại')
            _driver.refresh()

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
                text = 'VISA_462_MỞ_CỔNG'
                gui_thong_bao_tele(BOT_TELE, CHAT_ID, text)
                phat_nhac_canh_bao(FILE_MP3)

    return _driver


if __name__ == '__main__':
    CONFIG_FILE = 'config.conf'
    TELE_CONF = 'tele_config_2'
    ALARM = False
    SLEEP_TIME = 30
    FILE_MP3 = 'nhac.wav'
    THOI_GIAN_HIEN_TAI = datetime.now()
    LOGGER = thiet_lap_logging(testing=True)
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
    else:
        LOGGER.info('Đường dẫn file không tồn tại: %s', CONFIG_FILE)
        sys.exit()
    DRIVER = None

    try:
        LOGGER.info('Chạy chương trình')
        TEXT = 'Chạy auto canh visa úc mở trang 5'
        gui_thong_bao_tele(BOT_TELE, CHAT_ID, TEXT)
        HEADLESS = CONFIG.get('tool_config', 'HEADLESS')

        DRIVER = chay_trinh_duyet(
            browser=CONFIG.get('tool_config', 'BROWSER'),
            headless=int(HEADLESS),
        )
        LOGGER.info('Mở trang web')
        LOGGER.info(TEXT)
        URL = 'https://online.immi.gov.au'
        DRIVER = qua_trang_5(DRIVER, URL)

        THOI_GIAN_XU_LY = datetime.now() - THOI_GIAN_HIEN_TAI
        LOGGER.info('Thời gian xử lý: %s', THOI_GIAN_XU_LY)

    except Exception as error:
        LOGGER.exception(error)
        if ALARM:
            while True:
                TEXT = 'Không chạy được tool'
                gui_thong_bao_tele(BOT_TELE, CHAT_ID, TEXT)
                phat_nhac_canh_bao(FILE_MP3)
    finally:
        if DRIVER:
            DRIVER.close()
