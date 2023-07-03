# -*- coding: utf-8 -*-
# 自动实现增删改查，但是非常难使用，强烈不推荐
from eve import Eve
from eve.io.mongo import Mongo

SETTINGS = {
    "DOMAIN": {
        "plants": {
            "schema": {
                "name": {"type": "string", "required": True},
                "color": {"type": "string", "required": True},
            }
        }
    },
    "MONGO_URI": "mongodb://127.0.0.1:127.0.0.1:27017/plants"

}


class PlantsMongo(Mongo):
    def __init__(self, app):
        super().__init__(app)
        self.driver.db['plants'].create_index('name', unique=True)


app = Eve(settings=SETTINGS)
if __name__ == '__main__':
    app.run(host="127.0.0.1")
    # app.run(host='127.0.0.1',port=5010)
