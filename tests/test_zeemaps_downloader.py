import unittest
from scripts import zeemaps_downloader 
import os

class ZeemapsDownloaderTest(unittest.TestCase):

	def setUp(self):
		self.csv_file =  os.path.abspath('../ZeeMap-929714.csv') #'../../ZeeMap-929714.csv'

	def test_csv_file_exists(self):
		'''
		Test if CSV file exists
		'''
		self.assertTrue(zeemaps_downloader.csv_file_exists(self.csv_file))

	def test_rename_image_without_http_scheme(self):
		'''
		Test if image is renamed to human readable format for a URL without an http schema
		'''
		extension = '.jpg'
		index = '101'
		row = ['', 'Montreal', '1001 Sherbrooke', 'Montreal', 'Quebec', 'Canada', 'H2A 2C2', 'red', '//zeemapsimages.s3.amazonaws.com/36234c2cd1b03f95da6cf5bebd7270e1-nouvelle.jpg', '', '', '', '', '','']
		self.assertEquals(zeemaps_downloader.rename_image(row, extension, index), 'Canada_Quebec_Montreal_%s%s' % (index, extension))

	def test_rename_image_with_http_scheme(self):
		'''
		Test if image is renamed to human readable format for a URL with an http schema
		'''
		extension = '.jpg'
		index = '101'
		row = ['', 'Montreal', '1001 Sherbrooke', 'Montreal', 'Quebec', 'Canada', 'H2A 2C2', 'red', 'http://zeemapsimages.s3.amazonaws.com/36234c2cd1b03f95da6cf5bebd7270e1-nouvelle.jpg', '', '', '', '', '','']
		self.assertEquals(zeemaps_downloader.rename_image(row, extension, index), 'Canada_Quebec_Montreal_%s%s' % (index, extension))

	def test_rename_image_with_https_scheme(self):
		'''
		Test if image is renamed to human readable format for a URL with an https schema
		'''
		extension = '.jpg'
		index = '101'
		row = ['', 'Montreal', '1001 Sherbrooke', 'Montreal', 'Quebec', 'Canada', 'H2A 2C2', 'red', 'https://zeemapsimages.s3.amazonaws.com/36234c2cd1b03f95da6cf5bebd7270e1-nouvelle.jpg', '', '', '', '', '','']
		self.assertEquals(zeemaps_downloader.rename_image(row, extension, index), 'Canada_Quebec_Montreal_%s%s' % (index, extension))

if __name__ == '__main__':
	unittest.main()