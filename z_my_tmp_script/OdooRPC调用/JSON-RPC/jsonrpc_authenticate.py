# _*_encoding:utf-8_*_
import json
import random
import requests
from xmlrpc import client
server_url='http://127.0.0.1:8888' # 地址
db_name='12DB_ENTER'  # 数据库
username='1'  # 账号
password='1'   # 密码s



json_endpoing=f"{server_url}/jsonrpc"  # jsonrpc 地址
headers={  # JSON-RPC接收JSON格式
    'Content-Type':'application/json',
}

def get_json_payload(service,method,*args):
    return json.dumps({
        'jsonrpc':'2.0',
        'method':'call',
        'params':{
            'service':service,
            'method':method,
            'args':args
        },
        'id':random.randint(0,10000)
    })
payload=get_json_payload('common','login',db_name,username,password)
print('payload',payload)  # 组装请求数据
response=requests.post(json_endpoing,data=payload,headers=headers)
print('response',response)
print(response.json())  # {'jsonrpc': '2.0', 'id': 428, 'result': 2}
user_id=response.json()['result']
print(user_id)


