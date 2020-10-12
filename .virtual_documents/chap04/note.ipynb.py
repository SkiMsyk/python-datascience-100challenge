import pandas as pd
import os
import re
import matplotlib.pyplot as plt

root_dir = '../sample-source/chap04/'


uselog = pd.read_csv(root_dir + 'use_log.csv')


uselog.isnull().sum()


customer = pd.read_csv(root_dir + 'customer_join.csv')


customer.isnull().sum()


customer_clustering = customer[
    ['mean', 'median', 'max', 'min', 'membership_period']
]


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customer_clustering_sc = sc.fit_transform(customer_clustering)


kmeans = KMeans(n_clusters=4, random_state=10)


clusters = kmeans.fit(customer_clustering_sc)


customer_clustering


customer_clustering = customer_clustering.assign(cluster = clusters.labels_)


customer_clustering['cluster']


print(customer_clustering['cluster'].unique())


customer_clustering.head()


customer_clustering.groupby('cluster').count()


customer_clustering.groupby('cluster').mean()


from sklearn.decomposition import PCA


x = customer_clustering_sc
pca = PCA(n_components=2)
pca.fit(x)
x_pca = pca.transform(x)
pca_df = pd.DataFrame(x_pca)
pca_df['cluster'] = customer_clustering['cluster']


import matplotlib.pyplot as plt
get_ipython().run_line_magic("matplotlib", " inline")
for i in customer_clustering['cluster'].unique():
    tmp = pca_df.loc[pca_df['cluster']==i]
    plt.scatter(tmp[0], tmp[1])


customer_clustering_trends = pd.concat([customer_clustering, customer], axis=1)
customer_clustering_trends.groupby(['cluster', 'is_deleted'], as_index=False).count() \
    [['cluster', 'is_deleted', 'customer_id']]


customer_clustering_trends.groupby(['cluster', 'routine_flg'], as_index=False).count()[['cluster', 'routine_flg', 'customer_id']]


uselog['usedate'] = pd.to_datetime(uselog['usedate'])
uselog


uselog['yymm'] = uselog['usedate'].dt.strftime('get_ipython().run_line_magic("Y%m')", "")
uselog_months = uselog.groupby(['yymm', 'customer_id'], as_index=False).count()
uselog_months.rename(columns={'log_id':'count'}, inplace=True)
del uselog_months['usedate']
uselog_months.head()


year_months = list(uselog_months['yymm'].unique())
train = pd.DataFrame()
for i in range(6, len(year_months)):
    tmp = uselog_months.loc[uselog_months['yymm']==year_months[i]]
    tmp.rename(columns={'count':'count_pred'}, inplace=True)
    for j in range(1,7):
        tmp_before = uselog_months.loc[uselog_months['yymm']==year_months[i-j]]
        del tmp_before['yymm']
        tmp_before.rename(columns={'count':'count_{}'.format(j-1)}, inplace=True)
        tmp = pd.merge(tmp, tmp_before, on='customer_id', how='left')
    train = pd.concat([train, tmp], ignore_index=True)


train = train.dropna().reset_index(drop=True)
train.head()


if 'start_date' not in train.columns:
    train = pd.merge(train, customer[['customer_id', 'start_date']], on='customer_id', how='left')
train.head()


from dateutil.relativedelta import relativedelta


# 会員期間を月単位で作成 
train['period'] = None
train['now_date'] = pd.to_datetime(train['yymm'], format='get_ipython().run_line_magic("Y%m')", "")
train['start_date'] = pd.to_datetime(train['start_date'])

for i in range(len(train)):
    delta = relativedelta(train['now_date'][i], train['start_date'][i])
    train['period'][i] = delta.years*12 + delta.months


train.head()


from sklearn import linear_model
import sklearn.model_selection


train = train.loc[train['start_date'] >= pd.to_datetime('20180401')]

model = linear_model.LinearRegression()
X = train[['count_{}'.format(i) for i in range(5)] + ['period']]
X.head()


y = train['count_pred']
y


X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y)
model.fit(X_train, y_train)


print(model.score(X_train, y_train))


print(model.score(X_test, y_test))


coef = pd.DataFrame({'feature_names': X.columns, 'coefficient':model.coef_})
coef



