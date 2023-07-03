# -*- coding: utf-8 -*-
import json
import tornado.ioloop
import tornado.web
from bson import ObjectId

from utils.mongodb_tool import db

settings = {
    "db": db,
    "static_path": "static",
    "template_path": "templates"
}


class PlantsHandler(tornado.web.RequestHandler):
    def initialize(self) -> None:
        self.db = self.settings['db']

    def get(self):
        """
            # 查询 1条/全部数据
        :param plant_id:
        :return:
        """
        plants = []
        for each_plant in self.db.plants.find():
            each_plant['_id'] = str(each_plant['_id'])
            plants.append(each_plant)
        self.write(json.dumps({"plants": plants, "status": 200}))

    def post(self):
        plant_dict = json.loads(self.request.body)
        result = self.db.plants.insert_one(plant_dict)
        self.write(json.dumps({"message": "新增成功", "status": 200, "inserted_id": str(result.inserted_id)}))


class PlantHandler(tornado.web.RequestHandler):
    def initialize(self) -> None:
        self.db = self.settings['db']

    def get(self, plant_id):
        one_plant_dict = self.db.plants.find_one({"_id": ObjectId(plant_id)})
        if not one_plant_dict:
            one_plant_dict = {}
            message = "查询结果不存在！"
        else:
            one_plant_dict['_id'] = str(one_plant_dict['_id'])
            message = "查询成功！"

        return self.write(json.dumps({"data": one_plant_dict, "message": message}))

    def put(self, plant_id):
        new_plant_dic = json.loads(self.request.body)
        update_result = self.db.plants.update_one({"_id": ObjectId(plant_id)}, {"$set": new_plant_dic})

        message = "更新成功" if update_result.upserted_id else "无变更/更新失败"
        return self.write(json.dumps({"message": message}))

    def delete(self, plant_id):
        delete_result = self.db.plants.delete_one({"_id": ObjectId(plant_id)})
        message = "删除成功" if delete_result.deleted_count else "删除失败！"
        return self.write(json.dumps({"message": message}))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/plants', PlantsHandler),
            (r'/plant/([a-fA-F0-9]{24})', PlantHandler)
        ]
        super().__init__(handlers, **settings)


if __name__ == '__main__':
    app = Application()
    app.listen(9003)
    tornado.ioloop.IOLoop.current().start()
