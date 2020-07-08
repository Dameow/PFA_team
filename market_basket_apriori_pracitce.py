import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 一、采用efficient_apriori工具包
from efficient_apriori import apriori
#由于这张表没有表头（head），读的时候会把第一行作为head，所以需要加一句header = None
dataset = pd.read_csv('./Market_Basket_Optimisation.csv', header = None) 
# shape为(7501,20)
print("表规模",dataset.shape) 

# 将数据存放到transactions中
transactions = []
for i in range(0, dataset.shape[0]): #shape[0]表示的是第7501行？
    temp = []
    for j in range(0, 20): #从0列到第20列
        if str(dataset.values[i, j]) != 'nan': 
           temp.append(str(dataset.values[i, j])) #到底是先从第一行的每一列开始加还是从第一列的每一行开始加[i,j]
    transactions.append(temp)
#print(transactions)
transactions_datasheet=pd.DataFrame(data=transactions)#
transactions_datasheet.to_csv('transactions_datasheet.csv')
# 挖掘频繁项集和频繁规则
itemsets, rules1 = apriori(transactions, min_support=0.05,  min_confidence=0.2)
print("频繁项集1：", itemsets)
print("关联规则1：", rules1)


# 二、采用efficient_apriori工具包
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

transactions = apriori(transactions,use_colnames=True, min_support=0.05) 
transactions = transactions.sort_values(by="support" , ascending=False) #用sort_values,按照support来进行排序
print('频繁项集2：',transactions)

rules2 =  association_rules(itemsets, metric='lift', min_threshold=1)
rules2 = rules2.sort_values(by="lift" , ascending=False) 
print('关联规则2：',rules2)