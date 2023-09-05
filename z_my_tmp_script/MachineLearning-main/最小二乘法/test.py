# -*-coding:utf-8-*-
# 2021/10/20
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

nobs = 100
X = np.random.random((nobs, 2))
print(X)
X = sm.add_constant(X)
beta = [1, .1, .5]
print(beta)
e = np.random.random(nobs)
y = np.dot(X, beta) + e
result = sm.OLS(y, X).fit()
print(result.summary())
