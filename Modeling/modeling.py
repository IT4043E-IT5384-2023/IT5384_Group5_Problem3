# Basics
import pandas as pd
import psycopg2 as pg
import numpy as np
import pickle

# Visuals
import matplotlib.pyplot as plt
import seaborn as sns
from evaluation import *

# Models
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC

# Model support
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix, f1_score, auc,
                             precision_score, recall_score, roc_auc_score, roc_curve, 
                             precision_recall_curve)
from sklearn.model_selection import KFold






raw_df = pd.read_csv('C:\\Users\\Admin\\Desktop\\2023.1\\BigData\\btl\\IT5384_Group5_Problem3\\Modeling\\twitter_account_dataset.csv')
raw_df = raw_df.drop(['Unnamed: 0'], axis=1)

raw_df['bot'] = raw_df['account_type'].apply(lambda x: 1 if x == 'bot' else 0)
raw_df['default_profile'] = raw_df['default_profile'].astype(int)
raw_df['default_profile'] = raw_df['default_profile'].astype(int)
raw_df['default_profile_image'] = raw_df['default_profile_image'].astype(int)
raw_df['geo_enabled'] = raw_df['geo_enabled'].astype(int)
raw_df['verified'] = raw_df['verified'].astype(int)

# datetime conversion
raw_df['created_at'] = pd.to_datetime(raw_df['created_at'])
# hour created
raw_df['hour_created'] = pd.to_datetime(raw_df['created_at']).dt.hour

# usable df setup
df = raw_df[['bot', 'screen_name', 'created_at', 'hour_created', 'verified', 'location', 'geo_enabled', 'lang', 
             'default_profile', 'default_profile_image', 'favourites_count', 'followers_count', 'friends_count', 
             'statuses_count', 'average_tweets_per_day', 'account_age_days']]

del raw_df

# Interesting features to look at: 
df['avg_daily_followers'] = np.round((df['followers_count'] / df['account_age_days']), 3)
df['avg_daily_friends'] = np.round((df['followers_count'] / df['account_age_days']), 3)
df['avg_daily_favorites'] = np.round((df['followers_count'] / df['account_age_days']), 3)

# Log transformations for highly skewed data
df['friends_log'] = np.round(np.log(1 + df['friends_count']), 3)
df['followers_log'] = np.round(np.log(1 + df['followers_count']), 3)
df['favs_log'] = np.round(np.log(1 + df['favourites_count']), 3)
df['avg_daily_tweets_log'] = np.round(np.log(1+ df['average_tweets_per_day']), 3)

# Possible interactive features
df['network'] = np.round(df['friends_log'] * df['followers_log'], 3)
df['tweet_to_followers'] = np.round(np.log( 1 + df['statuses_count']) * np.log(1+ df['followers_count']), 3)

# Log-transformed daily acquisition metrics for dist. plots
df['follower_acq_rate'] = np.round(np.log(1 + (df['followers_count'] / df['account_age_days'])), 3)
df['friends_acq_rate'] = np.round(np.log(1 + (df['friends_count'] / df['account_age_days'])), 3)
df['favs_rate'] = np.round(np.log(1 + (df['friends_count'] / df['account_age_days'])), 3)

features = ['verified', 
            #'created_at',
            #'hour_created',
            #'lang',
            #'acct_location',
            'geo_enabled', 
            'default_profile', 
            'default_profile_image', 
            'favourites_count', 
            'followers_count', 
            'friends_count', 
            'statuses_count', 
            'average_tweets_per_day',
            #'avg_daily_followers', 
            #'avg_daily_friends',
            #'avg_daily_favorites',
            'network', 
            'tweet_to_followers', 
            'follower_acq_rate', 
            'friends_acq_rate', 
            'favs_rate'
           ]

X = df[features]
y = df['bot']

X, X_test, y, y_test = train_test_split(X, y, test_size=.3, random_state=1234)

model = KNeighborsClassifier(n_neighbors=10)

# Scaling
scalar = StandardScaler()
scalar.fit(X)
X_train_scaled = scalar.transform(X)

kf = KFold(n_splits=5, shuffle=True, random_state=33)
kf = KFold(n_splits=5, shuffle=True, random_state=33)

# Accuracy scores lists
acc_scores, prec_scores, recall_scores, f1_scores, roc_auc_scores = [], [], [], [], []

X_kf, y_kf = np.array(X), np.array(y)

for train_ind, val_ind in kf.split(X, y):

    X_train, y_train = X_kf[train_ind], y_kf[train_ind]
    X_val, y_val = X_kf[val_ind], y_kf[val_ind]

    # Fit model and make predictions
    model.fit(X_train, y_train)
    pred = model.predict(X_val)

    # Score model and append to list
    acc_scores.append(accuracy_score(y_val, pred))
    prec_scores.append(precision_score(y_val, pred))
    recall_scores.append(recall_score(y_val, pred))
    f1_scores.append(f1_score(y_val, pred))
    roc_auc_scores.append(roc_auc_score(y_val, model.predict_proba(X_val)[:,1]))

print(f'Model: {model}')
print("-"*30)
print(f'Accuracy:  {np.mean(acc_scores):.5f} +- {np.std(acc_scores):5f}')
print(f'Precision: {np.mean(prec_scores):.5f} +- {np.std(prec_scores):5f}')
print(f'Recall:    {np.mean(recall_scores):.5f} +- {np.std(recall_scores):5f}')
print(f'F1 Score:  {np.mean(f1_scores):.5f} +- {np.std(f1_scores):5f}')
print(f'ROC AUC:   {np.mean(roc_auc_scores):.5f} +- {np.std(roc_auc_scores):5f}')
print("")


preds = model.predict(X_test)

metrics_report(y_test, preds)


print(model)

with open('modeling/model.pickle', 'wb') as to_write:
   pickle.dump(model, to_write)