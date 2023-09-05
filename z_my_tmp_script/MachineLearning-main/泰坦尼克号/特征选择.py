# -*-coding:utf-8-*-
# 2022/2/13
from sklearn.feature_selection import SelectKBest, f_classif

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import re


def get_title(name):
    title_search = re.search('([A-Za-z])+\.', name)
    if title_search:
        return title_search.group(0).split('.')[0]
    return ""


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

#  1. 增加 Title 特征
titanic['FamilySize'] = titanic['SibSp'] + titanic['Parch']
# 2. 增加名字处理特征
titanic['NameLength'] = titanic['Name'].apply(lambda x: len(x))

# 3. 增加 人物分类 Title
titles = titanic['Name'].apply(get_title)
# print(titles)
print('统计名称:', pd.value_counts(titles))
title_mapping = {

    "Mr": 1, "Miss": 2, "Mrs": 3,
    "Master": 4, "Dr": 5, "Rev": 6,
    "Major": 7, "Col": 7, "Don": 8, "Mme": 2,
    "Ms": 2, "Lady": 2, "Sir": 1, "Mlle": 2,
    "Capt": 7, "Countess": 9, "Jonkheer": 9,

}
for k, v in title_mapping.items():
    titles[titles == k] = v

titanic['Title'] = titles

predictors = ['Title', 'FamilySize', 'NameLength', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

# 最优特征选择
selector = SelectKBest(f_classif, k=5)
selector.fit(titanic[predictors], titanic['Survived'])
scores = -np.log10(selector.pvalues_)

# 绘制 条形图
plt.bar(range(len(predictors)), scores)
plt.xticks(range(len(predictors)), predictors, rotation='vertical')
# plt.show()
plt.savefig('./特征重要程度.png')
