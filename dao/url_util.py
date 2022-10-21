# -*- coding:utf-8 -*-


from selenium import webdriver

header = {
    "ua_base": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 "
               "Safari/537.36 micromessenger/5.0.1.352 "
}


def open_chrome_get_html(html_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(html_url)
    return driver.page_source
