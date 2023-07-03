# -*- coding: utf-8 -*-
# sanic 中间件

# 请求到达处理程序之前执行
async def before_request(request):
    print('Before request')
    return

# 处理请求期间
async def during_request(request):
    print('During request')
    return

# 处理请求响应请求之后
async def after_request(request, response):
    print('After request')
    return response
