#  Student Name:Rashin Mir Sajjadi
#  Student Number:251348998
#  UWO UserName:smirsajj
#  date: 14/11/2023

# This python Main file contains the main functions that is the entry of the programme

# imports the sentiment_analysis module
from sentiment_analysis import *


# functions that gets tsv filename from the user and validates it
def get_tsv_file_name():
    # gets user tsv file name
    user_input = input("Input keyword filename (.tsv file): ")

    # Validates if its valid tsv file name
    if user_input.endswith(".tsv"):
        # return tsv file name if true
        return user_input
    else:
        # raise an Error
        raise Exception("Must have tsv file extension!")


# functions that gets csv filename from the user and validates it
def get_csv_file_name():
    # prompts the user to enter csv file name
    user_input = input("Input tweet filename (.csv file): ")

    # validates if user input is a valid csv file name
    if user_input.endswith(".csv"):
        # returns csv name if valid
        return user_input
    else:
        # raises an Error if it's invalid
        raise Exception("Must have csv file extension!")


# function that gets text file name and validates it
def get_text_file_name():
    # prompts the user to enter text file name
    user_input = input("Input filename to output report in (.txt file): ")

    # validates if its a valid text file name
    if user_input.endswith(".txt"):
        # return text file name if it is valid
        return user_input
    else:
        # raise an error if invalid
        raise Exception("Must have  txt file extension!")


def main():  # This function calls sentiment_analysis module functions

    tsv_file = get_tsv_file_name()

    csv_file = get_csv_file_name()

    txt_file = get_text_file_name()

    # gets  keywords dictionary from the tsv file, receives tsv file name
    keyword_dict = read_keywords(tsv_file)

    # gets a list of dictionaries of tweets, receives csv file name
    tweets_dict_list = read_tweets(csv_file)

    # checks for an empty dictionary or empty list
    if not keyword_dict or not tweets_dict_list:
        # raise an Exception if either is empty
        raise Exception("Tweet list or keyword dictionary is empty!")

    # gets a report analysis dictionary data
    report_dict = make_report(tweets_dict_list, keyword_dict)

    # write the report analysis data  dictionary to a file
    write_report(report_dict, txt_file)


# begin execution of the programme
main()
