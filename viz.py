from matplotlib import pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


def data_landscape(df):
    fig, ax = plt.subplots(figsize = (10,10))
    df.popularity.plot(kind = 'hist', density = True, bins = 15, alpha = .7, color = 'k')
    df.popularity.plot(kind = 'kde', color = 'lime')
    plt.xlabel('Popularity')
    ax.set_xlim(0,100)
    plt.ylabel('Frequency')
    ax.set_ylim(0,0.02)
    ax.set_yticks([])
    plt.title('Popularity of Spotify User\'s Top Songs')
    ax.tick_params(left = False, bottom=False)
    for ax, spine in ax.spines.items():
        spine.set_visible(False)
    return plt.show()

def beat_cluster(X_train_beat_cluster, centroids):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111, projection = '3d')
    x = X_train_beat_cluster.energy
    y = X_train_beat_cluster.tempo
    z = X_train_beat_cluster.danceability
    ax.scatter(x,y,z, c=X_train_beat_cluster.beat_cluster, s = 40, cmap='ocean')
    ax.set_xlabel('energy', fontsize = 15)
    ax.set_ylabel('tempo',fontsize = 15)
    ax.set_zlabel('danceability',fontsize = 15)
    plt.title('Beat Clusters by Energy, Tempo, and Danceability', fontsize = 15)

def mood_cluster(X_train_mood_cluster, centroids):
    # fig = plt.figure(figsize = (10,10))
    # ax = fig.add_subplot(111, projection = '3d')
    # x = X_train_mood_cluster.mode
    # y = X_train_mood_cluster.key
    # z = X_train_mood_cluster.valence
    # ax.scatter(x,y,z, c=X_train_mood_cluster.mood_cluster, s = 40, cmap='ocean')
    # ax.set_xlabel('mode', fontsize = 15)
    # ax.set_ylabel('key',fontsize = 15)
    # ax.set_zlabel('valence',fontsize = 15)
    # plt.title('Mood Clusters by Mode, Key, and Valence',fontsize = 15)
    plt.figure(figsize = (10,10))
    sns.scatterplot(data = X_train_mood_cluster, x = 'key', y = 'valence', hue = 'mood_cluster', s = 100, alpha = 0.7, palette=['springgreen','lime','green','dimgrey'])
    centroids.plot.scatter(x='key',y='valence',ax = plt.gca(), color = 'black',alpha = 0.8, s=300, label = 'centroid')
    plt.title('Mood Clusters by Key and Valence')
    plt.legend(loc = 'upper right')

def ambience_cluster(X_train_ambience_cluster, centroids):
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111, projection = '3d')
    x = X_train_ambience_cluster.acousticness
    y = X_train_ambience_cluster.instrumentalness
    z = X_train_ambience_cluster.loudness
    ax.scatter(x,y,z, c=X_train_ambience_cluster.ambience_cluster, s = 40, cmap='ocean')
    ax.set_xlabel('acousticness', fontsize = 15)
    ax.set_ylabel('instrumentalness',fontsize = 15)
    ax.set_zlabel('loudness',fontsize = 15)
    plt.title('Ambience Clusters by Acousticness, Instrumentalness, and Loudness', fontsize = 15)

def stats_beat(train):
    plt.figure(figsize=(6,10))
    sns.scatterplot(train.beat_cluster, train.popularity, color = 'lime')
    plt.xticks([0,1,2,3])
    return plt.show()


def stats_ambience(train):
    plt.figure(figsize=(6,10))
    sns.scatterplot(train.ambience_cluster, train.popularity, color = 'lime')
    plt.xticks([0,1,2,3])
    return plt.show()

def stats_danceability(train):
    plt.figure(figsize=(10,10))
    sns.relplot(train.danceability, train.popularity, alpha = 0.1, color = 'limegreen')

def stats_loudness(train):
    plt.figure(figsize=(10,10))
    sns.relplot(train.loudness, train.popularity, alpha = 0.1, color = 'limegreen')

def validate_residuals(y_validate):
    plt.figure(figsize = (16,8))
    plt.plot(y_validate.popularity, y_validate.baseline_pred_mean, alpha=.5, color="black", label='_nolegend_')
    plt.annotate("Baseline: Predict Using Mean", (0, (38.8 + 0.1)), size = 15)
    plt.plot(y_validate.popularity, y_validate.popularity, alpha=.5, color="grey", label='_nolegend_')
    plt.annotate("The Ideal Line: Predicted = Actual", (60, 61),size = 15,rotation=26)
    plt.scatter(y_validate.popularity, y_validate.popularity_pred_lm, 
            alpha=.2, color="grey", s=100, label="Model: LinearRegression")
    plt.scatter(y_validate.popularity, y_validate.popularity_pred_lm2, 
                alpha=.5, color="green", s=100, label="Model: Polynomial")
    # plt.scatter(y_validate.popularity, y_validate.popularity_pred_lars, 
    #             alpha=.5, color="green", s=100, label="Model: LassoLars")
    plt.scatter(y_validate.popularity, y_validate.popularity_pred_glm,
                alpha=.2, color="lime",s=100,label='Model: TweedieRegressor')
    plt.xlabel('popularity')
    plt.ylabel('Model Predictions')
    plt.legend()
    return plt.show()

def validate_hist(y_validate):
    plt.figure(figsize=(16,8))
    plt.hist(y_validate.popularity, color='black', alpha = .8, label="Actual Log Error")
    plt.hist(y_validate.popularity_pred_glm, color='grey', alpha=.5, label="Model: TweedieRegressor")
    plt.hist(y_validate.popularity_pred_lm2, color='green', alpha=.7, label="Model 2nd degree Polynomial")
    plt.hist(y_validate.popularity_pred_lm, color='lime', alpha=.5, label="Model: LinearRegression")
    plt.title("Comparison of the models using all the features")
    plt.xlabel("Popularity")
    plt.ylabel("Number of Songs")
    plt.title("Comparing the Distribution of Actual Popularity to Distributions of Predicted Popularity")
    plt.legend()
    return plt.show()