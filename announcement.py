# -*- coding: utf-8 -*-

import sys
import random
import requests
import urllib2
import urllib
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from datetime import *
import time
import chardet
import os


#指定系统默认编码
reload(sys)
sys.setdefaultencoding('utf8')

RECORDS_FILE = 'records.txt'

def download(url, dirname, filename, records):
    if(url.endswith(".pdf")):
        print "downloading " + url
        if not os.path.isdir(dirname):
            print("make dir " + dirname);
            os.mkdir(dirname)
        urllib.urlretrieve(url, os.path.join(dirname,filename + os.path.basename(url)));
        records.append(url)
        path = os.path.join(dirname, RECORDS_FILE)
        writeConfig(path, records)

def readConfig(filename):
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    return lines

def writeConfig(path, records):
    # 带加号为可读写
    print 'Update records file...\n'
    hl = open(path, 'w')
    for record in records:
        hl.write(record + "\n")
    hl.close()

def process(url, key_words):
    print 'Fetching data from ' + url

    # 使用webdriver.PhantomJS
    # D:\phantomjs-2.1.1-windows\bin
    browser=webdriver.PhantomJS(executable_path='D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    browser.get(url)
    time.sleep(3)
    #设置开始日期
    estart_date = browser.find_element_by_xpath('//input[@id="start_date"]')
    estart_date.click()
    edate_select = browser.find_element_by_xpath('//div[@class="datetimepicker-days"]/table/tfoot/tr/th[@class="today"][1]')
    edate_select.click()

##    #本地保存pdf文件路径
##    date = estart_date.get_attribute("value")
##    path = os.path.join(date, RECORDS_FILE)
##    if os.path.isfile(path):
##        records = readConfig(path)
##    else:
##        records = []
    #设置结束日期
    eend_date = browser.find_element_by_xpath('//input[@id="end_date"]')
    eend_date.click()
    edate_select2 = browser.find_element_by_xpath('//div[@class="datetimepicker datetimepicker-dropdown-bottom-right dropdown-menu"][2]\
                                                  /div[@class="datetimepicker-days"]/table/tbody/tr/td[@class="day new"]')
    edate_select2.click()
    #输入关键字
    for key in key_words:
        ekey_word = browser.find_element_by_xpath('//input[@class="form-control"]')
        ekey_word.clear()
        ekey_word.send_keys(key.decode("utf-8"))
        #提交搜索
        esubmit = browser.find_element_by_xpath('//button[@id="btnQuery"]')
        esubmit.click()
        time.sleep(3)
##        browser.get_screenshot_as_file('show.png')
        html = browser.execute_script("return document.documentElement.outerHTML")

        soup = BeautifulSoup(html, "html.parser")
        hlst = soup.findAll('dd', class_='just_this_only')

        print("using keyword " + key.decode("utf-8")  + " get " + str(len(hlst)) + " articles")
        for h in hlst:
            date = h.find('span').text.strip()
            path = os.path.join(date, RECORDS_FILE)
            if os.path.isfile(path):
                records = readConfig(path)
            else:
                records = []
            region = h.find('em', class_='pdf-first').a
            item_url = region.get('href')
            if item_url in records:
                continue
            item_name = region.text.strip().replace(":","")
            print(item_name.decode("utf-8"))
            download(item_url, date, item_name.decode("utf-8"), records)
    print 'done'



if __name__ == '__main__':
    print("here")
    url_pre = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/'
    print(url_pre)
    triggerlist = readConfig("triggers.txt")
    process(url_pre, triggerlist)

