from imdb import Cinemagoer
import random
import string
import sys
from unicodedata import category
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re


# import matplotlib.pyplot as plt
# from wordcloud import WordCloud

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


def choose_movie(x):
    """ Chooses a movie and return the reviews """
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
#print(movie_reviews_content)

def number_score(movie_reviews_content):
    """Returns a list of all the ratings from the reviews"""
    ratings_list=[]
    for reviews in movie_reviews_content:
        ratings_list.append(reviews['rating'])

    return ratings_list

ratings_list=number_score(movie_reviews_content)
# print(ratings_list)

def calculate_average_rating(ratings_list):
    """ Take the list of ratings and calculates the average rating."""
    total_reviews=len(ratings_list)
    sum=0
    for i in ratings_list:
        if(type(i) == int):
            sum+=i
    average=sum/total_reviews
    return average

average=calculate_average_rating(ratings_list)
# print(average)



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
    stop_words=set(stopwords.words('english')) #learned in chatgpt
    text = hist
    histogram = {}
    for word, freq in hist.items():
        word=re.sub(r'\d+','',word) #learned from chatgpt
        if word.lower() not in stop_words:
            histogram[word]=freq
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
    top_20= top[:20]
    return top_20

top_20=most_common(histogram)
# print(top_20)

def most_commonlist(top_20):
    """Print the list of top 20 words."""
    common=[]
    for tuples in top_20:
        common.append(tuples[1])
    return common

common=most_commonlist(top_20)
# print(common)

def sentiment(reviews):
    """Returns a numerical score form 0-1 on 
    how negative, neutral, positive and compound the reviews are. """
    score = SentimentIntensityAnalyzer().polarity_scores(reviews) #learned from chatgpt
    return score

score=sentiment(reviews)

def overall_sentiment(score):
    """Prints how negative or
      positive a film was perceived from the sentiment analysis score."""
    if score['compound']==1:
        print(" very postive")
    if score['compound']<0:
        print("very negative")
    if 0< score['compound']<=0.5:
        print("neutral")
    if 0.5<score['compound']<1:
        print("positive")

# overall_thoughts=overall_sentiment(score)

        


def main():
    reviews=extract_content(movie_reviews_content)
    hist=process_content(reviews)
    histogram=rid_stopwords(hist)

    print('The top 20 common words are:')
    common=most_commonlist(top_20)
    print(common)

    print('On average, out of 10 stars, people rated it:')
    ratings_list=number_score(movie_reviews_content)
    average=calculate_average_rating(ratings_list)
    print(average)

    print('Based on a sentiment analysis, the score was:')
    score=sentiment(reviews)
    print(score)

    print('Thus,most of the reviews were: ')
    overall_thoughts=overall_sentiment(score)
    # print(overall_thoughts)
   

if __name__=='__main__':
    main()