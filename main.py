import numpy as np
import random
import file
import train
from sets import Set
import scipy.spatial.distance as scidist 
import matplotlib.pyplot as plt
import evaluation
import threading
import sys

UAM_FILE = "data/C1ku_UAM.txt"
ARTISTS_FILE = "data/C1ku_idx_artists.txt"
USERS_FILE = "data/C1ku_idx_users.txt"
ARTISTS_EXTENDED = "data/C1ku_artists_extended.csv"
AAM_FILE = "data/AAM.txt"
ARTISTS = file.read_from_file(ARTISTS_FILE)
USERS = file.read_from_file(USERS_FILE)
UAM = np.loadtxt(UAM_FILE, delimiter='\t', dtype=np.float32)
ARTISTS_DATA = file.read_from_file(ARTISTS_EXTENDED)
# AAM = file.read_from_file(AAM_FILE)

def random_artist_recommender(UAM, user, _K):
    user_playcounts = UAM[user, :]
    recommendation_pool = np.where(user_playcounts == 0)[0]
    return random.sample(recommendation_pool, len(recommendation_pool))

def random_user_recommender(UAM, user, K):
    random_users = random.sample(range(0, UAM.shape[0]), K)
    users_playcounts = UAM[random_users, :]

    artist_pool = get_nonzero_artists_from_users(users_playcounts)
    my_user_counts = UAM[user, :]

    recommendation_pool = np.where(my_user_counts[artist_pool] == 0)[0]
    return random.sample(recommendation_pool, len(recommendation_pool))

def popularity_recommender(UAM, _user, _K):
    sums = np.sum(UAM, axis=1)
    top_ranked_indizes = np.argsort(sums)
    return top_ranked_indizes[::-1]

def get_nonzero_artists_from_users(users_playcounts):
    artist_pool = []
    for user_playcount in users_playcounts:
        artist_pool.extend(np.nonzero(user_playcount)[0])
    return np.unique(artist_pool)

def collaborative_filtering_recommender(UAM, user, K):
    pc_vec = UAM[user, :]
    sim_users = np.zeros(shape=(UAM.shape[0]), dtype=np.float32)
    for user_index in range(0, UAM.shape[0]):
        sim_users[user_index] = 1.0 - scidist.cosine(pc_vec, UAM[user_index,:])   
    sort_idx = np.argsort(sim_users)
    neighbours_idx = sort_idx[-1-K:-1]
    counter = {}
    for idx, neighbour in enumerate(neighbours_idx):
        artist_idx_u = np.nonzero(UAM[user, :])
        artist_idx_n = np.nonzero(UAM[neighbour, :])
        recommended_artists_idx = np.setdiff1d(artist_idx_n[0], artist_idx_u[0])
        for artist_idx in recommended_artists_idx:
            if artist_idx in counter:
                counter[artist_idx] += UAM[neighbour, artist_idx] * (len(neighbours_idx) - idx)
            else:
                counter[artist_idx] = UAM[neighbour, artist_idx] * (len(neighbours_idx) - idx)
    return sorted(counter, key=counter.get, reverse=True)

def hybrid_cf_po_recommender(UAM, user, K):
    collaborative_filtering_recommender


def start_evaluation_with_multithreading():
    plot_1 = plt.figure()
    plot_2 = plt.figure()

    precion_recall_plot = plot_1.add_subplot(111)
    f1_plot = plot_2.add_subplot(111)

    threads = [threading.Thread(target=evaluation.evaluate, args=(random_artist_recommender, UAM, precion_recall_plot, f1_plot, 'r')),
        threading.Thread(target=evaluation.evaluate, args=(random_user_recommender, UAM, precion_recall_plot, f1_plot, 'g')),
        threading.Thread(target=evaluation.evaluate, args=(popularity_recommender, UAM, precion_recall_plot, f1_plot, 'b')),
        threading.Thread(target=evaluation.evaluate, args=(collaborative_filtering_recommender, UAM, precion_recall_plot, f1_plot, 'y'))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    plot_1.savefig('./results/pr_compared.png')
    plot_2.savefig('./results/f1_compared.png')


def start_cold_start_evaluation_with_multithreading():
    plot_3 = plt.figure()
    cs_plot = plot_3.add_subplot(111)

    threads = [threading.Thread(target=evaluation.evaluate_cold_start, args=(random_artist_recommender, UAM, cs_plot, 'r')),
        threading.Thread(target=evaluation.evaluate_cold_start, args=(random_user_recommender, UAM, cs_plot, 'g')),
        threading.Thread(target=evaluation.evaluate_cold_start, args=(popularity_recommender, UAM, cs_plot, 'b')),
        threading.Thread(target=evaluation.evaluate_cold_start, args=(collaborative_filtering_recommender, UAM, cs_plot, 'y'))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    plot_3.savefig('./results/f1_listenings.png')

def content_based_recommender(user, K):
    return random_user_recommender(100)

if len(sys.argv) < 2: print "no arguments set"
elif sys.argv[1] == "cb": evaluation.evaluate(content_based_recommender, UAM, None, None, 'y'),
elif sys.argv[1] == "cf": evaluation.evaluate(collaborative_filtering_recommender, UAM, None, None, 'y'),
elif sys.argv[1] == "po": evaluation.evaluate(popularity_recommender, UAM, None, None, 'b'),
elif sys.argv[1] == "ru": evaluation.evaluate(random_user_recommender, UAM, None, None, 'g'),
elif sys.argv[1] == "ra": evaluation.evaluate(random_artist_recommender, UAM, None, None, 'r'),
elif sys.argv[1] == "ev": start_evaluation_with_multithreading(),
elif sys.argv[1] == "cs": start_cold_start_evaluation_with_multithreading()
print "Done."