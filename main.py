import numpy as np
import random
import file
from sets import Set
from sklearn import cross_validation
import scipy.spatial.distance as scidist
import matplotlib.pyplot as plt

UAM_FILE = "data/C1ku_UAM.txt"
ARTISTS_FILE = "data/C1ku_idx_artists.txt"
USERS_FILE = "data/C1ku_idx_users.txt"
ARTISTS_EXTENDED = "data/C1ku_artists_extended.csv"
AAM_FILE = "data/AAM.txt"
ARTISTS = file.read_from_file(ARTISTS_FILE)
USERS = file.read_from_file(USERS_FILE)
UAM = np.loadtxt(UAM_FILE, delimiter='\t', dtype=np.float32)
ARTISTS_DATA = file.read_from_file(ARTISTS_EXTENDED)
AAM = np.loadtxt(AAM_FILE, delimiter='\t', dtype=np.float32)

FOLDS = 10

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

def content_based_recommender(UAM, user, K):
  count_artists = min(len(np.nonzero(UAM[100,:])[0]),200)
  pc_vec = np.argsort(UAM[user,:])[(count_artists * (-1)):]
  sort_idx = np.argsort(AAM[pc_vec,:], axis=1)
  neighbor_idx = list(set(sort_idx[:,-1-K:-1].flatten()))
  for idx in pc_vec:
    if idx in neighbor_idx:
      neighbor_idx.pop(neighbor_idx.index(idx))
  return neighbor_idx

def evaluate(method, color="r"):
    MAX_RECOMMENDATIONS = 100
    MAX_USERS = 5

    sample_users = random.sample(range(0, UAM.shape[0]), MAX_USERS)

    precisions = []
    recalls = []
    f_measures = []

    for recommendations_count in range(1, MAX_RECOMMENDATIONS):

        avg_precision = 0
        avg_recall = 0

        for user_index in sample_users:
            user = UAM[user_index:]

            folds = cross_validation.KFold(len(user), n_folds=FOLDS)

            for _train_artists, test_artists in folds:
                training_uam = UAM.copy()
                training_uam[user_index, test_artists] = 0.0

                result_indizes = method(training_uam, user_index, 100)[0:recommendations_count]
                correct_indizes = np.intersect1d(user[test_artists], result_indizes)

                true_positives = len(correct_indizes)

                precision = 100.0 if len(result_indizes) == 0 else 100.0 * true_positives / len(result_indizes)
                recall = 100.0 if len(test_artists) == 0 else 100.0 * true_positives / len(test_artists)

                avg_precision += precision / (FOLDS * MAX_USERS)
                avg_recall += recall  / (FOLDS * MAX_USERS)

        f_measure = 2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall)) if (avg_precision + avg_recall) else 0.00

        precisions.append(avg_precision)
        recalls.append(avg_recall)
        f_measures.append(f_measure)

        print ("\n\nMean Average Precision: %.2f\nMean Average Recall %.2f" % (avg_precision, avg_recall))

    precion_recall_plot.plot(recalls, precisions, color)
    f1_plot.plot(range(1, MAX_RECOMMENDATIONS), f_measures, color)

plot1 = plt.figure()
plot2 = plt.figure()

precion_recall_plot = plot1.add_subplot(111)
f1_plot = plot2.add_subplot(111)

evaluate(random_artist_recommender, 'r')
evaluate(random_user_recommender, 'g')
evaluate(popularity_recommender, 'b')
evaluate(collaborative_filtering_recommender, 'y')
evaluate(content_based_recommender)


plot1.savefig('./results/pr_compared.png')
plot2.savefig('./results/f1_compared.png')

print "Done."
