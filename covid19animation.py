import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import datetime as dt
import numpy as np
from IPython.display import HTML

covid19 = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')

df = pd.melt(covid19,id_vars = ['Province/State','Country/Region','Lat','Long'], var_name = 'Date', value_name = 'Cases')

df['Date'] = pd.to_datetime(df['Date'])
df['Province/State'].fillna(df['Country/Region'], inplace=True)
#print(df)
counter = 43895

#groupLk = covid19Unpivot.set_index('Province/State')['Country/Region'].to_dict()

df1 = df.groupby(['Country/Region','Date'],as_index=False).sum()
del df1['Lat']
del df1['Long']
#df1 = df1[df1['Country/Region'] != 'China']
#print(df1)
maxCases = df1['Cases'].max()

fig, ax = plt.subplots(figsize=(16, 9))

def draw_barchart(counter):
    currentDate = dt.datetime.fromordinal(dt.datetime(1900, 1, 1).toordinal() + int(counter) - 2)
    dff = df1[df1['Date'].eq(currentDate)].sort_values(by='Cases', ascending=True).tail(15)
    #print(dff)
    ax.clear()
    ax.barh(dff['Country/Region'], dff['Cases'], color = '#b5c1e6')
    dx = dff['Cases'].max() / 200
    for i, (value, name) in enumerate(zip(dff['Cases'], dff['Country/Region'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='center')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
    # ... polished styles
    ax.text(1, 0.4, dt.datetime.strftime(currentDate,'%d/%m/%Y'), transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
    ax.text(0, 1.06, 'Population infected', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, 'Covid-19 Cases excl. China',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by: Andy Sawyer | credit: towardsdatascience.com | datasource: JHU CSSE', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    plt.xlim([0,maxCases+1000])
    
draw_barchart(counter)

from IPython.display import HTML
fig, ax = plt.subplots(figsize=(16, 9))

minDate = df1['Date'].min()
maxDate = df1['Date'].max()
startDate = minDate #dt.datetime(2020, 1, 25)
endDate = maxDate #dt.datetime(2020, 3, 15)
temp = dt.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
deltaStart = startDate - temp
deltaEnd = endDate - temp
startDateInt = int(deltaStart.days)
endDateInt = int(deltaEnd.days) + 1

animator = animation.FuncAnimation(fig, draw_barchart, frames = range(startDateInt,endDateInt), repeat_delay=3000, interval=700)
HTML(animator.to_jshtml())
animator.save('covid19.mp4')