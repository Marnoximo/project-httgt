from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
import pathlib
from glob import glob
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

WATCHED_FOLDER_PATH = './data'

def verbalise(x):
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
    
    df['metascore_verdict'] = df['metascore'].apply(verbalise)
    df['userscore_verdict'] = df['userscore'].apply(lambda x: verbalise(x*10))
    
    df.groupby(['metascore_verdict']).count()['title'].plot.bar()
    plt.savefig('./static/figures/metacritic/numTitlesByMetaVerdict.png', bbox_inches='tight')
    
    df.groupby(['userscore_verdict']).count()['title'].plot.bar()
    plt.savefig('./static/figures/metacritic/numTitlesByUserVerdict.png', bbox_inches='tight')
    
    return True

def get_verdict(x):
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

    df['verdict'] = df['score'].apply(get_verdict)

    df.groupby(['verdict']).count()['title'].plot.bar()
    plt.title('Number of titles by verdict')
    plt.savefig('./static/figures/gameranking/numTitlesByVerdict.png', bbox_inches='tight')
    
    df.groupby(['title']).mean()['score'].sort_values(ascending=False).head(15).plot.bar()
    plt.title('Top 15 games with highest scores')
    plt.savefig('./static/figures/gameranking/top15games.png', bbox_inches='tight')
    
    return True

def data_handler():
    print('Got event!')
    if 'gameranking.csv' in os.listdir('./data'):
        analyze_gamerk()
        print('Analyzed gameranking data')
    if 'metacritic.csv' in os.listdir('./data'):
        analyze_metacritic()
        print('Analyzed metacritic data')

class Watcher:
	directory = WATCHED_FOLDER_PATH
	
	def __init__(self):
		self.observer = Observer()
	
	def run(self):
		event_handler = Handler()
		self.observer.schedule(event_handler, self.directory, recursive=True)
		self.observer.start()
		try:
			while True:
				time.sleep(5)
		except:
			self.observer.stop()
			print('Error')
		self.observer.join()

class Handler(FileSystemEventHandler):
	@staticmethod
	def on_any_event(event):
		data_handler()

if __name__ == '__main__':
	w = Watcher()
	w.run()
