#! /usr/bin/env python3

from bs4 import BeautifulSoup
import os, os.path
import requests
from sys import argv

delete_cache = "delete-cache"

base_link = "http://sports-reference.com"

tournament_data_folder_format = "%d-tournament-data"
out_file_format = "%d_%s_tournament_data.html"

tournament_results_folder = "tournament-results"
tournament_results_format = "%d_real_results.txt"

tournament_structure_folder = "tournament-structure"
tournament_structure_format = "%d_tournament_structure.html"

start_year = 2001
end_year = 2016
years = range(start_year, end_year + 1)

def get_tournament_data_for_one_year(year):
	print("%s%d%s" % ("=" * 13, year, "=" * 13))
	current_folder = tournament_data_folder_format % year
	should_delete = delete_cache in argv or ("delete-%d" % year) in argv
	if os.path.isdir(current_folder) and should_delete:
		os.system("rm -rf %s" % current_folder)
	if not os.path.isdir(current_folder):
		os.system("mkdir %s" % current_folder)
	tournament_structure_file = open(os.path.join(tournament_structure_folder, tournament_structure_format % year))
	tournament_structure = tournament_structure_file.read()
	tournament_structure_file.close()
	soup = BeautifulSoup(tournament_structure, "html.parser")
	all_team_elements = [list(filter(lambda x: 'rowspan' not in x.attrs,\
							         seed.parent.findChildren('td', {'class' : ''})))[0]\
				               for seed in soup.findChildren('td', {'class' : 'seed'})]
	all_team_links = [x.findChildren('a', {'class' : ''})[0] for x in all_team_elements]
	for team_link in all_team_links:
		team = team_link.text
		link = team_link['href']
		short_team_name = link.split('/')[-2]
		out_file_name = os.path.join(tournament_data_folder_format % year,\
			                         out_file_format % (year, short_team_name))
		if os.path.exists(out_file_name):
			print("CACHED - (%s, %d) data" % (team, year))
		else:
			print("Downloading data for %s in %d..." % (team, year))
			out_file = open(out_file_name, 'wb')
			out_file.write(requests.get(base_link + link).content)
			out_file.close()
	print("=" * 30)

if __name__ == '__main__':
	for year in years:
		get_tournament_data_for_one_year(year)