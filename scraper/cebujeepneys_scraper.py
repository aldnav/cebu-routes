from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(filename='dining.log', level=logging.DEBUG, format='$(message)s')
base_url = 'http://cebujeepneys.weebly.com/'
codes = []

def get_codes():
	r = requests.get(base_url)
	soup = BeautifulSoup(r.text)
	listing = soup.findAll('ul', {'class', 'wsite-menu-default'})[0].contents
	global codes
	for item in listing:
		codes.append(item.a.text)

def main():
	get_codes()

if __name__ == '__main__':
	main()