import numpy as np
import random
import file

UAM_FILE = "data/C1ku_UAM.txt"                    
ARTISTS_FILE = "data/C1ku_idx_artists.txt"       
USERS_FILE = "data/C1ku_idx_users.txt"   
ARTISTS_EXTENDED = "data/C1ku_artists_extended.csv"  
ARTISTS = file.read_from_file(ARTISTS_FILE)
USERS = file.read_from_file(USERS_FILE)
UAM = np.loadtxt(UAM_FILE, delimiter='\t', dtype=np.float32)
ARTISTS_DATA = file.read_from_file(ARTISTS_EXTENDED)

def random_artist_recommender(user):
    recommendation_pool = []
    user_playcounts =  UAM[user,:]
    for idx, count in enumerate(user_playcounts):
        if count == 0:
            recommendation_pool.append(ARTISTS_DATA[idx][1])
    return random.sample(recommendation_pool, 10)

def random_user_recommender(user):
    artist_pool = []
    random_users = random.sample(USERS,10)
    for idx, user_id in enumerate(random_users):
        user_playcounts =  UAM[int(USERS.index(user_id)),:]
        for idx, count in enumerate(user_playcounts):
            if count > 0:
                artist_pool.append(idx)
    recommendation_pool = []
    user_playcounts =  UAM[user,:]
    for idx, artist in enumerate(artist_pool):
        if user_playcounts[artist] == 0:
            recommendation_pool.append(ARTISTS_DATA[artist][1])
    return random.sample(recommendation_pool,10)

print random_user_recommender(100)
print random_artist_recommender(100)