# Import modules

import requests
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
from env import client_id, client_secret, redirect_uri

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

def get_spotify_top_songs_data():
    '''
    This function retrieves Spotify data for a user's top songs from all three
    time ranges Spotify tracks and writes them to JSON files and creates 
    datframes from the JSONs, including the songs from the albums the top songs came from.
    '''
    if os.path.isfile('spotify_top_songs_data.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('spotify_top_songs_data.csv', index_col=0)

    else:
        # define scope for pull
        scope = 'user-top-read'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        # Retrieve 30 Day Top
        short_term_tracks = sp.current_user_top_tracks(limit=50,offset=0,time_range='short_term')
        # Write to JSON
        with open('short_term_top_tracks.json','w',encoding='utf-8') as f:
            json.dump(short_term_tracks,f, ensure_ascii = False, indent = 4)

        # Retrieve 6 Month Top
        medium_term_tracks = sp.current_user_top_tracks(limit=50, offset = 0, time_range = 'medium_term')
        # Write to JSON
        with open('medium_term_top_tracks.json','w',encoding='utf-8') as f:
            json.dump(medium_term_tracks,f, ensure_ascii = False, indent = 4)

        # Retrieve Years Top
        long_term_tracks = sp.current_user_top_tracks(limit=50, offset = 0, time_range = 'long_term')
        # Write to JSON
        with open('long_term_top_tracks.json','w',encoding='utf-8') as f:
            json.dump(long_term_tracks,f, ensure_ascii = False, indent = 4)
        
        # Open all JSON
        with open('short_term_top_tracks.json') as f:
            short_data = json.load(f)
        with open('medium_term_top_tracks.json') as f:
            medium_data = json.load(f)
        with open('long_term_top_tracks.json') as f:
            long_data = json.load(f)
        # create short term dataframe
        artist_name = []
        artist_uri = []
        song_name = []
        song_uri = []
        album_name = []
        album_uri = []
        for track in short_data['items']:
            track['album']
            artist_name.append(track['artists'][0]['name'])
            artist_uri.append(track['artists'][0]['uri'])
            song_name.append(track['name'])
            song_uri.append(track['uri'])
            album_name.append(track['album']['name'])
            album_uri.append(track['album']['uri'])


        short_df = pd.DataFrame({'artist':artist_name,
        'song':song_name,
        'album':album_name,
        'song_uri':song_uri,
        'album_uri':album_uri,
        'artist_uri':artist_uri})
        # Create medium term dataframe
        artist_name = []
        artist_uri = []
        song_name = []
        song_uri = []
        album_name = []
        album_uri = []
        for track in medium_data['items']:
            track['album']
            artist_name.append(track['artists'][0]['name'])
            artist_uri.append(track['artists'][0]['uri'])
            song_name.append(track['name'])
            song_uri.append(track['uri'])
            album_name.append(track['album']['name'])
            album_uri.append(track['album']['uri'])

        medium_df = pd.DataFrame({'artist':artist_name,
        'song':song_name,
        'album':album_name,
        'song_uri':song_uri,
        'album_uri':album_uri,
        'artist_uri':artist_uri})
        # create long term dataframe
        artist_name = []
        artist_uri = []
        song_name = []
        song_uri = []
        album_name = []
        album_uri = []
        for track in long_data['items']:
            track['album']
            artist_name.append(track['artists'][0]['name'])
            artist_uri.append(track['artists'][0]['uri'])
            song_name.append(track['name'])
            song_uri.append(track['uri'])
            album_name.append(track['album']['name'])
            album_uri.append(track['album']['uri'])
        long_df = pd.DataFrame({'artist':artist_name,
        'song':song_name,
        'album':album_name,
        'song_uri':song_uri,
        'album_uri':album_uri,
        'artist_uri':artist_uri})
        # Combine all three dataframes into one top songs dataframe
        dfs = [short_df, medium_df, long_df]
        df = pd.concat(dfs)
        # retrieve all songs from all albums for songs in top songs, expand song dataset
        album_data = []
        for s in df.album_uri.to_list():
            album_data.append(sp.album(s))
        # create album dataframe with all songs from albums found in top songs
        artist_name = []
        artist_uri = []
        song_name = []
        song_uri = []
        album_name = []
        album_uri = []
        genre = []
        for album in album_data:
            for song in album['tracks']['items']:
                artist_name.append(song['artists'][0]['name'])
                artist_uri.append(song['artists'][0]['uri'])
                song_name.append(song['name'])
                song_uri.append(song['uri'])
                album_name.append(album['name'])
                album_uri.append(album['uri'])

        df = pd.DataFrame({'artist':artist_name,
        'song':song_name,
        'album':album_name,
        'song_uri':song_uri,
        'album_uri':album_uri,
        'artist_uri':artist_uri})
        df.drop_duplicates(inplace=True)
        # pull audio features of all songs
        audio_features = []
        for row in df.itertuples():
            audio_features.append(sp.audio_features(tracks = row.song_uri))
        # create dataframe of audio features
        audio_features_df = pd.DataFrame.from_dict(audio_features)
        # turn dicionary of columns to complete dataframe
        audio_features_df = audio_features_df[0].dropna().apply(pd.Series)
        # merge audio features data with songs dataframe
        df = pd.merge(df,audio_features_df,how='right',left_on='song_uri',right_on='uri')
        # create artist_uris dataframe to drop duplicate uris
        artist_uris = pd.DataFrame(df.artist_uri.to_list()).drop_duplicates()
        # rename columns for ease of access
        artist_uris.rename(columns={0:'uri'},inplace = True)
        # pull artist data from spotify
        artist_data = []
        for a in artist_uris.uri.to_list():
            artist_data.append(sp.artist(a))
        # create dataframe of artist data
        artist_data_df = pd.DataFrame.from_dict(artist_data)
        # drop columns I don't need to merge
        artist_data_df.drop(columns=['id','external_urls','followers','href','images','name','popularity','type'],inplace= True)
        # merge genres onto dataframe
        df = pd.merge(df,artist_data_df,how='left',left_on='artist_uri',right_on='uri')
        # drop unneccessary columns
        df.drop(columns = ['song_uri','album_uri','artist_uri','type','id','uri_x','track_href','analysis_url','uri_y'],inplace=True)
        # write to csv
        df.to_csv('spotify_top_songs_data.csv')
    return df

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

    return df