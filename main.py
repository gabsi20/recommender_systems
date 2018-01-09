import numpy as np
import random
import file
from sets import Set

UAM_FILE = "data/C1ku_UAM.txt"                    
ARTISTS_FILE = "data/C1ku_idx_artists.txt"       
USERS_FILE = "data/C1ku_idx_users.txt"   
ARTISTS_EXTENDED = "data/C1ku_artists_extended.csv"  
ARTISTS = file.read_from_file(ARTISTS_FILE)
USERS = file.read_from_file(USERS_FILE)
UAM = np.loadtxt(UAM_FILE, delimiter='\t', dtype=np.float32)
ARTISTS_DATA = file.read_from_file(ARTISTS_EXTENDED)

MAX_RECOMMENDATIONS = 10

def random_artist_recommender(user):
    user_playcounts = UAM[user, :]
    recommendation_pool = np.nonzero(user_playcounts == 0)[0]
    return random.sample(recommendation_pool, MAX_RECOMMENDATIONS)

def random_user_recommender(user):
    random_users = random.sample(range(0, UAM.shape[0]), 10)
    users_playcounts = UAM[random_users, :]

    artist_pool = get_nonzero_artists_from_users(users_playcounts)
    my_user_counts = UAM[user, :]

    recommendation_pool = np.where(my_user_counts[artist_pool] == 0)[0]
    return random.sample(recommendation_pool, 10)

def popularity_recommender():
    sums = np.sum(UAM, axis=0)
    top_ranked_indizes = np.argsort(sums)[-MAX_RECOMMENDATIONS:]
    return top_ranked_indizes


def get_nonzero_artists_from_users(users_playcounts):
    artist_pool = []
    for user_playcount in users_playcounts:
        artist_pool.extend(np.nonzero(user_playcount)[0])
    return np.unique(artist_pool)


print random_user_recommender(100)
print random_artist_recommender(100)
print popularity_recommender()