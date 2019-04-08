import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)

data = pd.read_csv('/home/ginko/Documents/projects/eeg/data/EEG_data.csv')

print(data.head())

data.describe()

data['Delta'].plot()
data['Alpha1'].plot()
data['Alpha2'].plot()
plt.show()

data['Delta'].loc[(data['SubjectID'] == 1) & (data['VideoID'] == 1)].plot()
data['Alpha1'].loc[(data['SubjectID'] == 1) & (data['VideoID'] == 1)].plot()
plt.show()

sns.barplot(data=data, x='SubjectID', y='Attention', palette='BrBG')
plt.show()

sns.distplot(data['Alpha1'].loc[(data['SubjectID'] == 1)
                                & (data['VideoID'] == 1)])

sns.distplot(data['Alpha2'].loc[(data['SubjectID'] == 1)
                                & (data['VideoID'] == 1)])

sns.distplot(data['Theta'].loc[(data['SubjectID'] == 1)
                               & (data['VideoID'] == 1)])
plt.show()

waves = ['Delta', 'Theta', 'Alpha1', 'Alpha2',
         'Beta1', 'Beta2', 'Gamma1', 'Gamma2']

minmax = data[waves].describe().loc[['min', 'max']]

(data[waves] / 10**4).describe()

