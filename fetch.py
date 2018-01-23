import os
import csv
import file
import progress
import requests

# Parameters
API_BASE_URL = "https://api.spotify.com/v1/"
API_KEY = '' # set SPOTIFY API KEY 

ARTISTS_FILE = "./data/C1ku_artists_extended.csv" # text file containing Last.fm user names
OUTPUT_DIRECTORY = "./data/"       # directory to write output to

def __fetch_spotify_artists(artists):
    artists_data = {}
    
    print 'fetching artists'
    for index in range(0, len(artists)):
        artist_name = artists[index][1]
        progress.print_progressbar(index, len(artists), artist_name)
        try:
            headers = {"Authorization":"Bearer " + API_KEY}
            search_query = API_BASE_URL + 'search/?q=' + artist_name + '&type=artist'

            response = requests.get(search_query, headers=headers).json()
            
            artists_data[index] = {
                'id': artists[index][0],
                'name': artist_name,
                'spotify_id': response['artists']['items'][0]['id'],
                'genres': response['artists']['items'][0]['genres']
            }
            artists_data = __fetch_spotify_top_tracks(artists_data, index)
        except:
            artists_data[index] = {
                'id': artists[index][0],
                'name': artist_name,
                'spotify_id': None,
                'genres': [],
                'tracks': [],
                'average_audio_features': [0,0,0,0,0,0,0,0,0,0]
            }
        __write_csv_file(artists_data, index)

def __fetch_spotify_top_tracks(artists_data, artist_index):
    artists_data[artist_index]['tracks'] = []
    try:
        headers = {"Authorization":"Bearer " + API_KEY}
        search_query = API_BASE_URL + 'artists/' + artists_data[artist_index]['spotify_id'] + '/top-tracks?country=AT'
        response = requests.get(search_query, headers=headers).json()
        
        for index in range(0, len(response['tracks'])):
            artists_data[artist_index]['tracks'].append(response['tracks'][index]['id'])
        artists_data = __fetch_average_audio_features(artists_data, artist_index)
    except:
        artists_data[artist_index]['tracks'] = []
        artists_data[artist_index]['average_audio_features'] = [0,0,0,0,0,0,0,0,0,0]
    
    return artists_data

def __compute_average(response, artists_data, artist):
    artist_average_audio_features = [0,0,0,0,0,0,0,0,0,0]
    song_count = len(response["audio_features"])    

    for index in range(0, song_count):
        artist_average_audio_features[0] += (response["audio_features"][index]["danceability"] / float(song_count))
        artist_average_audio_features[1] += (response["audio_features"][index]["energy"] / float(song_count))
        artist_average_audio_features[2] += (response["audio_features"][index]["key"] / float(song_count))
        artist_average_audio_features[3] += (response["audio_features"][index]["loudness"] / float(song_count))
        artist_average_audio_features[4] += (response["audio_features"][index]["mode"] / float(song_count))
        artist_average_audio_features[5] += (response["audio_features"][index]["speechiness"] / float(song_count))
        artist_average_audio_features[5] += (response["audio_features"][index]["acousticness"] / float(song_count))
        artist_average_audio_features[6] += (response["audio_features"][index]["instrumentalness"] / float(song_count))
        artist_average_audio_features[7] += (response["audio_features"][index]["liveness"] / float(song_count))
        artist_average_audio_features[8] += (response["audio_features"][index]["valence"] / float(song_count))
        artist_average_audio_features[9] += (response["audio_features"][index]["tempo"] / float(song_count))
    artists_data[artist]['average_audio_features'] = artist_average_audio_features
    return artists_data
    

def __fetch_average_audio_features(artists_data, artist):
    try:
        headers = {"Authorization":"Bearer " + API_KEY}
        search_query = API_BASE_URL + 'audio-features/?ids=' + ','.join(artists_data[artist]['tracks'])
        response = requests.get(search_query, headers=headers).json()

        artists_data = __compute_average(response, artists_data, artist)
    except:
        artists_data[artist]['average_audio_features'] = [0,0,0,0,0,0,0,0,0,0]

    return artists_data

def __write_csv_file(artists_data, index):
    with open(OUTPUT_DIRECTORY + 'spotify_data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        try:
            writer.writerow([artists_data[index]['id'], artists_data[index]['name']] + artists_data[index]['average_audio_features'] + artists_data[index]['genres'])
        except:
            writer.writerow([artists_data[index]['id']] + [0,0,0,0,0,0,0,0,0,0])

def get_artists_context(refetch):
    print "fetch data"
    artists = file.read_from_file(ARTISTS_FILE)
    __fetch_spotify_artists(artists)
    print 'finished'

if __name__ == "__main__":
    get_artists_context(refetch=True)
