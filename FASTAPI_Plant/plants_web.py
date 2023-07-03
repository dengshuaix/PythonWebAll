# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

from FASTAPI_Plant.resource.plant_resource import plant_router

app = FastAPI()
app.include_router(plant_router)

from FASTAPI_Plant.middleware import *

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9002)
