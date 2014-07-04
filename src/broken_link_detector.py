'''
Script that crawls through html and xml file of provided folder and finds all
broken links and stores them in a csv file
'''

from bs4 import BeautifulSoup
import requests
import argparse
import os
import json

# After exporting course content fron edX Studio to local computer or server,
# user can update the  constant variable SESSION to the name of the downloaded folder
SESSION = '2014_Winter'

# Base directory in which exported course content folder was stored
# E.g. Currently I store my course content folder in the Downloads folder
# User can change it with respect to where the exported course content folder was stored
BASE = '/Users/ue/Downloads/'

def load_folder():
	pass


def retrieve_links(input_file):
	'''
	Retrieve all urls and static files (href or src attributes that have files stored 
	in the static folder) from given file
	'''
	try:
		with open(input_file, 'r') as f:
			soup = BeautifulSoup(f)
			result = {input_file : [check_link(a['href']) for a in soup.find_all('a', href=True)]}
			return result
	except:
		pass
	#key = SESSION + input_file.split(SESSION)[1]
	

def check_link(link):
	'''
	Check status code of URL
	'''
	result = {}
	
	try:
		# Check if link is a URL

		r = requests.head(link)
		#print r.status_code
		if r.status_code != 200:
			#print "hello", r.status_code 
			result['link'] = link
			result['status_code'] = r.status_code
			result['status'] = r.reason
			return result
			
	except:
		# Link is local file in static folder
		#print BASE+SESSION + link, os.path.exists(BASE+SESSION + link)
		if not os.path.exists(BASE+SESSION + link):
			result['status'] = 'File does not exist'
			result['status_code'] = 'NA'
			return result		
	#print result
	#json.dumps(result)

def define_arguments_parser():
	'''
	Define command line arguments that are accepted by the script
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument(dest='input',nargs='+',help="Load file or list of files or directory or list of directories")
	args = parser.parse_args()
	return args.input

def main():
	input_list = define_arguments_parser()
	folders = filter(os.path.isdir, input_list)
	files = filter(os.path.isfile, input_list)
	#print retrieve_links(files[0])
	data = []
	for i in files:
		#print i
		data.append(retrieve_links(i))
	#print folders
	for folder in folders:		 
		for f in os.listdir(folder):
			if os.path.isfile(os.path.join(folder,f)):
				print f
				data.append(retrieve_links(os.path.join(folder,f)))
			else:
				file_path = os.path.join(folder,f)
				for i in os.listdir(file_path):
					if os.path.isfile(os.path.join(file_path,i)):	 
						data.append(retrieve_links(os.path.join(file_path,i)))
	#print data

if __name__ == '__main__':
	main()
	#check_link('/static/CHEM181x_SYLLABUS_BANNER.png')
