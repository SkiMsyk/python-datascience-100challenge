import os
import re
import pandas as pd
import matplotlib.pyplot as plt


root_dir = '../sample-source/chap02/'
m = re.compile(r'(?P<fn>.*)\.(csv|xlsx)')


for fn in os.listdir(root_dir):
    dfn = m.search(fn)
    if dfn:
        print(dfn['fn'])


uriage = pd.read_csv(root_dir + 'uriage.csv')
uriage.head()


kokyaku = pd.read_excel(root_dir + 'kokyaku_daicho.xlsx')
kokyaku.head()


uriage.columns


# uriage
uriage['purchase_date']


uriage['item_name'].unique()


uriage['item_price'].isnull().sum()


uriage.shape


uriage['customer_name'].isnull().sum()


uriage['customer_name'][0] in kokyaku['顧客名']


kokyaku.columns = ['user_name', 'kana', 'area', 'email', 'register_date']


kokyaku['user_name'].unique()


kokyaku['kana'].unique()


kokyaku['area'].unique()


kokyaku['email'].unique()


kokyaku['register_date'].unique()


uriage['purchase_date'] = pd.to_datetime(uriage['purchase_date'])
uriage['purchase_month'] = uriage['purchase_date'].dt.strftime('get_ipython().run_line_magic("Y%m')", "")
res = uriage.pivot_table(index='purchase_month', columns='item_name', aggfunc='size', fill_value=0)
res


res = uriage.pivot_table(index='purchase_month', columns='item_name', values = 'item_price', aggfunc='sum', fill_value=0)
res


print(len(pd.unique(uriage.item_name)))


def fix_item_name(x):
    x = x.str.upper()
    x = x.str.replace(' ', '')
    x = x.str.replace('　', '')
    return x


# OK
fix_item_name(uriage['item_name']).unique()


uriage['item_name'] = fix_item_name(uriage['item_name'])


uriage['purchase_date'] = pd.to_datetime(uriage['purchase_date'])
uriage['purchase_month'] = uriage['purchase_date'].dt.strftime('get_ipython().run_line_magic("Y%m')", "")
res = uriage.pivot_table(index='purchase_month', columns='item_name', aggfunc='size', fill_value=0)
res


res = uriage.pivot_table(index='purchase_month', columns='item_name', values = 'item_price', aggfunc='sum', fill_value=0)
res


uriage.isnull().any(axis=0)


price_master = dict()
for item_name in sorted(uriage['item_name'].unique()):
    price_master[item_name] = int(uriage[uriage['item_name'] == item_name]['item_price'].dropna().unique()[0])


price_table = pd.DataFrame({
    'item_name' : list(price_master.keys()),
    'item_price_comp' : list(price_master.values())
})
price_table


uriage = uriage.merge(price_table, on = 'item_name', how='left')


def fix_user_name(x):
    x = x.str.replace(' ', '')
    x = x.str.replace('　', '')
    return x


kokyaku['user_name'] = fix_user_name(kokyaku['user_name'])


flg_is_serial = kokyaku['register_date'].astype("str").str.isdigit()


pd.to_timedelta(kokyaku.loc[flg_is_serial, 'register_date'].astype('float'), unit='D') + pd.to_datetime('1900/01/01')


pd.to_datetime(kokyaku.loc[~flg_is_serial, 'register_date'])


kokyaku['register_date_comp'] = pd.concat([
    pd.to_timedelta(kokyaku.loc[flg_is_serial, 'register_date'].astype('float'), unit='D') + pd.to_datetime('1900/01/01'),
    pd.to_datetime(kokyaku.loc[~flg_is_serial, 'register_date'])
])


kokyaku


kokyaku['register_month'] = kokyaku['register_date_comp'].dt.strftime('get_ipython().run_line_magic("Y%m')", "")


kokyaku


pd.merge(uriage, kokyaku, left_on='customer_name', right_on='user_name', how='left')


cleaned_data = pd.merge(uriage, kokyaku, left_on='customer_name', right_on='user_name', how='left')[['purchase_date', 'purchase_month', 'item_name', 'item_price_comp', 'customer_name', 'kana', 'area', 'email', 'register_date_comp']]


cleaned_data


cleaned_data.to_csv('mydump.csv', index=False)


df = pd.read_csv('mydump.csv')
df.head()


byItem = df.pivot_table(index='purchase_month', columns='item_name', aggfunc='size', fill_value=0)
byItem


byPrice = df.pivot_table(index='purchase_month', columns='item_name', values='item_price_comp', aggfunc='sum', fill_value=0)
byPrice


byCustomer = df.pivot_table(index='purchase_month', columns='customer_name', aggfunc='size', fill_value=0)
byCustomer


byArea = df.pivot_table(index='purchase_month', columns='area', aggfunc='size', fill_value=0)
byArea


# 購入履歴がないユーザーがいるかどうか  
res = pd.merge(
    kokyaku[['user_name', 'register_date_comp']],
    pd.DataFrame(df.groupby('customer_name').sum()['item_price_comp']).reset_index(),
    left_on='user_name',
    right_on='customer_name',
    how='left'
)


res[res['item_price_comp'].isnull()]



