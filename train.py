import os
import numpy as np
import scipy.spatial.distance as scidist
import urllib
import file
import fetch
import progress

DATA_DIRECTORY = "./data/"
OUTPUT_TFIDF_FILE = "tfidfs.txt"  # file to store term weights
OUTPUT_TERMS_FILE = "terms.txt"   # file to store list of terms (for easy interpretation of term weights)
OUTPUT_SIMS_FILE = "AAM.txt"      # file to store similarities between items

STOP_WORDS = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

def __remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out

def __get_tokenized_html_content():
    html_contents = {}
    artists = file.read_from_file(fetch.ARTISTS_FILE)
    
    for i in range(0, len(artists)):
        html_filename = fetch.OUTPUT_DIRECTORY + "/" + str(i) + ".html"

        if os.path.exists(html_filename):
            html_content = open(html_filename, 'r').read()
            content_tags_removed = __remove_html_markup(html_content)
            content_casefolded = content_tags_removed.lower()
            tokens = content_casefolded.split()
            tokens_filtered = filter(lambda t: t.isalnum(), tokens)
            tokens_filtered_stopped = filter(lambda t: t not in STOP_WORDS, tokens_filtered)
            html_contents[i] = tokens_filtered_stopped
            progress.print_progressbar(i, len(artists), html_filename + ' ' + str(len(tokens_filtered_stopped)) + ' tokens')
        # else:
        #     print "Target file " + html_filename + " does not exist!"
    
    return html_contents

def __compute_term_frequency(html_contents):
    terms_document_frequency = {}
    print "Computing Term Frequencies"

    for aid, terms in html_contents.items():
        for term in set(terms):
            if term not in terms_document_frequency:
                terms_document_frequency[term] = 1
            else:
                terms_document_frequency[term] += 1
    return terms_document_frequency

def __compute_similarities(artists_count, term_frequency_inverse_document_frequency):
    similarities = np.zeros(shape=(artists_count, artists_count), dtype=np.float32)
    print "Computing pairwise similarities between artists"

    for i in range(0, artists_count):
        progress.print_progressbar(i, artists_count, i)
        for j in range(i, artists_count):
            cosine_matrix = 1.0 - scidist.cosine(term_frequency_inverse_document_frequency[i], term_frequency_inverse_document_frequency[j])

            # If either TF-IDF vector (of i or j) only contains zeros, cosine similarity is not defined (NaN: not a number).
            # In this case, similarity between i and j is set to zero (or left at zero, in our case).
            if not np.isnan(cosine_matrix):
                similarities[i, j] = cosine_matrix
                similarities[j, i] = cosine_matrix
    return similarities

def __compute_document_frequency_vector(terms_count, artists_count, terms_document_frequency, term_list):
    inverse_document_frequency = np.zeros(terms_count, dtype=np.float32)
    print "Computing document frequency vector"

    for i in range(0, terms_count):
        inverse_document_frequency[i] = np.log(artists_count / terms_document_frequency[term_list[i]])
    return inverse_document_frequency

def __compute_term_frequency_inverse_document_frequency(artists_count, terms_count, html_contents, term_list, inverse_document_frequency):
    term_frequency_inverse_document_frequency = np.zeros(shape=(artists_count, terms_count), dtype=np.float32)
    print "Computing term weights"

    terms_index_lookup = {}
    for a_idx, terms in html_contents.items():
        progress.print_progressbar(a_idx, len(html_contents), a_idx)
        for t in terms:
            if t in terms_index_lookup:
                t_idx = terms_index_lookup[t]
            else:
                t_idx = term_list.index(t)
                terms_index_lookup[t] = t_idx
            term_frequency_inverse_document_frequency[a_idx, t_idx] += 1

    term_frequency_inverse_document_frequency = np.log1p(term_frequency_inverse_document_frequency) * np.tile(inverse_document_frequency, artists_count).reshape(artists_count, terms_count)
    return term_frequency_inverse_document_frequency

def __dictionary_to_list(dictionary):
    list = []
    for t in dictionary.keys():
        list.append(t)
    return list

def __write_terms_file(term_list):
    print "Saving term list to " + OUTPUT_TERMS_FILE
    with open(DATA_DIRECTORY + O./UTPUT_TERMS_FILE, 'w') as f:
        for t in term_list:
          f.write(t + "\n")
ef __write_tfidf_file(tfidf):   print "Saving TF-IDF matrix to " + OUTPUT_TFIDF_FILE
    np.savetxt(DATA_DIRECTORY + O./UTPUT_TFIDF_FILE, tfidf, fmt='%0.6f', delimiter='\t', newline='\n')

f __write_sims_file(similarities):
  print "Saving cosine similarities to " + OUTPUT_SIMS_FILE   np.savetxt(DATA_DIRECTORY + O./UTPUT_SIMS_FILE, similarities, fmt='%0.6f', delimiter='\t', newline='\n')

f train_content_based_recommender():
  html_contents = __get_tokenized_html_content()   terms_document_frequency = __compute_term_frequency(html_contents)
    term_list = __dictionary_to_list(terms_document_frequency)
    artists_count = len(html_contents.items())
    terms_count = len(terms_document_frequency)

    inverse_document_frequency = __compute_document_frequency_vector(terms_count, artists_count, terms_document_frequency, term_list)
    tfidf = __compute_term_frequency_inverse_document_frequency(artists_count, terms_count, html_contents, term_list, inverse_document_frequency)
    similarities = __compute_similarities(artists_count, tfidf)

    __write_tfidf_file(tfidf)
    __write_terms_file(term_list)
    __write_sims_file(similarities)

train_content_based_recommender()