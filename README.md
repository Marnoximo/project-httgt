System details:
1/ Crawl data from metacritic.com and gameranking.com => 2 csv files saved in data folder
2/ The watcher watch any modification in data folder and fire messages to RabbitMQ server (local)
3/ The receiver get messages from RabbitMQ and then parse them, conduct the appropriate analyzing process. Result graphs are saved in static folder
4/ The flask web visualizes results

Requirements:
1/ RabbitMQ-server is installed and started
2/ watchdog, urllib, beautifulsoup4 for crawling
3/ pika for communicating with RabbitMQ from python apps
4/ pandas, matplotlib for analyzing
5/ flask for python web

How to run:
1/ Run watcher.py to begin to watch
2/ Run receive.py to begin to wait for message
3/ Run crawl_metacritic.py to get data from metacritic.com
4/ Run crawl_gameranking.py to get data from gameranking.com
5/ Run web.py to create a local flask website for visualizing
