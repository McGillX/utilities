utilities
=========

Useful scripts for McGill/edX Courses

List of Scripts
============
1) **broken_link_detector.py**: Detect broken links in course content

2) **zeemaps_downloader.py**: Download images from ZeeMap CSV file which contains path to images in Amazon S3 (public)

Usage
==========
1) **broken_link_detector.py**:

    python broken_link_detector.py <path_to_folder>
    
    Required libraries:
        beautifulsoup
        requests
        argparse
        os
        json
        csv
        re

2) **zeemaps_downloader.py**:

    python zeemaps_downloader.py <path_to_csv_file> <path_to_output_directory>
    
Tests
=====

To run all the tests, under the utilities folder, just do:

    $ python -m unittest discover tests -v

To run individual tests, under the utilities folder,

    $ python -m unittest tests.<module name>
