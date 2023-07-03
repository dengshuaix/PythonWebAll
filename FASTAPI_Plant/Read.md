# FastAPI 框架

### 结构类似flask

- project
    - model
        - plants.py
    - resource
        - plant_resource.py
    - middleware.py
    - run.py

### 使用 uvicorn 提供wsgi服务,外层仍可以使用uwsgi作为部署
```python
# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9002)
```

### 代码展示

- plants.py

```python

# -*- coding: utf-8 -*-
from pydantic import BaseModel


# 定义plant模型
class Plant(BaseModel):
    name: str
    color: str

```

- plant_resource.py

```python
# -*- coding: utf-8 -*-
from bson import ObjectId
from fastapi import HTTPException, APIRouter
from FASTAPI_Plant.model.plants import Plant
from utils.mongodb_tool import db

plant_router = APIRouter()


# 查全部
@plant_router.get("/plants")
async def get_all_plants():
    plants = []
    for each_plant in db.plants.find():
        each_plant['_id'] = str(each_plant['_id'])
        plants.append(each_plant)

    return plants


# 查一条
@plant_router.get("/plant/{plant_id}")
async def get_plant(plant_id: str):
    plant_dic = db.plants.find_one({"_id": ObjectId(plant_id)})
    if plant_dic:
        plant_dic["_id"] = str(plant_dic['_id'])
        return plant_dic
    else:
        raise HTTPException(status_code=404, detail='没有找到数据！')


# 添加
@plant_router.post("/plant/add")
async def add_plant(plant: Plant):
    plant_dict = plant.dict()
    result = db.plants.insert_one(plant_dict)
    plant_dict["_id"] = str(result.inserted_id)
    return plant_dict


# 修改
@plant_router.put("/plant/edit/{plant_id}")
async def edit_plant(plant_id, plant: Plant):
    plant_dic = plant.dict()
    result = db.plants.update_one({"_id": ObjectId(plant_id)}, {"$set": plant_dic})
    if result.modified_count == 1:
        plant_dic['_id'] = plant_id
        return plant_dic
    else:
        raise HTTPException(status_code=404, detail='没有找到数据！')


# 删除一条

@plant_router.delete("/plant/delete/{plant_id}")
async def delete_plant(plant_id):
    result = db.plants.delete_one({"_id": ObjectId(plant_id)})
    if result.deleted_count == 1:
        return {"message": "删除成功！"}
    else:
        raise HTTPException(status_code=404, detail='没有找到数据！')

```

- middleware.py

```python
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

```

- run.py

```python
# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

from FASTAPI_Plant.resource.plant_resource import plant_router

app = FastAPI()
app.include_router(plant_router)

from FASTAPI_Plant.middleware import *

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=9002)

```