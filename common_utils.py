# coding: utf-8
import logging
import sentry_sdk

from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


EXTRA = dict(cookies_name=None)


class CustomLogFilter(logging.Filter):
    '''Lớp filter lấy tên cookies đang sử dụng. Nếu không có thì để None'''
    def filter(self, record):
        if not hasattr(record, 'cookies_name'):
            record.cookies_name = EXTRA.get('cookies_name')
        return True


def thiet_lap_logging(name, testing=None):
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
    if not testing:
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


def tam_ngung_va_tim_danh_sach(driver, _xpath):
    '''Hàm tạm ngưng đến khi xuất hiện đường dẫn xpath và chọn các phần tử có
    xpath đó
    '''
    tam_ngung_den_khi(driver, _xpath)
    return driver.find_elements(by='xpath', value=_xpath)
