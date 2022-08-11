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
    thiet_lap_logging, tam_ngung_va_tim, tam_ngung_den_khi,
    tam_ngung_va_tim_danh_sach, chay_trinh_duyet, gui_thong_bao_tele,
    phat_nhac_canh_bao,
)


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

    # Kiểm tra location Việt Nam
    while True:

        # Lấy thông tin khu vực được phép apply
        ds_khu_vuc = tam_ngung_va_tim_danh_sach(
            _driver,
            '//div[@class="category-item"]',
        )
        LOGGER.info('Tìm được %d khu vực', len(ds_khu_vuc))

        LOGGER.info('Bảng danh sách tình trạng các khu vực:')
        # for stt, khu_vuc in enumerate(ds_khu_vuc):
        #     ten_khu_vuc = khu_vuc.find_element(
        #         by='xpath',
        #         value='.//span[@id="'
        #         f'ContentPlaceHolder1_countryRepeater_countryName_{stt}"]',
        #     )
        #     tinh_trang = khu_vuc.find_element(
        #         by='xpath',
        #         value='.//span[@id="'
        #         f'ContentPlaceHolder1_countryRepeater_countryStatus_{stt}"]',
        #     )
        #     LOGGER.info('%s: %s (%s)', stt,
        #     ten_khu_vuc.text, tinh_trang.text)

        stt = 44
        khu_vuc = ds_khu_vuc[stt]
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
                text = 'VIET_NAM_MỞ_CỔNG'
                gui_thong_bao_tele(BOT_TELE, CHAT_ID, text)
                phat_nhac_canh_bao(FILE_MP3)
        else:
            LOGGER.info('Đợi %ds thử lại', SLEEP_TIME)
            sleep(SLEEP_TIME)
            LOGGER.info('Thử lại')
            _driver.refresh()
            continue

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
        TEXT = 'Chạy auto apply visa newzealand'
        gui_thong_bao_tele(BOT_TELE, CHAT_ID, TEXT)
        HEADLESS = CONFIG.get('tool_config', 'HEADLESS')

        DRIVER = chay_trinh_duyet(
            browser=CONFIG.get('tool_config', 'BROWSER'),
            headless=int(HEADLESS),
        )
        LOGGER.info('Mở trang web')
        LOGGER.info('Chạy auto apply visa newzealand')
        URL = 'https://onlineservices.immigration.govt.nz/'
        DRIVER = visa2(DRIVER, URL)

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
