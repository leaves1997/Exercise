# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import jieba

df_clean = pd.read_csv('cleanDATE.csv')

# 各行业招聘信息数量柱状图绘制
title_info = df_clean.groupby('Title').size()
title_info = title_info.reset_index()
title_info.columns = ['title', 'count']
x = title_info['title']
y = title_info['count']
plt.barh(x, y, label='数量')
plt.title('各行业招聘信息数量统计表')
for y, x in zip(x, y):
    plt.text(x+0.05, y, '%.0f' % x, ha='left', va='center')
plt.show()

# 工资分布饼图绘制
salary_info = df_clean['salary'].value_counts()
salary_info = salary_info.reset_index()
salary_info.columns = ['salary', 'count']
s = salary_info['count'].sum()
per = [i/s for i in salary_info['count']]
plt.pie(per, labels=salary_info['salary'], autopct='%1.2f%%')
plt.title('全行业工资水平分布图')
plt.show()

# 计算机互联网行业工资分布饼图绘制
IT = df_clean.groupby('Title').get_group('计算机/互联网/通信/电子')
ITsalary = IT['salary'].value_counts()
ITsalary = ITsalary.reset_index()
ITsalary.columns = ['salary', 'count']
s = ITsalary['count'].sum()
per = [i/s for i in ITsalary['count']]
plt.pie(per, labels=ITsalary['salary'], autopct='%1.2f%%')
plt.title('计算机/互联网/通信/电子行业工资水平分布图')
plt.show()

# 计算机互联网行业经验要求饼图
ITexp = IT['experience'].value_counts()
ITexp = ITexp.reset_index()
ITexp.columns = ['experience', 'count']
s = ITexp['count'].sum()
per = [i/s for i in ITexp['count']]
plt.pie(per, labels=ITexp['experience'], autopct='%1.2f%%')
plt.title('计算机/互联网/通信/电子行业经验要求')
plt.show()

# 房地产行业工资分布饼图绘制
RE = df_clean.groupby('Title').get_group('建筑/房地产/物业')
REsalary = RE['salary'].value_counts()
REsalary = REsalary.reset_index()
REsalary.columns = ['salary', 'count']
s = REsalary['count'].sum()
per = [i/s for i in REsalary['count']]
plt.pie(per, labels=REsalary['salary'], autopct='%1.2f%%')
plt.title('建筑/房地产/物业行业工资水平分布图')
plt.show()

# 房地产行业经验要求饼图
RE = df_clean.groupby('Title').get_group('建筑/房地产/物业')
REexp = RE['experience'].value_counts()
REexp = REexp.reset_index()
REexp.columns = ['experience', 'count']
s = REexp['count'].sum()
per = [i/s for i in REexp['count']]
plt.pie(per, labels=REexp['experience'], autopct='%1.2f%%')
plt.title('建筑/房地产/物业行业经验要求')
plt.show()

# 金融行业工资分布饼图绘制
FI = df_clean.groupby('Title').get_group('财务/金融/银行/保险/信托')
FIsalary = FI['salary'].value_counts()
FIsalary = FIsalary.reset_index()
FIsalary.columns = ['salary', 'count']
s = FIsalary['count'].sum()
per = [i / s for i in FIsalary['count']]
plt.pie(per, labels=FIsalary['salary'], autopct='%1.2f%%')
plt.title('财务/金融/银行/保险/信托行业工资水平分布图')
plt.show()
