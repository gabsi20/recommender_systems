import os
import urllib
import csv
import file
import progress

# Parameters
FETCH_TARGET_URL = "https://www.last.fm/music/"

ARTISTS_FILE = "./data/LFM1b_artists.txt"          # text file containing Last.fm user names
OUTPUT_DIRECTORY = "./data/last_fm"     # directory to write output to

def __fetch_page(artist):
    artist_quoted = urllib.quote(artist)
    url = FETCH_TARGET_URL + artist_quoted

    try:
        content = urllib.urlopen(url).read()
        return content
    except IOError:
        print "error on " + artist
        return ""

def __write_htmlfile(index, html_content):
    html_filename = OUTPUT_DIRECTORY + "/" + str(index) + ".html"

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    try:
        with open(html_filename, 'w') as html_file:
            html_file.write(html_content)
    except Exception as error:
        print "error on " + html_filename
        print error

def get_artists_context(refetch):
    print "fetch data"
    artists = file.read_from_file(ARTISTS_FILE)

    for index in range(0, len(artists)):
        if not os.path.exists(OUTPUT_DIRECTORY + "/" + str(index) + ".html") or refetch:
            html_content = __fetch_page(artists[index][1])
            __write_htmlfile(index, html_content)
            progress.print_progressbar(index, len(artists), artists[index][1])
            
if __name__ == "__main__":
    get_artists_context(refetch=False)