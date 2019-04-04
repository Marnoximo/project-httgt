# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('metacritic.html')

@app.route('/gameranking')
def gameranking():
    return render_template('gameranking.html')

if __name__ == '__main__':
    app.run()
    
