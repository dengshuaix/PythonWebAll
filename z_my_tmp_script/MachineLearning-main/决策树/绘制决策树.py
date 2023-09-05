# -*- coding: utf-8 -*-
from sklearn.datasets._california_housing import fetch_california_housing
import pydotplus
from IPython.display import Image

housing = fetch_california_housing()
print(housing.DESCR)
print(housing.data.shape)  # 形状

print(housing.data[0])

from sklearn import tree

dtr = tree.DecisionTreeRegressor(max_depth=3)
dtr.fit(housing.data[:, [6, 7]], housing.target)

### 决策树的可视化
dot_data = tree.export_graphviz(
    dtr,
    out_file=None,
    feature_names=housing.feature_names[6:8],
    filled=True,
    impurity=False,
    rounded=True
)  # 生成 dot 对象

graph = pydotplus.graph_from_dot_data(dot_data)
graph.get_nodes()[7].set_fillcolor('#FFF2DD')

image_path = "DecisionTree.png"

# 保存图片
from IPython.display import Image
Image(graph.create_png())
graph.write_png(image_path)

#
# with open(image_path, 'wb') as f:
#     f.write(graph.create_png())
