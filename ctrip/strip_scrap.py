#!/usr/bin/env python3
# coding:utf-8

import config
from openpyxl import Workbook
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import asyncio

DAYS = config.DAYS
D_CITY = config.D_CITY
A_CITY = config.A_CITY

FULL_PRICE = config.FULL_PRICE

entry_url = 'http://flights.ctrip.com/booking/%s-%s-day-1.html' % (D_CITY, A_CITY)

wb = Workbook()
worksheet = wb.active


@asyncio.coroutine
def save_one_row(ws_name):
    while True:
        l = yield
        if l is not None:
            l.insert(0, datetime.datetime.now())
            worksheet.append(l)
            print('正在保存中。。。')
            wb.save(ws_name)


@asyncio.coroutine
def begin(save):
    coun = 2
    driver = webdriver.Firefox()
    driver.get(entry_url)
    driver.find_element_by_xpath('//*[@id="reSearchForm"]/div/div[3]/input').click()
    driver.implicitly_wait(10)
    flights = driver.find_element_by_xpath('//*[@id="J_flightlist2"]')

    # flights.get_attribute()
    children = flights.find_elements_by_xpath('div')
    print(children)
    for child in children:
        l = []
        # 航班号
        flight_id = child.get_attribute('id').strip()[7:]
        # 计划机型
        flight_type = child.find_element_by_xpath('table/tbody/tr/td[1]/div[2]/span').text.strip()
        # 起飞时刻
        flight_dtime = child.find_element_by_xpath('table/tbody/tr/td[2]/div[1]/strong').text.strip()
        # 起飞机场
        flight_dport = child.find_element_by_xpath('table/tbody/tr/td[2]/div[2]').text.strip()
        # 到达时刻
        flight_atime = child.find_element_by_xpath('table/tbody/tr/td[4]/div[1]/strong').text.strip()
        # 到达时刻
        flight_aport = child.find_element_by_xpath('table/tbody/tr/td[4]/div[2]').text.strip()
        # 币种
        money_type = child.find_element_by_xpath('table/tbody/tr/td[8]/span/dfn').text.strip()
        # 最低价格
        flight_lprice = child.find_element_by_xpath('table/tbody/tr/td[8]/span').text.strip()[1:]
        price = int(flight_lprice[1:])
        # 折扣
        discount = price / FULL_PRICE
        l.append(flight_id)
        l.append(flight_type)
        l.append(flight_dtime)
        l.append(flight_dport)
        l.append(flight_atime)
        l.append(flight_aport)
        l.append(money_type)
        l.append(flight_lprice)
        l.append(discount)
        save.send(l)
        yield
    while coun < DAYS + coun:
        coun = coun + 1
        # 下面一天
        driver.find_element_by_xpath('//*[@id="J_controlPannel"]/div[1]/div[2]/ul/li[%d]/a' % coun).click()
        flag = coun % 2
        if flag == 1:
            id_ = 'J_flightlist1'
        else:
            id_ = 'J_flightlist2'
        flights_ = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, id_)))
        # flights_ = driver.find_elemet_by_xpath('//*[@id="J_flightlist1"]')
        print(flights_.get_attribute('id'))
        # flights.get_attribute()
        children_ = flights_.find_elements_by_xpath('div')
        for child in children_:
            l = []
            # 航班号
            flight_id = child.get_attribute('id').strip()[7:]
            # 计划机型
            flight_type = child.find_element_by_xpath('table/tbody/tr/td[1]/div[2]/span').text.strip()
            # 起飞时刻
            flight_dtime = child.find_element_by_xpath('table/tbody/tr/td[2]/div[1]/strong').text.strip()
            # 起飞机场
            flight_dport = child.find_element_by_xpath('table/tbody/tr/td[2]/div[2]').text.strip()
            # 到达时刻
            flight_atime = child.find_element_by_xpath('table/tbody/tr/td[4]/div[1]/strong').text.strip()
            # 到达时刻
            flight_aport = child.find_element_by_xpath('table/tbody/tr/td[4]/div[2]').text.strip()
            # 币种
            money_type = child.find_element_by_xpath('table/tbody/tr/td[8]/span/dfn').text.strip()
            # 最低价格
            flight_lprice = child.find_element_by_xpath('table/tbody/tr/td[8]/span').text.strip()[1:]
            price = int(flight_lprice[1:])
            # 折扣
            discount = price / FULL_PRICE
            l.append(flight_id)
            l.append(flight_type)
            l.append(flight_dtime)
            l.append(flight_dport)
            l.append(flight_atime)
            l.append(flight_aport)
            l.append(money_type)
            l.append(flight_lprice)
            l.append(discount)
            save.send(l)
            yield


save = save_one_row('%s-%s.xls' % (D_CITY, A_CITY))
save.send(None)
loop = asyncio.get_event_loop()
loop.run_until_complete(begin(save))
loop.close()
