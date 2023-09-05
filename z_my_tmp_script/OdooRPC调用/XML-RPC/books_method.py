# _*_encoding:utf-8_*_
# 通过XML-RPC调用方法

from xmlrpc import client

server_url = 'http://127.0.0.1:8888'  # 地址
db_name = '12DB_ENTER'  # 数据库
username = '1'  # 账号
password = '1'  # 密码

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)
print(user_id,models)
if user_id:
    book_id = models.execute_kw(db_name, user_id, password,
                                'library.book', 'create',
                                [{'name': 'New Book', 'date_release': '2019-01-26', 'state': 'draft'}])
    print(book_id)

    # 调用方法
    models.execute_kw(db_name,user_id,password,'library.book','make_available',[[book_id]])
    models.execute_kw(db_name, user_id, password,
                      'library.book', 'make_available',
                      [[52]])

    # 检查状态

    books_data = models.execute_kw(db_name, user_id, password,
                                   'library.book',
                                   'read',
                                   [[52], ['name', 'date_release','create_uid']], )
    print('Book state after method call:', books_data[0]['state'])
