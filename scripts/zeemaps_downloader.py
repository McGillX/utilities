'''
This module loads image urls from a csv file, downloads thr images and stores 
them in an output directory
'''

import requests
import csv
import argparse

EXTENSIONS = {'', '', '', ''}

def read_csv(csv_file):
	pass



def define_arguments_parser():
	'''
	Define command line arguments that are accepted by the script
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument(dest='input',nargs='+',help="CSV files to be loaded")
	args = parser.parse_args()
	return args.input

def main():
	args = define_arguments_parser()
	print args

if __name__ == '__main__':
	main()