# -*-coding:utf-8-*-
# 2022/2/13

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import cross_validate, cross_val_score, KFold

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

alg_10 = RandomForestClassifier(random_state=1, n_estimators=10, min_samples_split=2, min_samples_leaf=1)
alg_50 = RandomForestClassifier(random_state=1, n_estimators=50, min_samples_split=2, min_samples_leaf=1)

kf = KFold(n_splits=3, shuffle=True, random_state=42)
scores_10 = cross_val_score(alg_10, titanic[predictors], titanic['Survived'], cv=kf)
print(scores_10.mean())
scores_50 = cross_val_score(alg_50, titanic[predictors], titanic['Survived'], cv=kf)
print(scores_50.mean())
