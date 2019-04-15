from sklearn import preprocessing
import pandas as pd
pd.set_option('display.max_columns', 500)


def standardize(df):
    scaler = preprocessing.MinMaxScaler()
    scaled_df = scaler.fit_transform(df)
    stand_df = pd.DataFrame(scaled_df,
                            columns=df.columns,
                            index=df.index)
    return stand_df


def group_var(fulldf, df, var):
    r_variables = ['r{}_{}'.format(n, var) for n in range(1, 6)]
    d_variables = ['d{}_{}'.format(n, var) for n in range(1, 6)]
    r_value = fulldf[r_variables].sum(axis=1)
    d_value = fulldf[d_variables].sum(axis=1)
    df = pd.concat([df, r_value, d_value], axis=1)
    df.rename(columns={0: 'r_{}'.format(var),
                       1: 'd_{}'.format(var)}, inplace=True)
    return df


def read_and_merge():
    raw_data = pd.read_csv('data/train_features.csv')

    raw_target = pd.read_csv('data/train_targets.csv')
    raw_target = raw_target.drop(['game_time', 'match_id_hash'], axis=1)

    full_raw_df = pd.concat([raw_data, raw_target], axis=1)

    return full_raw_df


def gen_work_df(full_df):
    tmp_work_df = pd.DataFrame(index=full_df.index)
    tmp_work_df['game_time'] = full_df['game_time']
    tmp_work_df['radiant_win'] = full_df['radiant_win']

    good_features = ('kills',
                     'assists',
                     'deaths',
                     'denies',
                     'gold',
                     'lh',
                     'level',
                     'stuns',
                     'creeps_stacked',
                     'firstblood_claimed',
                     'teamfight_participation',
                     'towers_killed',
                     'roshans_killed',
                     'obs_placed',
                     'sen_placed')

    for column in good_features:
        tmp_work_df = group_var(full_df, tmp_work_df, column)

    tmp_work_df = tmp_work_df.drop(['d_kills', 'd_deaths'])

    tmp_work_df_stand = standardize(tmp_work_df)

    return tmp_work_df, tmp_work_df_stand


clean_df = read_and_merge()

work_df, work_df_stand = gen_work_df(clean_df)
