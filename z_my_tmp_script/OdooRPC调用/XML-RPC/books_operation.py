# _*_encoding:utf-8_*_

from xmlrpc import client

server_url = 'http://127.0.0.1:8888'  # 地址
db_name = '12DB_ENTER'  # 数据库
username = '1'  # 账号
password = '1'  # 密码

common = client.ServerProxy(f'{server_url}/xmlrpc/2/common')
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    # create_date = [
    #     {'name': '西游记', 'release_date': string_to_datetime('2019-01-26').astimezone(tz=pytz.utc)},
    #     {'name': '水浒传', 'release_date': string_to_datetime('2019-03-26').astimezone(tz=pytz.utc)},
    #     {'name': '三国演义', 'release_date': string_to_datetime('2019-05-26').astimezone(tz=pytz.utc)},
    #     {'name': '红楼梦', 'release_date': string_to_datetime('2019-07-26').astimezone(tz=pytz.utc)},
    # ]
    import time

    create_date = [
        {'name': '西游记', 'date_release': time.strftime('%Y-%m-%d %H:%M:%S')},
        {'name': '水浒传', 'date_release': '2019-03-26 00:00:00'},
        {'name': '三国演义', 'date_release': '2019-05-26 00:00:00'},
        {'name': '红楼梦', 'date_release': '2019-07-26 00:00:00'}
    ]

    # 创建新的数据
    books_ids = models.execute_kw(db_name, user_id, password, 'library.book', 'create', [create_date])
    print(books_ids)

    # 修改数据
    book_to_write = books_ids[1]
    write_data = {'name': '水壶赚2'}
    written = models.execute_kw(db_name, user_id, password,
                                'library.book', 'write', [book_to_write, write_data])
    print(written)

    # 删除
    books_to_delete = books_ids[2]
    deleted = models.execute_kw(db_name, user_id, password, 'library.book', 'unlink', [books_to_delete])
    print(deleted)
