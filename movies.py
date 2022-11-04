"""
Make a program that examines imdb reviews of a movie that was considered to "flop" and accomplishes two goals:
    1) Display the most used (influential) words in these reviews.
        a) The purpose of this is to gauge why the movie was not successfull.
    2) Use natural language to gauge the sentiment of each review.
Each entry will be stored in a dictionary depending on how high the sentiment score for that emotion was.
"""
from imdb import Cinemagoer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def movie_id(movie):
    """
    Returns IMDB movie code.  Movie inpit must be string.
    """
    ia = Cinemagoer()
    # if type(movie) != str:
    #     raise Exception('Sorry, Movie must be a string.  Try using ""')
    # else:
    name = ia.search_movie(movie)[0]
    id = name.movieID
    return id
# print(movie_id('The Matrix Resurrections'))
matrixid = 10838180
def sent_movie_reviews():
    ia = Cinemagoer()
    data = ia.get_movie_reviews(10838180)
    rev_list = data['data']['reviews'] #rev_list is a list of dictionaries
    # print(len(rev_list))
    sent_rev = []
    review = []
    for i in range(len(rev_list)):
        dictionary = rev_list[i-1]
        review.append(dictionary['content'])
        # for review in dictionary:
        # print(review)
        for sentence in review:
            sent_rev.append(sent_tokenize(sentence)) 
            # print(sentence)
    return sent_rev # List of lists of sentences
# print(sent_movie_reviews())
def word_movie_reviews():
    data = sent_movie_reviews()
    result = []
    for lst in data:
        for sentence in lst:
            result.append(word_tokenize(sentence))
    return result
def remove_fluff():
    filtered_rev = []
    fluff = tuple(stopwords.words("english"))
    review = word_movie_reviews()
    for word in review:
        if word not in fluff:
            filtered_rev.append(word)
    return filtered_rev
# print(remove_fluff())
def make_hist():
    hist = {}
    data = remove_fluff()
    # print(type(data))
    for review in data:
        for word in review:
            word = word.lower()
            if word not in hist:
                hist[word] = 1
            else:
                hist[word] += 1 
    return hist
# print(make_hist())
def order_hist():
    hist = make_hist()
    inverse = {}
    for key , value in hist.items():
            inverse[value] = key
    most_common = sorted(list(inverse.items()), reverse = True)
    return most_common

def sentiment(): # I made this function into regular code in order to speed things up (running this takes a lot of time)
    """
    Get sentiment score of each sentence in a review
    """
    scores = []
    reviews = sent_movie_reviews()
    for review in reviews: # reviews is a list of reviews
        for sentence in review: #Each review is a list of sentences
            # print(sentence)
            score = SentimentIntensityAnalyzer().polarity_scores(sentence)
            scores.append(score) # List of dictionaries
    return scores

def average(lst):
    return sum(lst)/len(lst)
def average_score(scores):
    pos_score = []
    neg_score = []
    neu_score = []
    com_score = []
    for dictionary in range(len(scores)):
        pos_score.append(scores[dictionary]['pos'])
        neg_score.append(scores[dictionary]['neg'])
        neu_score.append(scores[dictionary]['neu'])
        com_score.append(scores[dictionary]['compound'])
    total_scores = sum(pos_score) + sum(neg_score) + sum(neu_score) + sum(com_score)
    perc_pos = sum(pos_score)/total_scores # This calculates what the % of an "overall review" would have been for each cat
    perc_neg = sum(neg_score)/total_scores
    perc_neu = sum(neu_score)/total_scores
    perc_com = sum(com_score)/total_scores
    absolute_avg = {'pos': perc_pos, 'neg': perc_neg, 'neu': perc_neu, 'compound': perc_com}
    categorical_avg = {'pos': average(pos_score), 'neg': average(neg_score), 'neu': average(neu_score), 'compound': average(com_score)}
    return absolute_avg

"""
I want to take every sentence's score (dictionary) and 
make a list out of it (hence making a summary of sent scores for a review)
I would then calc an average of the values of each key in each dict in the list
This average would be the score of the review
"""
def main():
    # print(average_score(sentiment()))
    # print(order_hist())
    print(len(word_movie_reviews()))
    print(len(stopwords.words("english")))
    print(len(remove_fluff()))
if __name__ == "__main__":
    main()