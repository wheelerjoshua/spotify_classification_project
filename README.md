# Executive Summary
## Goal
The goal of this project is to predict the popularity of songs based on user's top artists.
## Key Findings (application to business)

## Recommendations

## Next Steps


# About this project

## Project Goal
The goal of this project is to predict the popularity of songs based on user's top artists.

## Project Description
This project utilizes a user's Spotify data to retrieve the discography of each artist in the user's top artists and then predicts the popularity of each song.

## Initial Questions
1. 
2. 
3. 
4. 

## Data Dictionary

## The Plan
### Acquire
Acquisition is performed using credentials acquired from Spotify's developer platform and spotipy's modules to make acquisition easier. Data is pulled from a user's top artists of all timeframes, then the artist's discography is acquired and stored in a dataframe. The song ID is used to read Spotify's track features and used to create a dataframe containing all song information.

### Prepare
Upon acquisition, duplicates are dropped. A duration_minutes column is created from duration_ms and the latter is dropped. The data is ready to be scaled.

### Wrangle
Compile acquire and prepare modules and include a split function

### Exploratory Data Analysis

#### Compare audio features
Use visualizations to compare audio features to each other and identify drivers of popularity

#### Cluster
Scale data for clustering purposes.
Explore relationships of audio features to each other and how they may be clustered.
If clusters are found useful, encode them for modeling.

#### Statistical tests
Perform statistical tests to find relationship between genre and features/clusters.

### Regression Models
- Evaluate a baseline
- Create models
- Evaluate on train and validate
- Top performer evaluated on test


## Steps to Reproduce
What did I do to get here?

- Install Spotipy python package
- Create Spotify app for credentials
- Store credentials in env.py
- Use credentials and spotipy functions to retrieve data from Spotify
- Store data in a .csv
- Create an acquire.py module to easily reproduce data acquisition
- 