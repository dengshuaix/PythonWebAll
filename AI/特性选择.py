# -*- coding: utf-8 -*-
# 特性选择
# %matplotlib inline
import pandas as pd
from matplotlib import pyplot as plt

# 设置读取数据类型
pd.set_option("display.float_format", lambda x: "%.0f" % x)

# 读取数据
loan = pd.read_csv(
    "archive/accepted_2007_to_2018Q4.csv.gz", compression="gzip", low_memory=True
)

print(loan.info)

# 清晰数据
loans = loan[
    [
        "id",
        "loan_amnt",
        "term",
        "int_rate",
        "sub_grade",
        "emp_length",
        "grade",
        "annual_inc",
        "loan_status",
        "dti",
        "mths_since_recent_inq",
        "revol_util",
        "bc_open_to_buy",
        "bc_util",
        "num_op_rev_tl",
    ]
]

# remove missing value
loans = loans.dropna()

# 特征数据清洗，异常值，缺失值
q_low = loans["annual_inc"].quantile(0.08)
q_hi = loans["annual_inc"].quantile(0.92)
loans = loans[(loans["annual_inc"] < q_hi) & (loans["annual_inc"] > q_low)]
loans = loans[(loans["dti"] <= 45)]
q_hi = loans["bc_open_to_buy"].quantile(0.95)
loans = loans[(loans["bc_open_to_buy"] < q_hi)]
loans = loans[(loans["bc_util"] <= 160)]
loans = loans[(loans["revol_util"] <= 150)]
loans = loans[(loans["num_op_rev_tl"] <= 35)]

cleaner_app_type = {
    "term": {" 36 months": 1.0, " 60 months": 2.0},
    "sub_grade": {
        "A1": 1.0,
        "A2": 2.0,
        "A3": 3.0,
        "A4": 4.0,
        "A5": 5.0,
        "B1": 11.0,
        "B2": 12.0,
        "B3": 13.0,
        "B4": 14.0,
        "B5": 15.0,
        "C1": 21.0,
        "C2": 22.0,
        "C3": 23.0,
        "C4": 24.0,
        "C5": 25.0,
        "D1": 31.0,
        "D2": 32.0,
        "D3": 33.0,
        "D4": 34.0,
        "D5": 35.0,
        "E1": 41.0,
        "E2": 42.0,
        "E3": 43.0,
        "E4": 44.0,
        "E5": 45.0,
        "F1": 51.0,
        "F2": 52.0,
        "F3": 53.0,
        "F4": 54.0,
        "F5": 55.0,
        "G1": 61.0,
        "G2": 62.0,
        "G3": 63.0,
        "G4": 64.0,
        "G5": 65.0,
    },
    "emp_length": {
        "< 1 year": 0.0,
        "1 year": 1.0,
        "2 years": 2.0,
        "3 years": 3.0,
        "4 years": 4.0,
        "5 years": 5.0,
        "6 years": 6.0,
        "7 years": 7.0,
        "8 years": 8.0,
        "9 years": 9.0,
        "10+ years": 10.0,
    },
}
loans = loans.replace(cleaner_app_type)

# 训练
# 1. 删除低方差(超过90%)的特征
# 2. 删除有大量缺失值的特征
from sklearn.feature_selection import VarianceThreshold

variance = VarianceThreshold(threshold=(.9 * (1 - .9)))
variance.fit(loans)
variance.get_support()

from pandas_profiling import ProfileReport

profile = ProfileReport(loans, title='Loans Defaults Prediction', html={'style': {'full_width': True}})
print(profile)
