from preprocess import work_df
from preprocess import work_df_stand
import pandas as pd
import seaborn as sns
pd.set_option('display.max_columns', 500)

sns.distplot(work_df['r_kills'])

sns.lineplot(data=work_df, x='r_kills', y='radiant_win')

corr_matrix = work_df_stand.corr()
sns.heatmap(corr_matrix, square=True, yticklabels=True, xticklabels=True)
