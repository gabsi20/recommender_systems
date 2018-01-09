#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import csv
import file

# Parameters
WIKIPEDIA_URL = "http://en.wikipedia.org/wiki/"

ARTISTS_FILE = "./data/LFM1b_artists.txt"          # text file containing Last.fm user names
OUTPUT_DIRECTORY = "./data/wikipedia_pages"     # directory to write output to

def __print_progress_bar(iteration, total, current_item):
    fill = '█'
    decimals = 1
    length = 30
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print '\r|%s| %s%% %s %s\r' % (bar, percent, current_item, str(iteration))
    if iteration == total: 
        print()

def __fetch_wikipedia_page(artist):
    artist_quoted = urllib.quote(artist)
    url = WIKIPEDIA_URL + artist_quoted

    try:
        content = urllib.urlopen(url).read()
        return content
    except IOError:
        print "error on " + artist
        return ""

def __write_htmlfile(i, html_content):
    html_filename = OUTPUT_DIRECTORY + "/" + str(i) + ".html"

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    try:
        with open(html_filename, 'w') as f:
            f.write(html_content)
    except Exception as error:
        print "error on " + html_filename
        print error

def get_artists_context(refetch):
    if not os.path.exists(OUTPUT_DIRECTORY) or refetch:
        print "fetch data"
        artists = file.read_from_file(ARTISTS_FILE)

        for i in range(0, len(artists)):
            html_content = __fetch_wikipedia_page(artists[i][1])
            __write_htmlfile(i, html_content)
            __print_progress_bar(i, len(artists), artists[i][1])
            
    else:
        print "data already exists"
