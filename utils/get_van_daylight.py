#!/usr/bin env python
from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools
import pandas as pd

url = 'https://www.timeanddate.com/sun/canada/vancouver'
months = range(1, 13)
years = range(2003, 2017)
parsed_dates = list()
urls = list()
daylight_hours = list()


def month_and_years(years, months):
    for i in itertools.product(years, months):
        parsed_dates.append((i[0], i[1]))


def get_urls(base_url):
    for date in parsed_dates:
        target_url = '{}?month={}&year={}'.format(url, date[1], date[0])
        urls.append(target_url)


def get_daylight_hours(url_list):
    for link in url_list:
        soup = BeautifulSoup(urlopen(link).read(), 'lxml')
        table = soup.find('table')
        for row in table.findAll('td', {'class': 'c tr sep-l'}):
            daylight_hours.append(row.string)

month_and_years(years, months)
get_urls(url)
get_daylight_hours(urls)

data = pd.DataFrame({'Hours': daylight_hours}, index=pd.date_range(
    '2003-01-01', freq='D', periods=len(daylight_hours)))

data.to_csv('Vancouver_daylight_hours (2003-2016).csv')
