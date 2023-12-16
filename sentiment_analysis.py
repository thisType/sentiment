#  Student Name:Rashin Mir Sajjadi
#  Student Number:251348998
#  UWO UserName:smirsajj
#  date: 14/11/2023

# This file contains functional definitions used for sentimental analysis

# This function reads TSV file and returns a dictionary with a key for each keyword in the file and a corresponding
# value
def read_keywords(keyword_file_name):
    # keywords dictionary
    keywords_dictionary = {}
    try:
        # open file for reading
        file = open(keyword_file_name, "r")
        # read file by line
        line = file.readline()

        # loop through all the lines
        # check for the end of the lines
        while len(line) != 0:
            # split tab separated values
            line_values = line.split("\t")
            # keyword from the line values
            keyword = line_values[0]
            # keyword score string from the line values
            keyword_score_string = line_values[1]

            # int value of keyword score
            keyword_score = int(keyword_score_string)

            # add keyword and score to keywords dictionary
            keywords_dictionary[keyword] = keyword_score

            # read the next line
            line = file.readline()
        # close the file
        file.close()

    except IOError:
        # this block execute if IOError occurs
        print("Could not open file %s " % keyword_file_name)
        # return an empty keywords_dictionary
        return {}
    # return keywords_dictionary
    return keywords_dictionary


# function cleans tweet text
def clean_tweet_text(tweet_text):
    # a list that hold english letters or space character
    char_list = []

    # iterates of the tweet text
    for char in tweet_text:
        # convert character to a string
        char_string = str(char)

        # test if letter is an english character or a space character
        if char_string.isalpha() or char_string.isspace():
            # append the character if true
            char_list.append(char)

    # join the english letter list to a string
    string = "".join(char_list)
    # return a lower case cleaned  tweet text
    return string.lower()


# function that checks if a string value is equal to null and returns a string
def check_for_null_string(string):
    if string == "NULL":
        # return NULL string value
        return "NULL"
    else:
        # return the string
        return string


# function that checks if a string value is equal to NULL and returns a float value of a string
def check_for_null_float(string):
    if "NULL" in string:
        return "NULL"
    else:
        # return a float value of the string
        return float(string)


# this function reads CSV tweet file
def read_tweets(tweet_file_name):
    # list of dictionary tweets
    list_of_tweets = []

    # open and read csv file
    try:

        file = open(tweet_file_name, "r")
        # Read the file line by line
        line = file.readline()

        while len(line) != 0:
            #  split comma separated values
            tweet_values = line.split(",")

            # create tweet dictionary
            tweet_dictionary = {"date": tweet_values[0], "text": clean_tweet_text(tweet_values[1]),
                                "user": tweet_values[2],
                                "retweet": int(tweet_values[3]), "favorite": int(tweet_values[4]),
                                "lang": tweet_values[5], "country": check_for_null_string(tweet_values[6]),
                                "state": check_for_null_string(tweet_values[7]),
                                "city": check_for_null_string(tweet_values[8]),
                                "lat": check_for_null_float(tweet_values[9]),
                                "lon": check_for_null_float(tweet_values[10])}

            # append the tweet dictionary to tweet_list
            list_of_tweets.append(tweet_dictionary)

            # read the line
            line = file.readline()

        file.close()  # close the file

    except IOError:
        # executes if IOError occurs
        print("Could not open %s" % tweet_file_name)
        # return an empty list
        return []

    # return a list of tweet dictionaries
    return list_of_tweets


# This function calculates sentiment score for a tweet
def calc_sentiment(tweet_text, keyword_dict):
    # total sentiment score for keywords in keyword_dict
    total_sentiment_score = 0

    # iterate over keyword_dict
    for keyword, keyword_score in keyword_dict.items():
        # get a word list from the tweet text
        word_list = tweet_text.split(" ")
        # get the number of count a keyword is in the word list
        keyword_count = word_list.count(keyword)

        # get the score of keyword
        keyword_score = keyword_count * keyword_score

        # sum the sentiment total score
        total_sentiment_score += keyword_score

    return total_sentiment_score


# This function classifies sentiment score
def classify(score):
    #  classify the sentiment score
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


# This function computes average by receiving total score and count
def average_compute(total, count):
    # validates count
    if count == 0:
        return "NULL"
    else:
        # average
        average = total / count
        # return average rounded to 2 decimal place
        return round(average, 2)


