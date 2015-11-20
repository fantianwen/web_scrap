#!/usr/bin/env python3
# coding:utf-8

import re

pattern = re.compile('^flight')

flag = pattern.search('flight——dfdsfsdf')


if flag is None:
    print('没有找到')
else:
    print('匹配成功')
