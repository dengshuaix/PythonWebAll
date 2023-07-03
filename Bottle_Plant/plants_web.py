# -*- coding: utf-8 -*-

from bottle import Bottle, request, HTTPError, HTTPResponse
from bson import ObjectId
from utils.mongodb_tool import db

app = Bottle()


@app.route('/', method=['GET'])
def index():
    return HTTPResponse("index")


# 查全部
@app.get("/plants")
def get_all_plants():
    plants = []
    for each_plant in db.plants.find():
        each_plant['_id'] = str(each_plant['_id'])
        plants.append(each_plant)
    return {"plants": plants}


# 查一条
@app.get("/plant/<plant_id>")
def get_plant(plant_id: str):
    plant_dic = db.plants.find_one({"_id": ObjectId(plant_id)})
    if plant_dic:
        plant_dic["_id"] = str(plant_dic['_id'])
        return plant_dic
    else:
        raise HTTPError(404, '没有找到数据！')


# 添加
@app.post("/plant/add")
def add_plant():
    plant_dict = request.json
    result = db.plants.insert_one(plant_dict)
    plant_dict["_id"] = str(result.inserted_id)
    return plant_dict


# 修改
@app.put("/plant/edit/<plant_id>", method=['PUT'])
def edit_plant(plant_id):
    plant_dict = request.json
    result = db.plants.update_one({"_id": ObjectId(plant_id)}, {"$set": plant_dict})
    if result.modified_count == 1:
        plant_dict['_id'] = plant_id
        return plant_dict
    else:
        raise HTTPError(404, '没有找到数据！')


# 删除一条

@app.delete("/plant/delete/<plant_id>")
def delete_plant(plant_id):
    result = db.plants.delete_one({"_id": ObjectId(plant_id)})
    if result.deleted_count == 1:
        return {"message": "删除成功！"}
    else:
        raise HTTPError(404, '没有找到数据！')


if __name__ == '__main__':
    app.run(host="localhost", port=9010, debug=True)
