from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import time
import os
import pika

WATCHED_FOLDER_PATH = './data'

# MESSAGE SENDING FUNCTION
def fire_messages(contents):
    print('[x] send message: ', contents)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='Tien7559'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=contents)
    connection.close()

# WATCHING CLASS
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

# EVENT HANDLING CLASS
class Handler(PatternMatchingEventHandler):
    patterns = ["*.csv"]
    
    def process (self, event):
        head, filename = os.path.split(event.src_path)
        if (filename == 'metacritic.csv'):
            fire_messages(filename)
        elif (filename == 'gameranking.csv'):
            fire_messages(filename)
        else:
            fire_messages(filename)
        
    def on_modified(self, event):
        self.process(event)

# MAIN SECTION
if __name__ == '__main__':
	w = Watcher()
	w.run()
