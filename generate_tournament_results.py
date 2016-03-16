#! /usr/bin/env python3

import os, os.path

tournament_structure_folder = "tournament-structure"

tournament_results_folder = "tournament-results"
tournament_results_format = "%s_real_results.txt"


def generate_results_for_one_tournament(tournament_listing_file):
	f = open(tournament_listing_file, 'r')
	teams = [[line.split(';')[0], line.strip().split(';')[2]] for line in f.readlines()]
	f.close()
	teams = [[team[0], [int(score) for score in team[1].split(',')]] for team in teams]
	rounds = [teams]
	while len(rounds[-1]) != 1:
		new_teams = []
		current_teams = rounds[-1]
		for i in range(len(current_teams)):
			if i % 2 == 0:
				(team_one, score_one, future_scores_one) = (current_teams[i][0], current_teams[i][1][0], current_teams[i][1][1:])
				(team_two, score_two, future_scores_two) = (current_teams[i + 1][0], current_teams[i + 1][1][0], current_teams[i + 1][1][1:])
				if score_one > score_two:
					new_teams.append((team_one, future_scores_one))
				else:
					new_teams.append((team_two, future_scores_two))
		rounds.append(new_teams)
	year = tournament_listing_file.split("/")[1].split("_")[0]
	if not os.path.isdir(tournament_results_folder):
		os.system("mkdir %s" % tournament_results_folder)
	out = open(os.path.join(tournament_results_folder, tournament_results_format % year), 'w')
	for round_result in rounds:
		team_for_round = [team_info[0] for team_info in round_result]
		out.write(', '.join(team_for_round))
		out.write("\n")
	out.close()

def generate_results_for_all_tournaments():
	files_to_analyze = filter(lambda x: x.endswith('_listing.txt'),
					          os.listdir(tournament_structure_folder))
	for tournament in files_to_analyze:
		print('Generating results for %s' % tournament)
		generate_results_for_one_tournament(os.path.join(tournament_structure_folder, tournament))

if __name__ == '__main__':
	generate_results_for_all_tournaments()