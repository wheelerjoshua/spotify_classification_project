# About this project

## Executive Summary
### Goal
### Key Findings (application to business)
### Recommendations
### Next Steps

## Project Goal
The goal of this project is to predict the genres of songs based on user's top songs.

## Project Description
This project utilizes a user's Spotify data to retrieve the discography of each artist in the user's top artists and then predicts the genre of each song. This may be used in creating recommendations to users based on genre.

## Initial Questions
1. 
2. 
3. 
4. 

## Data Dictionary

## The Plan
### Acquire
Acquisition is performed using credentials acquired from Spotify's developer platform and spotipy's modules to make acquisition easier. Data is pulled from a user's top artists of all timeframes, then the artist's discography is acquired and stored in a dataframe. The song ID is used to read Spotify's track features and used to create a dataframe containing all song information.

### Prepartion
Upon acquisition, it appears the only further preparation is simplifying the genre data.

### Wrangle
Compile acquire and prepare modules and include a split function

### Exploratory Data Analysis
#### Scale data
Scale data for clustering purposes.

#### Compare audio features
Use visualizations to compare audio features to each other and identify drivers of genre

#### Examine potential for clusters
Explore relationships of audio features to each other and how they may be clustered

#### Encode clusters
If clusters are found useful, encode them for modeling

#### Statistical tests
Perform statistical Tests to find relationship between genre and features/clusters.

### Model
- Evaluate a baseline
- Create models
- Evaluate on train and validate
- Top performer evaluated on Test


## Steps to Reproduce
What did I do to get here?

- Install Spotipy python package
- Create Spotify app for credentials
- Store credentials in env.py
- Use credentials and spotipy functions to retrieve data from Spotify
- Store data in a .csv
- Create an acquire.py module to easily reproduce data acquisition
- 