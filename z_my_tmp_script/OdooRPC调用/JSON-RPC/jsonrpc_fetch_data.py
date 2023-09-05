# _*_encoding:utf-8_*_

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
        'id':random.randint(0,10000000)
    })
payload=get_json_payload('common','login',db_name,username,password) # rpc 调用对象

response=requests.post(json_endpoing,data=payload,headers=headers)
user_id=response.json()['result']

if user_id:
    search_domain=['|',['name','ilike','python'], ['name', 'ilike', 'sql']]
    payload=get_json_payload('object','execute_kw',db_name,user_id,password,'library.book',
                             'search',[search_domain],{'limit':5})
    res=requests.post(url=json_endpoing,data=payload,headers=headers).json()
    print(res)
    payload=get_json_payload('object','execute_kw',db_name,user_id,password,
                             'library.book','read',
                             [res['result'],['name','date_release']])
    res=requests.post(json_endpoing,data=payload,headers=headers).json()
    print(res)

    payload=get_json_payload('object','execute_kw',db_name,user_id,password,
                             'library.book','search_read',
                             [search_domain,['name','date_release']],
                             {'limit':5})
    res=requests.post(json_endpoing,data=payload,headers=headers).json()
    print(res)


