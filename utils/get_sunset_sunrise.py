#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools
import pandas as pd

url = 'https://www.timeanddate.com/sun/canada/vancouver'
months = range(1, 13)
years = range(2003, 2017)
parsed_dates = list()
urls = list()
sunrise = list()
sunset = list()
time = list()


def month_and_years(years, months):
    for i in itertools.product(years, months):
        parsed_dates.append((i[0], i[1]))


def get_urls(base_url):
    for date in parsed_dates:
        target_url = '{}?month={}&year={}'.format(url, date[1], date[0])
        urls.append(target_url)


def get_sunrise_sunset(url_list):
    for link in url_list:
        soup = BeautifulSoup(urlopen(link).read(), 'lxml')
        table = soup.find('table')

        for row in table.findAll('td', {'class': 'c sep'}):
            sunrise.append(row.text.encode('ascii', 'ignore'))

        for row in table.findAll('td', {'class': 'sep c'}):
            sunset.append(row.text.encode('ascii', 'ignore'))


def parse_sunset_and_sunrise(sunrise_list, sunset_list):
    # index sunrise times
    sunrise_ = sunrise_list[::3]

    # put the raw sunset data into pandas series
    # to utilize the handy 'str.contains' feature
    sunset_ = pd.Series(sunset_list)
    # sunset times have (). i.e 5:11 AM  (52)
    sunset_ = sunset_[sunset_.str.contains(r'\(')].values

    for index, _ in enumerate(sunrise_):

        # sunrise
        x = '{} {}'.format(sunrise_[index].split(' ')[0],
                           sunrise_[index].split(' ')[1])

        # sunset
        y = '{} {}'.format(sunset_[index].split(' ')[0],
                           sunset_[index].split(' ')[1])

        time.append((x, y))

# run
month_and_years(years, months)
get_urls(url)
get_sunrise_sunset(urls)
parse_sunset_and_sunrise(sunrise, sunset)

data = pd.DataFrame(time, index=pd.date_range('2003-01-01', freq='D',
                                              periods=len(time)))
data.columns = ['Sunrise', 'Sunset']
data.to_csv('vancouver_sunset_sunrise (2003-2016).csv')
