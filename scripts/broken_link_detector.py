'''
Script that crawls through html and xml file of provided folder and finds all
broken links and stores them in a csv file
'''

from bs4 import BeautifulSoup
import requests
import argparse
import os
import json
import csv
from collections import defaultdict
import re 

def retrieve_links(input_file):
	'''
	Retrieve all urls and static files (href or src attributes that have files stored 
	in the static folder) from given file
	'''	
	try:
		with open(input_file, 'r') as f:
			soup = BeautifulSoup(f)
			result = defaultdict(list)
			global directory
			for a in soup.find_all('a', href=True):
				# Link to static files in href attribute
				if a['href'].startswith('/static'):
					#link = check_static_folder(os.path.join(directory,a['href'][1:]))	
					link = check_static_folder(directory,a['href'])	
					if link is not None:
						result[input_file].append(link)	
				# Link to URL in href attribute
				else:
					link = check_url(a['href'])
					if link is not None:
						result[input_file].append(link)
			# Link to images in static folder
			for a in soup.find_all('img'):
				if a['src'].startswith('/static'):
					#link = check_static_folder(os.path.join(directory,a['src'][1:]))
					link = check_static_folder(directory,a['src'])				
					if link is not None:
						result[input_file].append(link)					
			return result
	except:
		pass

def check_static_folder(link1, link2):
	'''
	Checks if file exists in static folder. EdX platform replaces all spaces 
	and ampersand (&) punctuation with an underscore. In order to get around
	this, replace all underscores with a regex wildcard '.' and look for new 
	compile regex in static folder
	'''
	link_file = link2.split('/static/')
	r = link_file[-1].replace('_','.')
	regex = re.compile(r)
	result = {}
	if link1[-1] != '/':
		link1 += '/'
	for root, dirs, files in os.walk(link1 + 'static'):
		for item in files:
			if re.search(regex, item):
				return None
	result['link'] = os.path.join(link1 + 'static', link_file[-1])
 	result['status_code'] = 'NA'
 	result['status'] = 'File does not exist'
 	return result	

def check_url(link):
	'''
	Checks status code of URL. Return only broken links which has status codes
	301, 302, or 404
	'''
	result = {}
	r = requests.head(link)
	#print link, r.status_code
	if r.status_code != 200 and r.status_code in [301,302,404]:
		result['link'] = link
		result['status_code'] = r.status_code
		result['status'] = r.reason
		return result	

def define_arguments_parser():
	'''
	Define command line arguments that are accepted by the script
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument(dest='input',nargs=1,help="Load folder")
	args = parser.parse_args()
	return args.input

def write_to_csv(csv_file, result):
	'''
	Write result to csv file
	'''
	for key,value in result.iteritems():
		for index in value:
			csv_file.writerow([key,index['link'],index['status_code'],index['status']])

def write_to_json(json_file, result):
	'''
	Write result to json file
	'''
	with open(json_file, 'w') as outfile:
  		json.dump(result, outfile)

def main():
	args = define_arguments_parser()
	data = []
	with open('broken_links.csv', 'w') as csv_file:
		data_csv = csv.writer(csv_file)
		data_csv.writerow(['File name','URL link', 'Status Code', 'Status'])
		csv_file.flush()
		global directory
		directory = args[0]
		for root, dirnames, filenames in os.walk(directory):
			if not dirnames:
				for item in filenames:
					result = retrieve_links(os.path.join(root, item))
					if result:
						data.append(result)
						write_to_csv(data_csv, result)
						csv_file.flush()
		write_to_json('broken_links.json', data)

if __name__ == '__main__':
	main()