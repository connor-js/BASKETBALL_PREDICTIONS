'''
This is a program that will scrape data for each of the previous
WNBA MVP's from basketball reference, clean it and then store it
in a SQL data base.
'''

from bs4 import BeautifulSoup
import requests


def gather_data_from_site(url):
    """
    This is a function that gathers all data from the
    basketball reference page for past WNBA MVP's.

    :param: link to all the past WNBA MVP's
    :return: all of the data but not clean.
    """

    # A request is made to the website and set to parse through html.
    website_page = requests.get(url)
    website_data = BeautifulSoup(website_page.text, 'html.parser')

    # Parses through and selects table of MVP's and gets all its rows.
    table_of_mvps = website_data.find('table')
    mvp_data = table_of_mvps.find_all('tr')

    # Combines data sets together and returns
    return mvp_data


def clean_data_from_site(unclean_data):
    """
    This is a function that cleans data gathered from a
    table of the WNBA's past MVP's.

    :param: unclean and sorted data
    :return: cleaned data
    """

    # Cleaned dataset is created as list
    cleaned_data = []

    # Loop runs for each MVP.
    for mvp in unclean_data:
        # Finds each stat (needs to get header data and regular)
        statistics = mvp.find_all('th') + mvp.find_all('td')

        # Loop runs for each statistic.
        for x in range(len(statistics)):
            # Converts statistic to text form.
            statistics[x] = statistics[x].text.strip()

            # Converts statistic to float/int if possible
            statistics[x] = string_to_number_conversion(statistics[x])

        # Cleaned data is added to the list. 
        cleaned_data.append(statistics)

    # Removes first result as it is unnneeded data leftover from table.
    cleaned_data.pop(0)

    return cleaned_data


def string_to_number_conversion(input_string):
    """
    This is a function that converts strings to a
    float or integer (depending on what number is)
    or leaves string as is, if its not a number

    :param: string
    :return: unchanged string
    :return: int
    :return: float

    """

    # Tries to convert string to workable number if coming across
    # float/int
    try:
        converted_string = float(input_string)

        # Checks if number is int (like jersey number or year)
        # and keeps it as so.
        if converted_string.is_integer():
            converted_string = int(converted_string)

        return converted_string

    # Carries on as is if not a number
    except ValueError:
        return input_string


def list_to_dictionairy(list_form_data):
    """
    This is a function that takes each player and their
    data and puts it into a dictionairy form so it's easier
    to work with in SQL.

    :param: cleaned data in nested list form
    :return: cleaned data as a list of dictionairys
    """

    # Creates empty list so data in dictionairy form can be added.
    dictionairy_form_data = []

    # Runs for every list in the nested list except the first
    # because first is the list of different statictics.
    for x in range(1, len(list_form_data)):
        # New dictionairy is created
        players_stats_as_dict = {}

        # Runs for each item in list.
        for y in range(len(list_form_data[x])):
            # Exludes voting stat as its link to voting numbers not a stat.
            if list_form_data[x][y] != '(V)':
                # Makes key the stat name and the value the corresponding stat.
                players_stats_as_dict[list_form_data[0][y]] = clean_data[x][y]

        # Data is added to the list.
        dictionairy_form_data.append(players_stats_as_dict)

    return dictionairy_form_data


if __name__ == '__main__':
    raw_data = gather_data_from_site("https://www.basketball-reference.com/wnba/awards/mvp.html")
    clean_data = clean_data_from_site(raw_data)
    dict_form_data = list_to_dictionairy(clean_data)
