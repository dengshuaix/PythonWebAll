# _*_encoding:utf-8_*_

from xmlrpc import client

server_url = 'http://127.0.0.1:8888'  # 地址
db_name = '12DB_ENTER'  # 数据库
username = '1'  # 账号
password = '1'  # 密码

common = client.ServerProxy(f'{server_url}/xmlrpc/2/common')
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

print(user_id, models)

if user_id:
    # execute_kw()可以访问任意模型的对公方法
    search_domain = ['|', ['name', 'ilike', 'odoo'], ['name', 'ilike', 'python']]
    # 执行 查找 search
    books_ids = models.execute_kw(db_name, user_id, password,
                                  'library.book', 'search',
                                  [search_domain],
                                  {'limit': 5})
    print('Books ids found:', books_ids)

    # 执行搜索 read
    books_data = models.execute_kw(db_name, user_id, password,
                                   'library.book',
                                   'read',
                                   [books_ids, ['name', 'date_release','create_uid']], )
    print(books_data)
else:
    print('Wrong')
