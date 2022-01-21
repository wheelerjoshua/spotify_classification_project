# Executive Summary
## Goal
The goal of this project is to predict the popularity of songs based on user's top artists.
## Key Findings (application to business)
Strictly analyzing audio features, features that matter the most are danceability, loudness, and modality.

## Recommendations
When looking at top artist popularity per user, including a more broad generic dataset will provide consistency and variety in modeling.

## Next Steps
Acquire more data from Spotify to diversify the dataset, building a model from the diverse dataset to apply to user's top artists.

# About this project

## Project Goal
The goal of this project is to predict the popularity of songs based on user's top artists.

## Project Description
This project utilizes a user's Spotify data to retrieve the discography of each artist in the user's top artists and then predicts the popularity of each song.

## Initial Questions
1. Can meaningful clusters be created from Spotify's audio features?
2. Does a song's dancability correlate with popularity?
3. Does a song's tempo correlate with popularity?
4. Does a song's key and mode correlate with popularity?

## Data Dictionary
| variable      | meaning       |
| ------------- |:-------------:|
|popularity|target value: Popularity of the artist, calculated by popularity of all artist's tracks|
|lm|Ordinary Least Squares Linear Regression modeling algorithm|
|lm2|Polynomial Regression modeling algorithm |
|glm|TweedieRegressor modeling algorithm|
|Audio Features|
|acousticness|confidence measure of whether the track is acoustic|
|danceability|how suitable a track is for dancing|
|duration_minutes|duration of track in minutes, rounded to the nearest whole minute|
|energy|perceptual measure of intensity and activity|
|instrumentalness|predicts whether a track contains no vocals|
|key|the key the track is in|
|liveness|presence of an audience in the recording|
|loudness|overall loudness of a track in decibels|
|mode|indicates modality, with 1 being major and 0 being minor|
|speechiness|presence of spoken words in a track, with 1 being a talk show or podcast|
|tempo|overall estimated pace of a track in beats per minute|
|time_signature|estimated meter of beats in a bar, ranging from 3/4 to 7/4|
|valence|measure of how positive a song sounds|

## The Plan
### Acquire
Acquisition is performed using credentials acquired from Spotify's developer platform and spotipy's modules to make acquisition easier. Data is pulled from a user's top artists of all timeframes, then the artist's discography is acquired and stored in a dataframe. The song ID is used to read Spotify's track features and used to create a dataframe containing all song information.

### Prepare
Upon acquisition, duplicates are dropped. A duration_minutes column is created from duration_ms and the latter is dropped. The data is ready to be scaled.

### Wrangle
Compile acquire and prepare modules and include a split function

### Exploratory Data Analysis

#### Compare audio features
Use visualizations to compare audio features to popularity and identify drivers of popularity.

#### Cluster
Scale data for clustering purposes.
Explore relationships of audio features to each other and how they may be clustered.
If clusters are found useful, encode them for modeling.

#### Statistical tests
Perform statistical tests to find relationships between popularity and features/clusters.

### Regression Models
- Evaluate a baseline
- Create models
- Evaluate on train and validate
- Top performer evaluated on test


## Steps to Reproduce
What did I do to get here?

- Install Spotipy python package.
- Create Spotify app for credentials.
- Store credentials in env.py.
- Use credentials and spotipy functions to retrieve data from Spotify.
- Store data in a .csv.
- Create an acquire.py module to easily reproduce data acquisition.
- Prepare data by removing outliers, converting duration_ms to duration_minutes, and dropping unnecessary columns.
- Split the data for exploration.
- Explore the data using visualizations.
- Using SelectKBest to learn what features are strongly correlated with popularity.
- Cluster features that make sense from a musician's point of view.
- Use statistical tests to verify correlation with popularity.
- Create different feature mask options for modeling.
- Create 9 regression models, using OLS, GLM, and Polynomial for each feature mask option.
- Evaluate models on train and validate.
- Visualize residuals for models.
- Evaluate top model on test dataset.
- Conclude with key takeaways, recommendations, and next steps.