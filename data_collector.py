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

    # A request is made to the website and set to parse through html
    website_page = requests.get(url)
    website_data = BeautifulSoup(website_page.text, 'html.parser')

    # Parses through and selects table of MVP's and gets all its rows
    table_of_mvps = website_data.find('table')
    mvp_data = table_of_mvps.find_all('tr')

    return mvp_data
