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


def bao_tri(_driver, url):
    '''Mở website và xem khi nào hết bảo tri
    '''
    try:
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
        nut_continue = tam_ngung_va_tim(
            _driver,
            '/html/body/form/div/div/button',
        )
        nut_continue.click()

        # Kiểm tra trang bảo trì
        while True:
            input()
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
                    text = 'Hết bảo trì'
                    gui_thong_bao_tele(BOT_TELE, CHAT_ID, text)
                    phat_nhac_canh_bao(FILE_MP3)
            else:
                LOGGER.info('Đang bảo trì')
                LOGGER.info('Thử lại sau %ds', SLEEP_TIME,)
                sleep(SLEEP_TIME)
                LOGGER.info('Reload')
                _driver.refresh()
                continue
    except Exception as error:
        LOGGER.exception(error)
    finally:
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
        TEXT = 'Chạy auto canh visa úc'
        gui_thong_bao_tele(BOT_TELE, CHAT_ID, TEXT)
        HEADLESS = CONFIG.get('tool_config', 'HEADLESS')

        DRIVER = chay_trinh_duyet(
            browser=CONFIG.get('tool_config', 'BROWSER'),
            headless=int(HEADLESS),
        )
        LOGGER.info('Mở trang web')
        LOGGER.info(TEXT)
        URL = 'https://online.immi.gov.au'
        DRIVER = bao_tri(DRIVER, URL)

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
