import unittest
from scripts import broken_link_detector
import os

class ZeemapsDownloaderTest(unittest.TestCase):

	def setUp(self):
		self.directory =  os.path.abspath('../2014_Winter') #'../../ZeeMap-929714.csv'

	def test_check_url_None(self):
		'''
		Checks if URL does NOT return either status code 301,302 or 404
		'''
		test_url = 'https://www.edx.org/'
		self.assertEquals(broken_link_detector.check_url(test_url), None)

	def test_check_url_404(self):
		'''
		Checks if URL does return either status code 301,302 or 404
		'''
		test_url = 'http://www.divched.org/'
		self.assertEquals(broken_link_detector.check_url(test_url)['status_code'], 404)

	def test_check_static_folder_None(self):
		'''
		Checks if file is in static folder
		'''
		self.assertEquals(broken_link_detector.check_static_folder(self.directory,'/static/CHEM181x_W01_L02_target_answer.png'), None)


	def test_check_static_folder_NA(self):
		'''
		Checks if file not in static folder
		'''
		self.assertEquals(broken_link_detector.check_static_folder(self.directory,'/static/c5f7240cf6d84cd4910ae5bc6d376b92/')['status_code'], 'NA')
	
if __name__ == '__main__':
	unittest.main()

