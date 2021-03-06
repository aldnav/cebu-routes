from bs4 import BeautifulSoup
from collections import OrderedDict
from Queue import Queue
from threading import Thread, Lock
import threading
import requests
import logging
import json

logging.basicConfig(
    filename='cebujeepneys.log',
    level=logging.WARNING,
    format='%(message)s')
base_url = 'http://cebujeepneys.weebly.com/'
proxies = {
    'https':'https://112.199.65.186:3128',
    'https':'https://116.93.58.85:8080',
}
codes = Queue()
lock = Lock()
pool = []

def get_codes():
	r = requests.get(base_url)
	soup = BeautifulSoup(r.text)
	listing = soup.findAll('ul', {'class', 'wsite-menu-default'})[0].contents
	global codes
	for item in listing:
		codes.put(item.a.text)

def dist():
	global codes
	with lock:
	# 	code = codes.get()
	# print threading.currentThread().name + ' - ' + code
	scrape(code)

def scrape(code):
	r = requests.get(base_url+code+'.html', proxies=proxies)
	r.encoding = 'utf-8'
	if r.status_code == requests.codes.ok:
		get_details(r, code)

def get_details(r, code):
	soup = BeautifulSoup(r.text)
	details = soup.findAll('div', {'class','paragraph'})
	print r.url
	data = OrderedDict()
	data['code'] = code
	lim = len(details)
	description = []
	if lim > 1:
		for i in xrange(0, lim-1):
			des = []
			for d in details[i].stripped_strings:
				des.append(d.replace(u'\u00a0',' '))
			description.append(','.join(des))
		data['description'] = ' === '.join(description)
	else:
		data['description'] = 'NA'
	log(data)

def log(data):
	logging.warning(json.dumps(data, indent=4))

def main():
	get_codes()
	
	global codes
	for i in xrange(codes.qsize()):
		pool.append(Thread(target=dist))
	for worker in pool:
		worker.start()

	for worker in pool:
		worker.join()

if __name__ == '__main__':
	main()
