# -*- coding: utf-8 -*-
import time

from FASTAPI_Plant.plants_web import app  # 这么写，暂时无问题，非正常例解代码


# 中间件
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response
