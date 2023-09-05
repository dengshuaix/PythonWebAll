# -*-coding:utf-8-*-
# 2022/2/10
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold

# 1. 数据读取   和  清洗
titanic = pd.read_csv('train.csv')
titanic_test = pd.read_csv('train.csv')

# 重新设置年龄
titanic['Age'] = titanic['Age'].fillna(titanic['Age'].median())

# print(titanic['Sex'].unique())  # ['male' 'female']
# 重新设置 女性和男性
titanic.loc[titanic['Sex'] == 'male', 'Sex'] = 0
titanic.loc[titanic['Sex'] == 'female', 'Sex'] = 1
# print(titanic['Sex'])

# 重新设置 登船 Embarked
# print(titanic['Embarked'].unique())  # ['S' 'C' 'Q' nan]
# 去除 nan值
titanic['Embarked'] = titanic['Embarked'].fillna('S')
titanic.loc[titanic['Embarked'] == 'S', 'Embarked'] = 0
titanic.loc[titanic['Embarked'] == 'C', 'Embarked'] = 1
titanic.loc[titanic['Embarked'] == 'Q', 'Embarked'] = 2
# print(titanic['Embarked'])

### 2. 线性回归 模型预测
predictors = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

alg = LinearRegression()
kf = KFold(n_splits=3)  # 交叉验证3次

predictions = [] # 分别得到交叉验证的模型
for train, test in kf.split(titanic[predictors]):
    train_predictors = (titanic[predictors].iloc[train, :])
    train_target = titanic['Survived'].iloc[train]
    alg.fit(train_predictors, train_target)
    test_predictions = alg.predict(titanic[predictors].iloc[test, :])
    predictions.append(test_predictions)
# print('预测 predictions:', predictions)

### 验证 模型结果
predictions = np.concatenate(predictions, axis=0)
predictions[predictions > .5] = 1
predictions[predictions < .5] = 0
accuracy = sum(predictions[predictions == titanic['Survived']]) / len(predictions)

print(accuracy)
