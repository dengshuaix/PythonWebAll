# -*- coding: utf-8 -*-
from pydantic import BaseModel


# 定义plant模型
class Plant(BaseModel):
    name: str
    color: str
