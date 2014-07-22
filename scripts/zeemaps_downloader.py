'''
This module loads image urls from a csv file, downloads thr images and stores 
them in an output directory
'''

import requests
import csv
import argparse
import os
import urllib

IMAGE_URL_COLUMN = 8

def extract_and_download_images(csv_file, directory):
	'''
	Return reader object which will iterate over lines in the given csv file
	'''
	with open(csv_file, 'rb') as file_object:
		reader = csv.reader(file_object)
		reader.next()
		for index,row in enumerate(reader):
			if row[IMAGE_URL_COLUMN]:
				extension = os.path.splitext(row[IMAGE_URL_COLUMN])[1]
				image_name = rename_image(row, extension, index)
				# Some URLs start with http or https and some do not
				if row[IMAGE_URL_COLUMN].startswith('http'):
					image_url = row[IMAGE_URL_COLUMN]
				else:
					image_url = 'http:' + urllib.pathname2url(row[IMAGE_URL_COLUMN])
				try:
					urllib.urlretrieve(image_url, os.path.join(directory, image_name))
				except:
					print 'Fail -> %d : %s' %(index, row[IMAGE_URL_COLUMN])

def rename_image(row, extension, index):
	'''
	Rename image to url to more readable format using Country, State and city
	from zeemap info and index
	'''
	country = row[5]
	state = row[4]
	city = row[3]
	image_name = ''
	if country:
		image_name += country.replace(' ', '_') + '_'
	if state:
		image_name += state.replace(' ', '_') + '_'
	if city:
		image_name += city.replace(' ', '_') + '_'
	image_name += str(index) + extension
	return image_name

def csv_file_exists(csv_file):
	'''
	Check if csv file exists
	'''
	if os.path.isfile(csv_file):
		return True
	else:
		raise Exception("CSV file %s does not exist" % csv_file)

def assure_directory_exists(directory):
	'''
	Check if directory exists and if does not exist,
	create directory
	'''
	try:
		os.makedirs(directory)
	except OSError:
		if not os.path.isdir(directory):
			raise Exception("Not a valid directory")

def define_arguments_parser():
	'''
	Define command line arguments that are accepted by the script
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument(dest='input',nargs=2,help="CSV file to be loaded followed by path to output directory" +
		"(directory will be created if it does not exist)")
	args = parser.parse_args()
	return args.input

def main():
	args = define_arguments_parser()
	csv_file_exists(args[0])
	assure_directory_exists(args[1])
	extract_and_download_images(args[0], args[1])

if __name__ == '__main__':
	main()