# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:38:02 2022

@author: matth
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


task1url = 'https://www.nhc.noaa.gov/pastdec.shtml'
wx_page = requests.get(task1url, headers={'User-agent': 'Mozilla/5.0'})
soup = BeautifulSoup(wx_page.text, 'html.parser')


#Store the tables down as a soup file
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx.html", "w", encoding='utf-8') as file: file.write(str(soup))
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx.html") as fp: soup = BeautifulSoup(fp, 'html.parser')

#Task 1 - Hurricans
wx_df = pd.read_html(str(soup.table))[0]
wx_df.columns = wx_df.columns.get_level_values(0)

#Convert the data frame from wide type to long type for plotting
long_df = pd.melt(wx_df, id_vars='Decade', value_vars= wx_df.columns.get_level_values(0)[6])
long_df.drop([16, 17, 18], inplace = True)
long_df.drop(["variable"], axis = 1, inplace = True)

long_df["value"] = long_df["value"].astype(str).astype(int)

#Plots of the hurricane data
sns.set(font_scale=1.0)
sns.relplot(data = long_df, x = "Decade", y = "value", kind = "line", height = 5, aspect = 2).set(title = "No. of Hurricane Strikes", xlabel = "Decade", ylabel = "Number")

#Task 2 - Flights
task2url = 'https://flightaware.com/live/flight/AAL481/history'
wx2_page = requests.get(task2url, headers={'User-agent': 'Mozilla/5.0'})
soup2 = BeautifulSoup(wx2_page.text, 'html.parser')

#Store the tables down as a soup file
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx2.html", "w", encoding='utf-8') as file: file.write(str(soup2))
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx2.html", "r", encoding='utf-8') as fp: soup2 = BeautifulSoup(fp, 'html.parser')

flights = []
flights_table = soup2.find('table', {"class" : "prettyTable fullWidth tablesaw tablesaw-stack"})

try:
#loop through table, grab each of the 7 columns shown 
    for row in flights_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 7:
            flights.append((cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip(), cols[6].text.strip()))
except: pass  

flights_array = np.asarray(flights)
len(flights_array)

#convert new array to dataframe
flight_df = pd.DataFrame(flights_array)

#rename columns, check output
flight_df.columns = ['Date', 'Aircraft', 'Origin','Destination', 'Departure', 'Arrival', 'Duration']
flight_df['Duration'] = pd.to_datetime(flight_df['Duration'], errors='coerce')
flight_df = flight_df.dropna(subset = ['Duration'])
flight_df['Time'] = ((pd.to_datetime(flight_df['Duration'], format = "%H:%M").dt.hour)*60) + pd.to_datetime(flight_df['Duration'], format = "%H:%M").dt.minute
print(flight_df['Time'].describe())

#Task 3 - WSJ

task3url = 'http://wsj.com'
wx3_page = requests.get(task3url, headers={'User-agent': 'Mozilla/5.0'})
soup3 = BeautifulSoup(wx3_page.text, 'html.parser')

#Store the tables down as a soup file
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx3.html", "w", encoding='utf-8') as file: file.write(str(soup3))
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx3.html", "r", encoding='utf-8') as fp: soup3 = BeautifulSoup(fp, 'html.parser')

popular_stories = soup3.find_all(class_ = 'WSJTheme--headline--nQ8J-FfZ')
stories_array = np.asarray(popular_stories)
adj_stories_array = stories_array[0:5]
print(adj_stories_array)

#Task 4 - Eater

task4url = 'https://philly.eater.com/maps/38-best-philadelphia-restaurants'
wx4_page = requests.get(task4url, headers={'User-agent': 'Mozilla/5.0'})
soup4 = BeautifulSoup(wx4_page.text, 'html.parser')

#Store the tables down as a soup file
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx4.html", "w", encoding='utf-8') as file: file.write(str(soup4))
with open("C:\\Users\\matth\\Wharton\\STATS 710\\wx4.html", "r", encoding='utf-8') as fp: soup4 = BeautifulSoup(fp, 'html.parser')

rest = []
for i in range (0,39):
    try:
        rest.append(soup4.find_all('h1', class_ = '')[i].text)
        i+=1
    except KeyError:
        i+=1
                
del rest[0]
print(rest)