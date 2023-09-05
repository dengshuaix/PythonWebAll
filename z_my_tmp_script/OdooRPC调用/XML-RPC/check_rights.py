# _*_encoding:utf-8_*_
from xmlrpc import client

server_url = 'http://127.0.0.1:8888'  # 地址
db_name = '12DB_ENTER'  # 数据库
username = '1'  # 账号
password = '1'  # 密码

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

# 验证' ' operation ' '给出的操作是否允许, 根据当前用户的访问权限
if user_id:
  has_access = models.execute_kw(db_name, user_id, password,
    'library.book', 'check_access_rights',
    ['read'], {'raise_exception': False})
  print('Has create access on book:', has_access )
else:
  print('Wrong credentials')

# 输出: Has create access on book: True