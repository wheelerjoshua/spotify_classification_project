# Import modules
## Normal modules
import requests
import os
import json
import pandas as pd
import numpy as np

## Spotipy modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

## Split data module
from sklearn.model_selection import train_test_split

## Scaler module
import sklearn.preprocessing

## env
from env import client_id, client_secret, redirect_uri



os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

####### Acquire #######
def get_spotify_top_artists_discography_data():
    '''
    This function pulls a user's top artists from Spotify, reads the artist's discography
    into a dataframe, including audio features and genre data.
    '''
    if os.path.isfile('spotify_top_artist_discography_data.csv'):
            
            # If csv file exists read in data from csv file.
            df = pd.read_csv('spotify_top_artist_discography_data.csv', index_col=0)

    else:
        # What I'm looking for
        scope = 'user-top-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        # Retrieve 30 Day Top
        short_term_artists = sp.current_user_top_artists(limit=50,offset=0,time_range='short_term')
        # Write to JSON
        with open('short_term_top_artists.json','w',encoding='utf-8') as f:
            json.dump(short_term_artists,f, ensure_ascii = False, indent = 4)

        # Retrieve 6 Month Top
        medium_term_artists = sp.current_user_top_artists(limit=50, offset = 0, time_range = 'medium_term')
        # Write to JSON
        with open('medium_term_top_artists.json','w',encoding='utf-8') as f:
            json.dump(medium_term_artists,f, ensure_ascii = False, indent = 4)

        # Retrieve Years Top
        long_term_artists = sp.current_user_top_artists(limit=50, offset = 0, time_range = 'long_term')
        # Write to JSON
        with open('long_term_top_artists.json','w',encoding='utf-8') as f:
            json.dump(long_term_artists,f, ensure_ascii = False, indent = 4)

        # Open all JSON
        with open('short_term_top_artists.json') as f:
            short_data = json.load(f)
        with open('medium_term_top_artists.json') as f:
            medium_data = json.load(f)
        with open('long_term_top_artists.json') as f:
            long_data = json.load(f)

        # create list of artist uri's
        artist_uri = []
        for a in short_data['items']:
            artist_uri.append(a['uri'])
        for a in medium_data['items']:
            artist_uri.append(a['uri'])
        for a in long_data['items']:
            artist_uri.append(a['uri'])

        # pull the discography for each artist
        discographies = []
        for a in artist_uri:
            discographies.append(sp.artist_albums(a))

        # pull album uris from discographies
        album_uris = []
        for artist in discographies:
            for album in artist['items']:
                album_uris.append(album['uri'])

        # create a song list from all albums
        song_list = []
        for a in album_uris:
            song_list.append(sp.album(a))

        # create dataframe of features
        artist_name = []
        artist_uri = []
        song_name = []
        song_uri = []
        album_name = []
        album_uri = []
        popularity = []
        for album in song_list:
            for song in album['tracks']['items']:
                artist_name.append(song['artists'][0]['name'])
                artist_uri.append(song['artists'][0]['uri'])
                song_name.append(song['name'])
                song_uri.append(song['uri'])
                album_name.append(album['name'])
                album_uri.append(album['uri'])
                popularity.append(album['popularity'])


        df = pd.DataFrame({'artist':artist_name,
        'song':song_name,
        'album':album_name,
        'song_uri':song_uri,
        'album_uri':album_uri,
        'artist_uri':artist_uri,
        'popularity':popularity})

        # drop duplicates of song list
        df.drop_duplicates(inplace=True)

        # pull audio features of all songs
        audio_features = []
        for row in df.itertuples():
            audio_features.append(sp.audio_features(tracks = row.song_uri))

        # create a dataframe of audio features
        audio_features_df = pd.DataFrame.from_dict(audio_features)

        # turn dicionary of columns to complete dataframe
        audio_features_df = audio_features_df[0].dropna().apply(pd.Series)

        # merge audio features data with songs dataframe
        df = pd.merge(df,audio_features_df,how='right',left_on='song_uri',right_on='uri')

        # # get genres
        # artist_data = []
        # for a in artist_uri:
        #     artist_data.append(sp.artist(a))
        # # create dataframe of artist data
        # artist_data_df = pd.DataFrame.from_dict(artist_data)

        # # merge genres onto dataframe
        # df = pd.merge(df,artist_data_df,how='left',left_on='artist_uri',right_on='uri')

        # drop unneccessary columns
        df.drop(columns = ['song_uri','album_uri','artist_uri','type','id','track_href','analysis_url','uri'],inplace=True)
        # write to csv
        df.to_csv('spotify_top_artist_discography_data.csv')
    
    df = convert_duration(df)
    # drop str columns for ease of modeling
    cols = ['song','album','artist']
    df = drop_cols(df, cols)
    df = df[df.duration_minutes < 9]
    return df


####### Prepare ########

def convert_duration(df):
    '''
    Takes in a df and converts duration in milliseconds to duration in minutes.
    '''
    df['duration_minutes'] = round(df.duration_ms / 60000).astype(int)
    df.drop(columns = 'duration_ms', inplace = True)
    return df

def drop_cols(df, cols):
    '''
    Takes in a dataframe and drops specified columns
    '''
    df = df.drop(columns=cols)
    return df

def standard_scaler(train, validate, test):
    '''
    Takes train, validate, and test dataframes as arguments and returns
    standard scaler object and scaled versions of train, validate, and test.
    '''
    scaled_vars = list(train.select_dtypes('number').columns)
    scaled_column_names = [i for i in scaled_vars]
    scaler = sklearn.preprocessing.StandardScaler()
    train_scaled = scaler.fit_transform(train[scaled_vars])
    validate_scaled = scaler.transform(validate[scaled_vars])
    test_scaled = scaler.transform(test[scaled_vars])

    train_scaled = pd.DataFrame(train_scaled, columns=scaled_column_names, index=train.index.values)
    validate_scaled = pd.DataFrame(validate_scaled, columns=scaled_column_names, index=validate.index.values)
    test_scaled = pd.DataFrame(test_scaled, columns=scaled_column_names, index= test.index.values)
    return scaler, train_scaled, validate_scaled, test_scaled

####### Split #######
def split_data(df):
    '''
    Takes in a dataframe and returns train, validate, and test subset dataframes. 
    '''
    train, test = train_test_split(df, test_size = .2, stratify = df.popularity, random_state = 222)
    train, validate = train_test_split(train, test_size = .3, stratify = train.popularity, random_state = 222)
    return train, validate, test