# -*-coding:utf-8-*-
# 2022/2/13

### 通过 集成算法,提高模型的模拟分数
import re
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold


def get_title(name):
    title_search = re.search('([A-Za-z])+\.', name)
    if title_search:
        return title_search.group(0).split('.')[0]
    return ""


# 1. 数据读取   和  清洗
titanic = pd.read_csv('train.csv')
print('打印描述')
# print(titanic.describe())
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

predictors = ['Title', 'FamilySize', 'Pclass', 'Sex', 'Age', 'Embarked']

### 集成算法

from sklearn.ensemble import GradientBoostingClassifier

algorithms = [
    [GradientBoostingClassifier(random_state=1, n_estimators=25, max_depth=3), predictors],
    [LogisticRegression(random_state=1), predictors]
]

kf = KFold(n_splits=3, shuffle=True, random_state=42)

predictions = []
for train, test in kf.split(titanic):
    train_target = titanic['Survived'].iloc[train]
    full_test_predictions = []
    for alg, predictiors in algorithms:
        alg.fit(titanic[predictiors].iloc[train, :], train_target)
        test_predictions = alg.predict_proba(titanic[predictiors].iloc[test, :].astype(float))[:, 1]
        full_test_predictions.append(test_predictions)

    test_predictions = sum(full_test_predictions) / len(full_test_predictions)
    ### 增加权重
    # test_predictions = (full_test_predictions[0] * 3 + full_test_predictions[1]) / 4

    test_predictions[test_predictions <= .5] = 0
    test_predictions[test_predictions > .5] = 1
    predictions.append(test_predictions)

# 1.
predictions = np.concatenate(predictions, axis=0)
accuracy = sum(predictions[predictions == titanic['Survived']]) / len(predictions)
print(accuracy)
