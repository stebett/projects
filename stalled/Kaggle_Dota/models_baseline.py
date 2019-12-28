from sklearn import (svm,
                     tree,
                     linear_model,
                     neighbors,
                     naive_bayes,
                     ensemble,
                     discriminant_analysis,
                     gaussian_process,
                     model_selection)
from xgboost import XGBClassifier
from preprocess import work_df_stand
import pandas as pd
import seaborn as sns

MLA = [
    ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(),
    ensemble.ExtraTreesClassifier(),
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),

    gaussian_process.GaussianProcessClassifier(),

    linear_model.LogisticRegressionCV(),
    linear_model.PassiveAggressiveClassifier(),
    linear_model.RidgeClassifierCV(),
    linear_model.SGDClassifier(),
    linear_model.Perceptron(),

    naive_bayes.BernoulliNB(),
    naive_bayes.GaussianNB(),

    neighbors.KNeighborsClassifier(),

    svm.SVC(probability=True),
    svm.NuSVC(probability=True),
    svm.LinearSVC(),

    tree.DecisionTreeClassifier(),
    tree.ExtraTreeClassifier(),

    discriminant_analysis.LinearDiscriminantAnalysis(),
    discriminant_analysis.QuadraticDiscriminantAnalysis(),

    XGBClassifier()
]

cv_split = model_selection.ShuffleSplit(
    n_splits=10, test_size=.3, train_size=.6, random_state=33)

MLA_columns = ['MLA Name',
               'MLA Parameters',
               'MLA Train Accuracy Mean',
               'MLA Test Accuracy Mean',
               'MLA Test Accuracy 3*STD',
               'MLA Time']

MLA_compare = pd.DataFrame(columns=MLA_columns)

# MLA_predict = work_df_stand['radiant_win']
row_index = 0
for alg in MLA:
    MLA_name = alg.__class__.__name__
    MLA_compare.loc[row_index, 'MLA Name'] = MLA_name
    MLA_compare.loc[row_index, 'MLA Parameters'] = str(alg.get_params())

    cv_results = model_selection.cross_validate(
        alg, work_df_stand, work_df_stand['radiant_win'], cv=cv_split)

    MLA_compare.loc[row_index, 'MLA Time'] = cv_results['fit_time'].mean()
    MLA_compare.loc[row_index,
                    'MLA Train Accuracy Mean'] = cv_results['test_score'].mean()
    MLA_compare.loc[row_index,
                    'MLA Test Accuracy 3*STD'] = cv_results['test_score'].std()*3

    break
    # alg.fit(work_df_stand, MLA_predict)
    # MLA_predict[MLA_name] = alg.predict(work_df_stand)

MLA_compare.sort_values(by=['MLA Test Accuracy Mean'],
                        ascending=False, inplace=True)
sns.barplot(data=MLA_compare, x='MLA Test Accuracy Mean', y='MLA Name')
