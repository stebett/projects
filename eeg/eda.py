import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)

data = pd.read_csv('/home/ginko/Documents/projects/eeg/data/EEG_data.csv')

print(data.head())

data['Delta'].plot()
data['Alpha1'].plot()
data['Alpha2'].plot()
plt.show()

data.describe()

data['SubjectID'].shape
