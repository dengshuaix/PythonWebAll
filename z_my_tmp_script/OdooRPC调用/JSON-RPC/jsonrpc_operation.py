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

    # 创建 数据
    create_data = [
        {'name': 'Book 1', 'date_release': '2019-01-26'},
        {'name': 'Book 3', 'date_release': '2019-02-12'},
        {'name': 'Book 5', 'date_release': '2019-05-08'},
        {'name': 'Book 7', 'date_release': '2019-05-14'}
    ]
    payload=get_json_payload('object','execute_kw',db_name,user_id,password,
                             'library.book','create',
                             [create_data])
    res=requests.post(json_endpoing,data=payload,headers=headers).json()
    print(res)
    books_ids=res['result']

    # 修改
    book_to_write=books_ids[0]
    write_data={'name':'Book123456789'}
    payload=get_json_payload('object','execute_kw',db_name,user_id,password,
                             'library.book','write',
                             [book_to_write,write_data])
    res=requests.post(json_endpoing,data=payload,headers=headers).json()
    print(res)

    # 已有图书记录中进行删除
    book_to_unlink=books_ids[2]
    payload=get_json_payload('object','execute_kw',db_name,user_id,password,
                             'library.book','unlink',
                             [book_to_unlink])
    res=requests.post(json_endpoing,data=payload,headers=headers).json()
    print(res)


# check_access_rights  检查权限