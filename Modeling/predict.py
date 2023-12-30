# Imports
import os
import numpy as np
import pandas as pd

import pickle
import tweepy

import re
import time
from datetime import datetime


twitter_keys = {
    'consumer_key': os.environ.get('consumer_key', None),
    'consumer_secret': os.environ.get('consumer_secret', None),
    'access_token_key': os.environ.get('access_token_key', None),
    'access_token_secret': os.environ.get('access_token_secret', None)
}

# Get fully-trained KNNClassifier model
with open('modeling/model.pickle', 'rb') as read_file:
    knn_model = pickle.load(read_file)

# Set up connection to Twitter API
# auth = tweepy.OAuthHandler(
#     twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
# auth.set_access_token(
#     twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

# api = tweepy.API(auth)


def get_user_features(screen_name):
    '''
    Input: a Twitter handle (screen_name)
    Returns: a list of account-level information used to make a prediction 
            whether the user is a bot or not
    '''

    try:
        # Get user information from screen name
        user = api.get_user(screen_name)

        # account features to return for predicton
        account_age_days = (datetime.now() - user.created_at).days
        verified = user.verified
        geo_enabled = user.geo_enabled
        default_profile = user.default_profile
        default_profile_image = user.default_profile_image
        favourites_count = user.favourites_count
        followers_count = user.followers_count
        friends_count = user.friends_count
        statuses_count = user.statuses_count
        average_tweets_per_day = np.round(statuses_count / account_age_days, 3)

        # manufactured features
        hour_created = int(user.created_at.strftime('%H'))
        network = np.round(np.log(1 + friends_count)
                           * np.log(1 + followers_count), 3)
        tweet_to_followers = np.round(
            np.log(1 + statuses_count) * np.log(1 + followers_count), 3)
        follower_acq_rate = np.round(
            np.log(1 + (followers_count / account_age_days)), 3)
        friends_acq_rate = np.round(
            np.log(1 + (friends_count / account_age_days)), 3)

        # organizing list to be returned
        account_features = [verified, hour_created, geo_enabled, default_profile, default_profile_image,
                            favourites_count, followers_count, friends_count, statuses_count,
                            average_tweets_per_day, network, tweet_to_followers, follower_acq_rate,
                            friends_acq_rate]

    except:
        return 'User not found'

    return account_features if len(account_features) == 14 else f'User not found'


def bot_or_not(twitter_handle):
    '''
    Takes in a twitter handle and predicts whether or not the user is a bot
    Required: trained classification model (KNN) and user account-level info as features
    '''
    # check if twitter handle is a screen name, use api to get information and predict
    if isinstance(twitter_handle, str):
        user_features = get_user_features(twitter_handle)
    # if input is list of features, use model to predict
    elif isinstance(twitter_handle, list):
        user_features = twitter_handle
    else:
        return 'Invalid input'

    if user_features == 'User not found':
        return 'User not found'

    else:
        # features for model
        features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
                    'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
                    'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']

        # creates df for model.predict() format
        user_df = pd.DataFrame(np.matrix(user_features), columns=features)

        prediction = knn_model.predict(user_df)[0]

        return "Bot" if prediction == 1 else "Not a bot"


def bot_proba(twitter_handle):
    '''
    Takes in a twitter handle and provides probability of whether or not the user is a bot
    Required: trained classification model (KNN) and user account-level info from get_user_features
    '''
    if isinstance(twitter_handle, str):
        user_features = get_user_features(twitter_handle)
    # if input is list of features, use model to predict
    elif isinstance(twitter_handle, list):
        user_features = twitter_handle
        
    if user_features == 'User not found':
        return 'User not found'
    else:
        features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
                    'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
                    'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']
        user_df = pd.DataFrame([user_features], columns=features)
        proba = knn_model.predict_proba(user_df)[:, 1][0] * 100
        return round(proba, 2)
    

# features = ['verified', 'hour_created', 'geo_enabled', 'default_profile', 'default_profile_image',
#             'favourites_count', 'followers_count', 'friends_count', 'statuses_count', 'average_tweets_per_day',
#             'network', 'tweet_to_followers', 'follower_acq_rate', 'friends_acq_rate']


example = {
    "id": 787405734442958848,
    "name": "Ada Kuzucu",
    "screen_name": "best_in_dumbest",
    "location": "Harriman, TN",
    "description": "artist slash designer... co-creator MONKEY PRINCE (dc comics). former XMEN CHILDREN OF THE ATOM (marvel), TEEN TITANS, SUPERMAN",
    "url": "https://t.co/abcdefg",
    "followers_count": 1509,
    "friends_count": 4,
    "listed_count": 0,
    "created_at": "2016-10-15 21:32:11",
    "favourites_count": 0,
    "verified": 0,
    "geo_enabled": 0,
    "default_profile": 0,
    "default_profile_image": 0,
    "favourites_count": 9,
    "statuses_count": 10746,
    "everage_tweets_per_day": 7.867,
}

account_age_days = (datetime.now() - datetime.strptime(example['created_at'], '%Y-%m-%d %H:%M:%S')).days

hours_created = int(datetime.strptime(
    example['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%H'))

network = np.round(np.log(1 + example['friends_count'])
                   * np.log(1 + example['followers_count']), 3)
tweet_to_followers = np.round(
    np.log(1 + example['statuses_count']) * np.log(1 + example['followers_count']), 3)
follower_acq_rate = np.round(
    np.log(1 + (example['followers_count'] / account_age_days)), 3)
friends_acq_rate = np.round(
    np.log(1 + (example['friends_count'] / account_age_days)), 3)


# get user features from example by get values from dictionary
example_user = [example['verified'], hours_created, example['geo_enabled'], example['default_profile'], example['default_profile_image'],
                example['favourites_count'], example['followers_count'], example['friends_count'], example['statuses_count'],
                example['everage_tweets_per_day'], network, tweet_to_followers, follower_acq_rate,
                friends_acq_rate]

print(f"User information: {example}\n")
print(example_user)


# example
print(f"User is {bot_or_not(example_user)}\n")

print(f"Probability {bot_proba(example_user)}%")

    
