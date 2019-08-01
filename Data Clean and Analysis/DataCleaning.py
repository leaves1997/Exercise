# -*- coding: utf-8 -*-
import pandas as pd

# 数据清洗
df = pd.read_csv('info.csv')
df.columns = [
    'Title', 'position', 'url', 'company', 'salary', 'site', 'education',
    'experience', 'date'
]
df['date'] = pd.to_datetime(df['date'])
# 获得更新时间为7月16日之后的数据并将时间设置为索引
df = df.set_index('date')
df = df['2019-7-16':]
# 去重
df = df.drop_duplicates(subset='url', keep='first')
# 删除"链接"列
df.drop(['url'], inplace=True, axis=1)
# 处理"薪水","学历"两列的空值
values = {'salary': '面议', 'education': '不限'}
df = df.fillna(value=values)


# 薪水数据合并处理
def get_salary(word, method):
    position = word.find('-')
    if position != -1:
        bottom_salary = word[:position]
        top_salary = word[position + 1:]
    else:
        if word == '面议':
            bottom_salary = top_salary = 0
        else:
            bottom_salary = top_salary = word[:position - 2]
    if method == 'bottom':
        return bottom_salary
    else:
        return top_salary


df['bottom_salary'] = df.salary.apply(get_salary, method='bottom')
df.bottom_salary = df.bottom_salary.astype('int')
df['top_salary'] = df.salary.apply(get_salary, method='top')
df.top_salary = df.top_salary.astype('int')
df['avgsalary'] = df.apply(
    lambda x: (x.bottom_salary + x.top_salary) / 2, axis=1)
df = df.drop(['salary', 'bottom_salary', 'top_salary'], axis=1)


def salary_group(x):
    if x == 0:
        return '面议'
    elif x < 3000:
        return '3000以下'
    elif x < 6000:
        return '3000-6000'
    elif x < 10000:
        return '6000-10000'
    elif x < 30000:
        return '10000-30000'
    elif x < 50000:
        return '30000-50000'
    else:
        return '50000及以上'


df['salary'] = df['avgsalary'].apply(lambda x: salary_group(x))
df = df.drop(['avgsalary'], axis=1)


# 经验数据合并处理
def get_exp(word):
    post = word.find('年')
    if post != -1:
        exp = int(word[:post])
        if exp > 10:
            return '10年以上'
        elif exp > 5:
            return '5-10年'
        elif exp > 3:
            return '3-5年'
        else:
            return '1-3年'
    else:
        return word


df['experience'] = df['experience'].apply(lambda x: get_exp(x))
# 数据清洗及保存
df_clean = df
df_clean.to_csv('cleanDATE.csv', sep=',', header=True, index=True)
print('数据保存完成')
