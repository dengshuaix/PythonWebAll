# -*-coding:utf-8-*-
# 2022/2/8
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

housing = fetch_california_housing()
print('housing.target: ', housing.target)  # housing.target:  [4.526 3.585 3.521 ... 0.923 0.847 0.894]
data_train, data_test, target_train, target_test = train_test_split(housing.data,
                                                                    housing.target,
                                                                    test_size=0.1,  # 取10%的数据集
                                                                    random_state=42
                                                                    )
tree_param_grid = {"min_samples_split": list((3, 6, 9)),
                   "n_estimators": list((10, 50, 100))}
grid = GridSearchCV(RandomForestRegressor(), param_grid=tree_param_grid, cv=5)
# cv 对 训练集交叉验证
grid.fit(data_train,target_train)
print(grid.cv_results_)
print()
print(grid.best_params_)
print()
print(grid.best_score_)
