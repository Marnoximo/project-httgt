# -*- coding: utf-8 -*-

import pika
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to convert scores into verdicts for gameranking
def gamerk_verdict(x):
    if x >= 90:
        return 'Very good'
    elif x >= 75:
        return 'Good'
    elif x >= 60:
        return 'Average'
    elif x >= 45:
        return 'Bad'
    else:
        return "Very bad"

# Function to analyze gameranking data and save figures
def analyze_gamerk():
    df = pd.read_csv('./data/gameranking.csv')
    if df is None:
        return False

    df.groupby(['platform']).count()['title'].plot.bar()
    plt.title('Number of titles by platforms')
    plt.savefig('./static/figures/gameranking/numTitlesByPlatforms.png', bbox_inches='tight')

    df.groupby(['platform']).mean()['score'].plot.bar()
    plt.title('Average scores by platforms')
    plt.savefig('./static/figures/gameranking/averageScoresByPlatforms.png', bbox_inches='tight')

    df['verdict'] = df['score'].apply(gamerk_verdict)

    df.groupby(['verdict']).count()['title'].plot.bar()
    plt.title('Number of titles by verdict')
    plt.savefig('./static/figures/gameranking/numTitlesByVerdict.png', bbox_inches='tight')
    
    df.groupby(['title']).mean()['score'].sort_values(ascending=False).head(15).plot.bar()
    plt.title('Top 15 games with highest scores')
    plt.savefig('./static/figures/gameranking/top15games.png', bbox_inches='tight')
    
    return True

# Function to convert metascores to verdicts
def metacritic_verdict(x):
    if x >= 90:
        return 'Very good'
    elif x >= 75:
        return 'Good'
    elif x >= 50:
        return 'Average'
    elif x >= 20:
        return 'Bad'
    elif x >= 1:
        return 'Very bad'
    else:
        return 'None'

# Function to analyze metacritic data and save figures
def analyze_metacritic():
    df = pd.read_csv('./data/metacritic.csv')
    if df is None:
        return False
    
    df['metascore'] = df['metascore'].apply(lambda x: float(x))
    df['userscore'] = df['userscore'].apply(lambda x: float(x) if x!='tbd' else 0)
    m_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, \
          'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    df['month'] = df['release_date'].apply(lambda x: x.split(',')[0].split(' ')[0]).map(m_dict)
    df['day'] = df['release_date'].apply(lambda x: int(x.split(',')[0].split(' ')[2]) if '  ' in x else int(x.split(',')[0].split(' ')[1]))
    df['year'] = df['release_date'].apply(lambda x: int(x.split(', ')[1]))
    
    df.groupby(['platform']).count()['title'].plot.bar()
    plt.savefig('./static/figures/metacritic/numTitlesByPlatforms.png', bbox_inches='tight')
    
    df.groupby(['platform']).mean()['metascore'].plot.bar()
    plt.savefig('./static/figures/metacritic/averageMetascoreByPlatform.png', bbox_inches='tight')

    df.groupby(['platform']).mean()['userscore'].plot.bar()
    plt.savefig('./static/figures/metacritic/averageUserscoreByPlatforms.png', bbox_inches='tight')
    
    df['metascore_verdict'] = df['metascore'].apply(metacritic_verdict)
    df['userscore_verdict'] = df['userscore'].apply(lambda x: metacritic_verdict(x*10))
    
    df.groupby(['metascore_verdict']).count()['title'].plot.bar()
    plt.savefig('./static/figures/metacritic/numTitlesByMetaVerdict.png', bbox_inches='tight')
    
    df.groupby(['userscore_verdict']).count()['title'].plot.bar()
    plt.savefig('./static/figures/metacritic/numTitlesByUserVerdict.png', bbox_inches='tight')
    
    return True

# CALLBACK FUNCTION (FUNCTION TO CALL WHEN GET NEW MESSAGES)
def callback(ch, method, properties, body):
    name = body.decode()
    if name == 'metacritic.csv':
        analyze_metacritic()
    elif name == 'gameranking.csv':
        analyze_gamerk()
        
    print('Got message from ', name)

# MAIN SECTION
if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='Tien7559'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
