# -*-coding:utf-8-*-
# 2021/8/15

import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def sinplot(filp=1):
    x = np.linspace(0, 14, 100)
    for i in range(1, 7):
        plt.plot(x, np.sin(x + i * 0.5) * (7 - i) * filp)

### plt 绘制
sinplot()
plt.show()

### seaborn
sns.set()
sinplot()
plt.show()
# 设置风格 只有横线
sns.set_style('whitegrid')
data = np.random.normal(size=(20,6))+np.arange(6)/2
sns.boxplot(data=data)
plt.show()

# 没有刻度线
sns.set_style('dark')
sinplot()
plt.show()

# 设置白色背景
sns.set_style('white')
sinplot()
plt.show()

# x 和 y 添加 横线标注
sns.set_style('ticks')
sinplot()
sns.despine() #
plt.show()