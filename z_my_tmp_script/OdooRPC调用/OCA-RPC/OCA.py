# _*_encoding:utf-8_*_
import odoorpc

server_url='http://127.0.0.1:8888' # 地址
db_name='12DB_ENTER'  # 数据库
username='1'  # 账号
password='1'   # 密码s
# 获得odoorpc对象
odoo=odoorpc.ODOO('localhost',port=8888)
# 登录验证
odoo.login(db_name,username,password)

# 当前用户
user=odoo.env.user
print(user)
print(user.company_id.name)
print(user.email)


# 获取模型
BookModel=odoo.env['library.book']
search_domain=['|',['name','ilike','python'],['name','ilike','信息']]
books_ids=BookModel.search(search_domain,limit=5)
for book in BookModel.browse(books_ids):
    print(book.name,book.date_release)

# 新增
book_id=BookModel.create({'name':'Test','state':'draft'})
book=BookModel.browse(book_id)
book.make_available()
book=BookModel.browse(book_id)
print(book.state)


# login方法  传递数据库名，用户名 和密码
# odoo.execute方法 执行原声rpc语法
'''
    books_info = odoo.execute('library.book', 'search_read',
      [['name', 'ilike', 'odoo']], ['name', 'date_release'])
    print(books_info)
'''