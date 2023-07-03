# -*- coding: utf-8 -*-
from sanic import Sanic, NotFound, HTTPResponse
from sanic.response import json
from bson.objectid import ObjectId

from Sanic_Plant.middleware import before_request, during_request, after_request
from utils.mongodb_tool import db

app = Sanic(__name__)


@app.route('/plants')  # 获取全部植物
async def get_all_plants(request):  # 定义异步函数
    plants = []
    for plant in db.plants.find():
        plants.append(plant)
    # plants = list(db.plants.find())  # db中获取数据
    plants = [{k: str(v) for k, v in each_plant.items()} for each_plant in plants]
    return json(plants)  # 响应数据


@app.route('/plant/<o_id:str>')  # 获取一个植物
async def get_one_plant(request, o_id):  # 定义异步函数
    if not o_id:
        return HTTPResponse("请求数据有误", status=400)

    plant = db.plants.find_one({"_id": ObjectId(o_id)})
    if not plant:
        return HTTPResponse("未找到植物数据", status=400)
    plant['_id'] = str(plant['_id'])
    return json(plant)  # 响应数据


@app.route('/plant/add', methods=['POST'])
async def add_plant(request):
    plant_data = request.json
    print(plant_data, type(plant_data))
    # mongo 新增一条数据， insert_one
    result = db.plants.insert_one(plant_data)

    return json({
        "inserted_id": str(result.inserted_id),
        "method": "add",
        "message": "新增成功！"

    })


@app.route('/plant/edit/<o_id:str>', methods=['PUT'])
async def put_plant(request, o_id):
    if not o_id:
        return HTTPResponse("请求数据有误", status=400)

    # 获取 body 数据
    plant_data = request.json

    # 判断是否存在
    plant = db.plants.find_one({"_id": ObjectId(o_id)})
    if not plant:
        return HTTPResponse("未找到植物数据", status=400)

    # mongodb 更新一条数据 update_one
    result = db.plants.update_one({"_id": ObjectId(o_id)}, {"$set": plant_data})
    return json({
        "upserted_id": str(result.upserted_id or '') or '',
        "method": "update",
        "message": "修改成功！"

    })


@app.route('/plant/delete/<o_id:str>', methods=['delete'])
async def delete_plant(request, o_id):
    if not o_id:
        return HTTPResponse("请求数据有误", status=400)
    # 判断是否存在
    plant = db.plants.find_one({"_id": ObjectId(o_id)})
    if not plant:
        return HTTPResponse("未找到植物数据", status=400)

    # mongodb 删除一条数据 update_one
    result = db.plants.delete_one({"_id": ObjectId(o_id)})

    return json({
        "deleted_count": str(result.deleted_count),
        "method": "delete",
        "message": "删除成功！"
    })


# 注册 中间件
app.register_middleware(before_request, "request")
app.register_middleware(during_request, "request")
app.register_middleware(after_request, "response")

if __name__ == '__main__':
    app.run('127.0.0.1', port=9001)
