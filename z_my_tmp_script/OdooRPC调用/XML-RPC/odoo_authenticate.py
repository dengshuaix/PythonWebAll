# _*_encoding:utf-8_*_
from xmlrpc import client
server_url='http://127.0.0.1:8888' # 地址
db_name='12DB_ENTER'  # 数据库
username='1'  # 账号
password='1'   # 密码

common=client.ServerProxy(f'{server_url}/xmlrpc/2/common')
# authenticate 认证方法 。四个参数：数据，账号，密码，user agent环境，环境不能为空。至少传一个空字典
user_id=common.authenticate(db_name,username,password,{}) # 获取超级管理员id
version_info=common.version() # 获取版本

if user_id:
    print(user_id)
    print(version_info)
