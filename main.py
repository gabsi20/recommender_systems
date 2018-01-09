import numpy as np
import random
import file
import fetch
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
    random_users = random.sample(range(0, UAM.shape[0]), MAX_RECOMMENDATIONS)
    users_playcounts = UAM[random_users, :]

    artist_pool = get_nonzero_artists_from_users(users_playcounts)
    my_user_counts = UAM[user, :]

    recommendation_pool = np.where(my_user_counts[artist_pool] == 0)[0]
    return random.sample(recommendation_pool, MAX_RECOMMENDATIONS)

def popularity_recommender():
    sums = np.sum(UAM, axis=0)
    top_ranked_indizes = np.argsort(sums)[-MAX_RECOMMENDATIONS:]
    return top_ranked_indizes


def get_nonzero_artists_from_users(users_playcounts):
    artist_pool = []
    for user_playcount in users_playcounts:
        artist_pool.extend(np.nonzero(user_playcount)[0])
    return np.unique(artist_pool)


def collaborative_filtering_recommender(user, K):
    pc_vec = UAM[user,:]
    sim_users = np.inner(pc_vec, UAM)     # similarities between u and other users
    sort_idx = np.argsort(sim_users)        # sort in ascending order
    neighbor_idx = sort_idx[-2:-1][0]       # index of the closest neighbour ... last is user himself
    artist_idx_u = np.nonzero(UAM[user,:])                 # indices of artists user u listened to
    artist_idx_n = np.nonzero(UAM[neighbor_idx,:])      # indices of artists user u's neighbor listened to
    recommended_artists_idx = np.setdiff1d(artist_idx_n[0], artist_idx_u[0])      # get difference indices between user listened and neighbour listened
    return random.sample(recommended_artists_idx, MAX_RECOMMENDATIONS)

def content_based_recommender():
    fetch.get_artists_context(refetch=True)
    return 'content based recommender not implemented'


print random_user_recommender(100)
print random_artist_recommender(100)
print popularity_recommender()
print collaborative_filtering_recommender(100, 3)
print content_based_recommender()


