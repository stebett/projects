from preprocess import work_df_stand
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
pd.set_option('display.max_columns', 500)

X_train, X_test, y_train, y_test = train_test_split(
    work_df_stand.drop('radiant_win', axis=1),
    work_df_stand['radiant_win'],
    test_size=0.30,
    random_state=33)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

predictions = logreg.predict(X_test)

print(metrics.classification_report(y_test, predictions))
print("Accuracy:", metrics.accuracy_score(y_test, predictions))
