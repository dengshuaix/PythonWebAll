# -*- coding: utf-8 -*-
# 1. aiohttp 模块 : requests 和 Python的异步网络请求库 , 基于 asyncio的异步爬虫
import aiohttp
import asyncio
import async_timeout

async def fetch(session, url):
    """
        # 异步爬取 URL
    :param session: 异步 请求对象
    :param url:
    :return: 返回响应结果
    """
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def main():
    """
        # 异步主函数
    :return:
    """
    #  制作异步请求对象
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://zhuanlan.zhihu.com/p/224895183')
        print(html)


# loop : 事件循环对象
loop = asyncio.get_event_loop()
loop.run_until_complete(main())