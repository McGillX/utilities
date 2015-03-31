utilities
=========

Useful scripts for McGill/edX Courses

List of Scripts
============
1) **broken_link_detector.py**: Detect broken links in course content

 
2) **zeemaps_downloader.py**: 
    Downloads images from ZeeMap CSV file which contains path to images hosted on Amazon S3 (public)
    
To get the ZeeMap CSV:
* In the navbar click Map
* Select "Save  As CSV" from the dropdown
* Go to the admin dashboard of your ZeeMap

Usage
==========
1) **broken_link_detector.py**:

    python broken_link_detector.py <path_to_folder>
    
    Note, install the required libraries: beautifulsoup, requests, argparse

2) **zeemaps_downloader.py**:

    python zeemaps_downloader.py <path_to_csv_file> <path_to_output_directory>
    
Tests
=====

To run all the tests, under the utilities folder, just do:

    $ python -m unittest discover tests -v

To run individual tests, under the utilities folder,

    $ python -m unittest tests.<module name>
