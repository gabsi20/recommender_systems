from sklearn import cross_validation  
import numpy as np
import random
import matplotlib.pyplot as plt
import time

FOLDS = 10

def evaluate_cold_start(method, UAM, plot, color):
    RECOMMENDATIONS = 30

    users_sums = np.sum(UAM, axis=1)
    sorted_indizes = np.argsort(users_sums)[::-1]

    users_f_measures = []
    users_listenings = []

    for user_index in sorted_indizes:
        user = UAM[user_index]

        folds = cross_validation.KFold(len(user), n_folds=FOLDS)

        user_presicion = 0
        user_recall = 0

        for _train_artists, test_artists in folds:
            training_uam = UAM.copy()
            training_uam[user_index, test_artists] = 0.0

            result_indizes = method(training_uam, user_index, 10)[0:RECOMMENDATIONS]
            correct_indizes = np.intersect1d(user, result_indizes)

            true_positives = len(correct_indizes)

            precision = 100.0 if len(result_indizes) == 0 else 100.0 * true_positives / len(result_indizes)
            recall = 100.0 if len(test_artists) == 0 else 100.0 * true_positives / len(test_artists)

            user_presicion += precision / FOLDS
            user_recall += recall  / FOLDS

        user_f_measure = 2 * ((user_presicion * user_recall) / (user_presicion + user_recall)) if (user_presicion + user_recall) else 0.00
        user_listenings = users_sums[user_index]

        users_f_measures.append(user_f_measure)
        users_listenings.append(user_listenings)

        print ("\n\nListening Count for User: %.2f\nF-Measure for User %.2f" % (user_listenings, user_f_measure))

    plot.plot(users_listenings, users_f_measures, color) 

def evaluate(method, UAM, precion_recall_plot, f1_plot, color):
    MAX_RECOMMENDATIONS = int(UAM.shape[1] / FOLDS)
    MAX_USERS = 5

    sample_users = random.sample(range(0, UAM.shape[0]), MAX_USERS)

    precisions = []
    recalls = []
    f_measures = []
    counts = []

    for recommendations_count in range(1, MAX_RECOMMENDATIONS, 100):
        avg_precision = 0
        avg_recall = 0

        for user_index in sample_users:
            user = UAM[user_index]
            folds = cross_validation.KFold(len(user), n_folds=FOLDS)

            for _train_artists, test_artists in folds:
                training_uam = UAM.copy()
                training_uam[user_index, test_artists] = 0.0

                result_indizes = method(training_uam, user_index, 100)[0:recommendations_count]
                correct_indizes = np.intersect1d(user, result_indizes)

                true_positives = len(correct_indizes)

                precision = 100.0 if len(result_indizes) == 0 else 100.0 * true_positives / len(result_indizes)
                recall = 100.0 if len(test_artists) == 0 else 100.0 * true_positives / len(test_artists)

                avg_precision += precision / (FOLDS * MAX_USERS)
                avg_recall += recall  / (FOLDS * MAX_USERS)

        f_measure = 2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall)) if (avg_precision + avg_recall) else 0.00

        precisions.append(avg_precision) 
        recalls.append(avg_recall)
        f_measures.append(f_measure)
        counts.append(recommendations_count)

        print ("\n" + method.__name__)
        print ("\nCount: " + str(recommendations_count))
        print ("\nMean Average Precision: %.2f\nMean Average Recall %.2f" % (avg_precision, avg_recall))

    if (precion_recall_plot is not None):
        precion_recall_plot.plot(recalls, precisions, color)
        f1_plot.plot(counts, f_measures, color)
