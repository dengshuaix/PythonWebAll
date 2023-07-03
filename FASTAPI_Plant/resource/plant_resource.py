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
