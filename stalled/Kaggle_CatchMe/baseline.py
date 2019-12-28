import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.model_selection import cross_val_score, TimeSeriesSplit, GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler

# Import datasets
times = ['time{}'.format(i) for i in range(1, 11)]
sites = ['site{}'.format(i) for i in range(1, 11)]
data_dir = '/home/ginko/Documents/projects/catch_me/data/'
train_df = pd.read_csv(data_dir + 'train_sessions.csv',
                       parse_dates=times,
                       index_col="session_id")

test_df = pd.read_csv(data_dir + 'test_sessions.csv',
                      parse_dates=times,
                      index_col="session_id")

train_df.sort_values(by='time1')

cv = CountVectorizer(ngram_range=(1, 3), max_features=50000)
with open(data_dir + 'train_sessions_text.txt') as inp_train_file:
    X_train = cv.fit_transform(inp_train_file)

with open(data_dir + 'test_sessions_text.txt') as inp_test_file:
    X_test = cv.transform(inp_test_file)

y_train = train_df['target'].astype('int').values

# Define functions
time_split = TimeSeriesSplit(n_splits=10)
logit = LogisticRegression(random_state=17, C=1, solver='liblinear')


def cv_scores(x, y, crossval=time_split, c=1):
    logreg = LogisticRegression(random_state=17, C=c, solver='liblinear')
    return cross_val_score(logreg, x, y, cv=crossval,
                           scoring='roc_auc', n_jobs=3)


c_values = np.logspace(-2, 2, 10)
logit_grid_searcher = GridSearchCV(estimator=logit,
                                   param_grid={'C': c_values},
                                   scoring='roc_auc',
                                   n_jobs=2, cv=time_split)