# function that computes average sentiment of tweets  of a country
def country_average(country, tweet_list, keyword_dict):
    # sum of sentiment tweets score of a country
    sum_sentiment = 0
    # number of tweets from a country
    tweet_count = 0

    # loop over tweet list
    for tweet in tweet_list:
        # check for a country's name
        if tweet["country"] == country:
            sum_sentiment += calc_sentiment(tweet["text"], keyword_dict)
            tweet_count += 1

    # average sentiment score  of a country  sentiment
    avg = sum_sentiment / tweet_count
    return avg


# This functions sorts a country dictionary list and returns a string of representation of top 5 countries
def top_five_countries(countries_dictionary):
    # Sort the dictionary by value in descending order
    sorted_country_list = sorted(countries_dictionary.items(), key=lambda item: item[1], reverse=True)

    # records number of countries
    country_num = 1

    # country list
    five_country_list = []

    for data in sorted_country_list:
        # get country name
        country_name = data[0]
        five_country_list.append(country_name)
        if country_num == 5:
            break
        country_num += 1

    return ', '.join(five_country_list)


# This function performs analyses on tweet list and returns a dictionary of report data
def make_report(tweet_list, keyword_dict):
    # records data for analyses
    tweets_count = 0
    favorited_tweets_count = 0
    negative_tweets_count = 0
    neutral_tweets_count = 0
    positive_tweets_count = 0
    retweeted_tweets_count = 0
    # sum of  sentiment score of tweets
    total_favorited_sentiment_score = 0
    total_tweets_sentiment_score = 0
    total_retweet_sentiment_score = 0

    # a dictionary of each country average sentiment of tweets
    countries_average = {}

    for tweet in tweet_list:
        # count number of list
        tweets_count += 1
        # sum total sentiment score for all tweets
        total_tweets_sentiment_score += calc_sentiment(tweet["text"], keyword_dict)

        #  checks if a tweet has been favorited at least once
        if tweet["favorite"] >= 1:
            favorited_tweets_count += 1
            total_favorited_sentiment_score += calc_sentiment(tweet["text"], keyword_dict)

        # checks if a tweet is classified as negative
        if classify(calc_sentiment(tweet["text"], keyword_dict)) == "negative":
            negative_tweets_count += 1

        # checks if a tweet is classified as neutral
        if classify(calc_sentiment(tweet["text"], keyword_dict)) == "neutral":
            neutral_tweets_count += 1

        # checks if a  tweet is classified as positive
        if classify(calc_sentiment(tweet["text"], keyword_dict)) == "positive":
            positive_tweets_count += 1

        # checks for tweet retweeted at least once
        if tweet["retweet"] >= 1:
            retweeted_tweets_count += 1
            total_retweet_sentiment_score += calc_sentiment(tweet["text"], keyword_dict)

        # checks if country is nequl to NULL and if already exist in countries dictionary
        if tweet["country"] != 'NULL' and tweet["country"] not in countries_average:
            # stores total sentiment score for each country
            countries_average[tweet["country"]] = country_average(tweet["country"], tweet_list, keyword_dict)

    # report data
    dictionary_analyses = {"avg_favorite": average_compute(total_favorited_sentiment_score, favorited_tweets_count),
                           "avg_retweet": average_compute(total_retweet_sentiment_score, retweeted_tweets_count),
                           "avg_sentiment": average_compute(total_tweets_sentiment_score, tweets_count),
                           "num_favorite": favorited_tweets_count,
                           "num_negative": negative_tweets_count, "num_neutral": neutral_tweets_count, "num_positive": positive_tweets_count,
                           "num_tweets": tweets_count, "num_retweet": retweeted_tweets_count,
                           "top_five": top_five_countries(countries_average)}

    # return data dictionary
    return dictionary_analyses


# This function writes report data to a text file
def write_report(report, output_file):
    # open and write to file
    try:
        file = open(output_file, "w")
        # writes report dictionary to the text output file
        file.write("Average sentiment of all tweets: %.2f \n" % report["avg_sentiment"])
        file.write("Total number of tweets: %d \n" % report["num_tweets"])
        file.write("Number of positive tweets: %d \n" % report["num_positive"])
        file.write("Number of negative tweets: %d \n" % report["num_negative"])
        file.write("Number of neutral tweets: %d \n" % report["num_neutral"])
        file.write("Number of favorited tweets: %d \n" % report["num_favorite"])
        file.write("Average sentiment of favorited tweets: %0.2f \n" % report["avg_favorite"])
        file.write("Number of retweeted tweets: %d \n" % report["num_retweet"])
        file.write("Average sentiment of retweeted tweets: %.2f \n" % report["avg_retweet"])
        file.write("Top five countries by average sentiment: %s \n" % report["top_five"])
        # close file
        file.close()
        print("Wrote the report to %s " % output_file)

    # executes if IOError occurs
    except IOError:
        print("Could not open file %s " % output_file)
