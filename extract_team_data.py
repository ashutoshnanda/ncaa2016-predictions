#! /usr/bin/env python3

from bs4 import BeautifulSoup
import os, os.path
import pandas as pd

tournament_structure_folder_format = "%d-tournament-data"
assembled_data_format = "%s_data.csv"

tournament_listing_format = "tournament-results/%s_real_results.txt"

def get_headers():
	return ['Name', 'Wins', 'Seed', 'G', 'W', 'L', 'WPer', 'CW', 'CL', 'CWPer', 'PSG', 'PAG', 'PDG', 'SRS', 'SOS',\
	        'FGM', 'FGA', 'FGPer', 'TwFGM', 'TwFGA', 'TwFGPer', 'ThFGM', 'ThFGA', 'ThFGPer', 'FTM', 'FTA', 'FTPer',\
	        'Reb', 'Ast', 'Stl', 'Blk', 'Pts']

def get_data_from_html(data_file_name):
	year = data_file_name.split("-")[0]
	data_dict = {}
	data_file = open(data_file_name, 'r')
	soup = BeautifulSoup(data_file.read(), "html.parser")
	data_file.close()
	name = soup.find('h1').findNext('div').findChildren('a')[0].text.split("\xa0")[0]
	print(name, end = " ", flush = True)
	previous_stats_element = soup.find('h1').findNext('p')
	tournament_listing_file = open(tournament_listing_format % year)
	tourney_wins = 0
	for i, line in enumerate(tournament_listing_file):
		if i != 0:
			tourney_wins += line.split(", ").count(name)
	tournament_listing_file.close()
	year_summary = previous_stats_element.findNext('p')
	year_summary_parts = year_summary.text.split(" ")
	num_wins = float(year_summary_parts[1].split("-")[0])
	num_losses = float(year_summary_parts[1].split("-")[1][:-1].replace("*", ""))
	win_percentage = num_wins / (num_wins + num_losses)
	conf_num_wins = float(year_summary_parts[7].split("-")[0])
	conf_num_losses = float(year_summary_parts[7].split("-")[1][:-1])
	conf_win_percentage = conf_num_wins / (conf_num_wins + conf_num_losses)
	year_stats_summary = year_summary.findNext('p')
	year_stats_summary_parts = year_stats_summary.text.split(" ")
	points_scored_per_game = float(year_stats_summary_parts[1])
	points_allowed_per_game = float(year_stats_summary_parts[7])
	average_point_differential = points_scored_per_game - points_allowed_per_game
	simple_rating_system = float(year_stats_summary_parts[11])
	strength_of_schedule = float(year_stats_summary_parts[17])
	tournament_info = year_stats_summary.findNext('p')
	if name == "Notre Dame" and '2016' in data_file_name:
		seed = 6
	elif name == "Oregon" and '2016' in data_file_name:
		seed = 1
	else:
		seed = int(tournament_info.text.split(" ")[2].replace("(#", ""))
	first_row_team_stats = soup.find(id = "team_stats").findChildren('tr')[1].findChildren('td')
	num_games_played = int(first_row_team_stats[1].text)
	if data_file_name == '2006-tournament-data/2006_southern_tournament_data.html':
		num_games_played = 33
	field_goals_made = int(first_row_team_stats[3].text)
	field_goals_attempted = int(first_row_team_stats[4].text)
	field_goal_percentage = float(field_goals_made) / field_goals_attempted
	two_point_field_goals_made = int(first_row_team_stats[6].text)
	two_point_field_goals_attempted = int(first_row_team_stats[7].text)
	two_point_field_goal_percentage = float(two_point_field_goals_made) / two_point_field_goals_attempted
	three_point_field_goals_made = int(first_row_team_stats[9].text)
	three_point_field_goals_attempted = int(first_row_team_stats[10].text)
	three_point_field_goals_percentage = float(three_point_field_goals_made) / three_point_field_goals_attempted
	free_throws_made = int(first_row_team_stats[12].text)
	free_throws_attempted = int(first_row_team_stats[13].text)
	free_throw_percentage = float(free_throws_made) / free_throws_attempted
	total_rebounds = int(first_row_team_stats[17].text)
	assists = int(first_row_team_stats[18].text)
	steals = int(first_row_team_stats[19].text)
	blocks = int(first_row_team_stats[20].text)
	total_points = int(first_row_team_stats[23].text)
	return [name, tourney_wins, seed, num_games_played, num_wins, num_losses, win_percentage,\
	        conf_num_wins, conf_num_losses, conf_win_percentage,\
	        points_scored_per_game, points_allowed_per_game, average_point_differential,\
	        simple_rating_system, strength_of_schedule,\
	        field_goals_made, field_goals_attempted, field_goal_percentage,\
	        two_point_field_goals_made, two_point_field_goals_attempted, two_point_field_goal_percentage,\
	        three_point_field_goals_made, three_point_field_goals_attempted, three_point_field_goals_percentage,\
	        free_throws_made, free_throws_attempted, free_throw_percentage,\
	        total_rebounds, assists, steals, blocks, total_points]

def extract_one_tournament(tournament_folder):
	print("Extracting data in %s..." % tournament_folder)
	year = tournament_folder.split('-')[0]
	data_files = filter(lambda x: x.endswith('.html'), os.listdir(tournament_folder))
	data = [get_data_from_html(os.path.join(tournament_folder, data_file)) for data_file in data_files]
	print()
	df = pd.DataFrame(data, columns = get_headers())
	df.to_csv(assembled_data_format % year, index = False)

def extract_all_tournament_data():
	folders_to_analyze = filter(lambda x: x.endswith('-tournament-data'),
					            os.listdir())
	for tournament_folder in folders_to_analyze:
		extract_one_tournament(tournament_folder)

if __name__ == '__main__':
	extract_all_tournament_data()