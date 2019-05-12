from preprocess import work_df
from preprocess import work_df_stand
from scipy import stats
import pandas as pd
import seaborn as sns
pd.set_option('display.max_columns', 500)
%matplotlib qt5

df = work_df_stand

sns.distplot(work_df['r_kills'])

sns.lineplot(data=work_df, x='r_kills', y='radiant_win')

corr_matrix = df.corr()
sns.heatmap(corr_matrix, square=True, yticklabels=True, xticklabels=True)

sns.lineplot(data=df, x='r_creeps_stacked', y='radiant_win')

# Spotting outliers
var = 'r_kills'
sns.boxplot(data=df[var])

df.loc[df[var]>0.83][var].value_counts()

sns.boxplot(data=df.loc[df[var]<0.71][var])

((df.loc[df[var]>0.71].shape[0])/df.shape[0])*100

df[var].std()
df[var].mean()

df.head(0)

def remove_outliers(dataset):
    dataset[(np.abs(stats.zscore(dataset)) < 3).all(axis=1)]
    return dataset


