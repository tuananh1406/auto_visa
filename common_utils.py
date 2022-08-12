# coding: utf-8
import logging
import sentry_sdk
import requests
from platform import system

if system() == 'Windows':
    import winsound

from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.firefox.options import Options as firefox_options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def thiet_lap_logging(testing=None):
    '''Hàm thiết lập trình ghi log và gửi lỗi lên sentry'''
    sentry_sdk.init(
        'https://2e084979867c4e8c83f0b3b8062afc5b@o1086935.'
        'ingest.sentry.io/6111285',
        traces_sample_rate=1.0,
    )

    log_format = ' - '.join([
        '%(asctime)s',
        '%(name)s',
        '%(levelname)s',
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

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.addHandler(syslog)
    if not testing:
        logger.addHandler(file_handles)

    return logger


def tam_ngung_den_khi(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath
    '''
    try:
        _tam_ngung = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                _xpath,
            )),
        )
        driver.execute_script("window.stop();")
        return _tam_ngung
    except Exception as error:
        logging.exception(error)
        return driver


def tam_ngung_va_tim(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath và chọn xpath đó
    '''
    try:
        tam_ngung_den_khi(driver, _xpath)
        return driver.find_element(by='xpath', value=_xpath)
    except Exception as error:
        logging.exception(error)
        return driver


def tam_ngung_va_tim_danh_sach(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath và chọn các phần tử có
    xpath đó
    '''
    tam_ngung_den_khi(driver, _xpath)
    return driver.find_elements(by='xpath', value=_xpath)


def chay_trinh_duyet(browser='chrome', headless=True):
    '''Mở trình duyệt và trả về driver
    '''
    headless = bool(headless)
    logging.info('Chạy trình duyệt %s, headless=%s', browser, headless)

    if browser == 'chrome':
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"
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
            desired_capabilities=caps,
        )

    if browser == 'firefox':
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "none"
        options = firefox_options()
        options.headless = headless
        service = Service(GeckoDriverManager().install())
        _driver = webdriver.Firefox(
            options=options,
            service=service,
        )

    # Đặt cửa sổ bằng nửa màn hình để debug
    if not headless:
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


def gui_thong_bao_tele(bot_token=None, chat_id=None, text=None):
    '''Gửi thông báo qua telegram'''
    if any([bot_token, chat_id]) is None:
        logging.info('bot token hoặc chat id không có thông tin')
        return None
    tele_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text,
    }
    logging.info('Gửi thông báo telegram')
    requests.post(url=tele_url, data=params)
    return True


def phat_nhac_canh_bao(file_mp3=None):
    '''Hàm phát nhạc cảnh báo'''
    if file_mp3 and system() == 'Windows':
        logging.info('Phát nhạc')
        winsound.PlaySound('nhac.wav', winsound.SND_FILENAME)
        return True
    return None
