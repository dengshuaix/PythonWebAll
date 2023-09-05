# -*-coding:utf-8-*-
# 2022/2/8
### 决策树
from sklearn import tree
from sklearn.datasets._california_housing import fetch_california_housing
from sklearn.model_selection import train_test_split

housing = fetch_california_housing()
print('housing.target: ', housing.target)  # housing.target:  [4.526 3.585 3.521 ... 0.923 0.847 0.894]
data_train, data_test, target_train, target_test = train_test_split(housing.data,
                                                                    housing.target,
                                                                    test_size=0.1,  # 取10%的数据集
                                                                    random_state=42
                                                                    )

dtr = tree.DecisionTreeRegressor(random_state=42)
dtr.fit(data_train, target_train)
print('决策树得分:')
print(dtr.score(data_test, target_test))  # 0.6310922690494536

### 随机森林
from sklearn.ensemble import RandomForestRegressor

rfr = RandomForestRegressor(random_state=42)
rfr.fit(data_train, target_train)
print('随机森林得分:')
print(rfr.score(data_test, target_test))  # 0.8103647255362918
