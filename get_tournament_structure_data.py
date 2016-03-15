#! /usr/bin/env python3

from bs4 import BeautifulSoup
import os, os.path
import requests
import shutil
from sys import argv

cache_argv = "delete-cache"

tournament_structure_folder = "tournament-structure"
out_file_format = "%d_tournament_structure.html"

url_format = "http://www.sports-reference.com/cbb/postseason/%d-ncaa.html"
start_year = 2001
end_year = 2015
years = range(start_year, end_year + 1)

if cache_argv in argv:
	if os.path.isdir(tournament_structure_folder):
		os.system("rm -rf %s" % tournament_structure_folder)

if not os.path.isdir(tournament_structure_folder):
	os.system("mkdir %s" % tournament_structure_folder)

for year in years:
	out_file_name = os.path.join(tournament_structure_folder, out_file_format % year)
	if os.path.exists(out_file_name):
		print("CACHED - %d tournament structure data" % year)
	else:
		print("Downloading %d tournament structure data..." % year)
		out_file = open(out_file_name, 'wb')
		out_file.write(requests.get(url_format % year).content)
		out_file.close()