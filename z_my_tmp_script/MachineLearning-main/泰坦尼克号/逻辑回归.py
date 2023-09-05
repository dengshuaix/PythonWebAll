# -*-coding:utf-8-*-
# 2022/2/13
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate,cross_val_score

# 1. 数据读取   和  清洗
titanic = pd.read_csv('train.csv')
print('打印描述')
print(titanic.describe())
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

predictors = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

alg = LogisticRegression(random_state=1)
scores = cross_val_score(alg, titanic[predictors], titanic['Survived'], cv=3)
print(scores.mean())
