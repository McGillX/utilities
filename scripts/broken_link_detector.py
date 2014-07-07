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
				if a['href'].startswith('/static'):
					# Slicing done so that local path is not considered absolute 
					# i.e. /static/<file_name> would be considered absolute, hence
					# removing '/' will enable to join static folder to directory
					link = check_static_folder(os.path.join(directory,a['href'][1:]))				
				else:
					link = check_url(a['href'])
				if link is not None:
					result[input_file].append(link)
			for a in soup.find_all('img'):
				if a['src'].startswith('/static'):
					# Slicing done so that local path is not considered absolute 
					# i.e. /static/<file_name> would be considered absolute, hence
					# removing '/' will enable to join static folder to directory
					link = check_static_folder(os.path.join(directory,a['href'][1:]))				
					if link is not None:
						result[input_file].append(link)
			return result
	except:
		pass

# def check_href(soup, result):
# 	global directory
# 	for a in soup.find_all('a', href=True):
# 		if a['href'].startswith('/static'):
# 			# Slicing done so that local path is not considered absolute 
# 			# i.e. /static/<file_name> would be considered absolute, hence
# 			# removing '/' will enable to join static folder to directory
# 			link = check_static_folder(os.path.join(directory,a['href'][1:]))				
# 		else:
# 			link = check_url(a['href'])
# 		if link is not None:
# 			result[input_file].append(link)
# def check_src(soup, result):
# 	'''
# 	Extracts src attributes from files
# 	'''
# 	global directory
# 	for a in soup.find_all('img'):
# 		if a['src'].startswith('/static'):
# 			# Slicing done so that local path is not considered absolute 
# 			# i.e. /static/<file_name> would be considered absolute, hence
# 			# removing '/' will enable to join static folder to directory
# 			link = check_static_folder(os.path.join(directory,a['href'][1:]))				
# 			if link is not None:
# 				result[input_file].append(link)

def check_static_folder(link):
	'''
	Checks if file exists in static folder
	'''
	result = {}
	if not os.path.exists(link):
		result['link'] = link
		result['status_code'] = 'NA'
		result['status'] = 'File does not exist'
		return result	

def check_url(link):
	'''
	Checks status code of URL
	'''
	result = {}
	r = requests.head(link)
	#print link, r.status_code
	if r.status_code != 200:
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
	data_csv = csv.writer(open('broken_links.csv', 'w'))
	data_csv.writerow(['File name','URL link', 'Status Code', 'Status'])
	global directory
	directory = args[0]
	for root, dirnames, filenames in os.walk(directory):
		if not dirnames:
			for item in filenames:
				result = retrieve_links(os.path.join(root, item))
				if result:
					data.append(result)
					write_to_csv(data_csv, result)
	write_to_json('broken_links.json', data)		

if __name__ == '__main__':
	main()