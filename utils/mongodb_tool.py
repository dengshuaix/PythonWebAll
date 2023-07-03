# -*- coding: utf-8 -*-

from pymongo import MongoClient

client = MongoClient()  # 默认连接本地mongodb数据库
db = client['plants']
