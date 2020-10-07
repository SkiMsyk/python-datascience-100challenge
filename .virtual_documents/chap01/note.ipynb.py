import os
import numpy as np
import re
import pandas as pd


# chap01の関連ファイル一覧
os.listdir('../sample-source/chap01')


root_dir = '../sample-source/chap01/'


customer_master = pd.read_csv(root_dir+'customer_master.csv')


customer_master.head()


for fname in os.listdir(root_dir):
    m = re.match(r'^(?P<filename>.*)\.csv$', fname)
    if m:
        print(m['filename'])


transaction_detail_1 = pd.read_csv(root_dir + 'transaction_detail_1.csv')
transaction_detail_2 = pd.read_csv(root_dir + 'transaction_detail_2.csv')
transaction_1 = pd.read_csv(root_dir + 'transaction_1.csv')
transaction_2 = pd.read_csv(root_dir + 'transaction_2.csv')
item_master = pd.read_csv(root_dir + 'item_master.csv')


transaction_1.head()


transaction_2.head()


transaction = pd.concat([
    transaction_1,
    transaction_2
], axis=0, ignore_index=True)


transaction_detail = pd.concat([
    transaction_detail_1,
    transaction_detail_2
], axis=0, ignore_index=True)


joined_data = pd.merge(transaction_detail, transaction[['transaction_id', 'payment_date', 'customer_id']], on='transaction_id', how='left')


joined_data.head()


joined_data = pd.merge(transaction_detail, transaction[['transaction_id', 'payment_date', 'customer_id']], on='transaction_id', how='left') \
    .merge(customer_master, on='customer_id', how='left') \
    .merge(item_master, on='item_id', how='left')


joined_data.head()


joined_data['price'] = joined_data['quantity'] * joined_data['item_price']
joined_data[['quantity', 'item_price', 'price']].head()


joined_data['price'].sum() == transaction['price'].sum()


joined_data.isnull().sum()


joined_data.describe()


joined_data.dtypes


# datetime型への変換  
joined_data['payment_date'] = pd.to_datetime(joined_data['payment_date'])
joined_data['payment_month'] = joined_data['payment_date'].dt.strftime('get_ipython().run_line_magic("Y%m')", "")
joined_data.head()


joined_data.groupby('payment_month').sum()['price']


joined_data.groupby(['payment_month', 'item_name']).sum()[['price', 'quantity']]


pd.pivot_table(joined_data, index='item_name', columns='payment_month', values=['price', 'quantity'], aggfunc='sum')


import matplotlib.pyplot as plt
get_ipython().run_line_magic("matplotlib", " inline")


viz_df = pd.pivot_table(joined_data, index='payment_month', columns='item_name', values='price', aggfunc='sum')


for col in viz_df.columns:
    plt.plot(list(viz_df.index), viz_df[col], label=col)


viz_df.head()



