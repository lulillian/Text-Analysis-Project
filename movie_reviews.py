from imdb import Cinemagoer
import random
import string
import sys
from unicodedata import category
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def choose_movie(x):
    """ Chooses a movie"""
    #create an instance of the Cinemagoer class
    ia = Cinemagoer()
    
    # search movie
    movie = ia.search_movie(x)[0]
    movieid = movie.movieID #'0468569'
    movie_reviews = ia.get_movie_reviews(movieid)  # all the words
    # print(movie_reviews) #prints data dict, leads to review dict, leads to a list of dicts of each review
    movie_reviews_content = movie_reviews["data"]["reviews"]
    return (movie_reviews_content)


movie_reviews_content=choose_movie('Scream 6')

def extract_content(movie_reviews_content):
    """Put all the content of the reviews into one string"""
    reviews = ""
    for review in movie_reviews_content:
        reviews += review["content"]
    reviews = reviews.replace("\n", " ").replace("\r", "").replace("  ", " ")
    return reviews

reviews=extract_content(movie_reviews_content)
# print(extract_content(movie_reviews_content))


def process_content(reviews):
    """Makes a histogram with """
    hist={}
    strippables = "".join(
        [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
    ) #variable that holds all the punctuation

    for line in reviews:
        line=line.replace('-',' ')
        line = line.replace(chr(8212), ' ')  # Unicode 8212 is the HTML decimal entity for em dash

    split_reviews=reviews.split(' ') # this will split words in reviews into a list
    
    for word in split_reviews:
        word=word.strip(strippables)
        word=word.lower()
        hist[word]=hist.get(word,0)+1
    
    return hist

hist=process_content(reviews)
# print(hist)


def rid_stopwords(hist):
    """Get rids of stop words and returns a dictionary without them."""
    stop_words=set(stopwords.words('english'))
    text = hist
    histogram = {word: freq for word, freq in text.items() if word.lower() not in stop_words}
    return (histogram)

histogram=rid_stopwords(hist)
# print(rid_stopwords(hist))



def most_common(histogram):
    """Returns the top 20 most common used words. """
    top=[]
    for word in histogram:
        freq=histogram[word]
        top.append((freq,word))
    top.sort(reverse=True)
    return top[:20]

top=most_common(histogram)
print(top)


# def main():
    





# movie_reviews_content=movie_reviews['data']['reviews'] #list of dictionaries of each review
# print(movie_reviews_content[1])


# def process_reviewsinto_list(movie_reviews):
#     """Takes all the reviews of the movie and returns a list"""
#     for review in movie_reviews["data"]["reviews"]:
#         # review_title=review['title']
#         # review_content=review['content']
#         reviews_list.append(review["content"])
#     return reviews_list


# movie_review_list = process_reviewsinto_list(movie_reviews)
# print(movie_review_list)


# def word_freq(movie_review_list):
#     """Takes a list of words
#     and returns a dict of
#     all the words and their frequencies."""

#     strippables = "".join(
#         [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]
#     )
#     freq = {}
#     for word in movie_review_list:


# stop_words=['The','and','of']


# def filter_out_stopwords(movie_reviews):
#     """Filter out stop words like the, end, of, etc for more accurate representation of what was said about
#     the film."""

#     words_without_stopwords=[]

#     for word in movie_review_list:
#         if word not in stop_words:
#             words_without_stopwords.append(word)
#     return words_without_stopwords

# print(filter_out_stopwords(movie_reviews))


# if __name__ == '__main__':
# main()
