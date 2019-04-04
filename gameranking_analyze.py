# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
