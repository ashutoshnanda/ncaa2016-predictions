#! /usr/bin/env python3

from bs4 import BeautifulSoup
import os, os.path

tournament_structure_folder = "tournament-structure"
listing_format = "%s_listing.txt"

def parse_team_and_score(element, seed = None, final = False):
	team_name = element.findChildren('a', {'class' : ''})[0].text
	if final:
		return team_name
	team_score = element.findChildren('a', {'class' : 'bold_text'})[0].text
	if seed:
		return (team_name, seed, team_score)
	else:
		return (team_name, team_score)

def extract_teams(region):
	sixteen_teams = [None for filler in range(16)]
	eight_teams = [None for filler in range(8)]
	four_teams = [None for filler in range(4)]
	two_teams = [None for filler in range(2)]
	region_winner = None
	for i, seed in enumerate(region.findChildren('td', {'class' : 'seed'})):
		team = list(filter(lambda x: 'rowspan' not in x.attrs,
				           seed.parent.findChildren('td', {'class' : ''})))
		if len(team) != 1:
			print(team)
			print("Ambiguous!")
			exit()
		sixteen_teams[i] = parse_team_and_score(team[0], seed = seed.text)
	for i, first_round_winner in enumerate(region.findChildren('td', {'rowspan' : '2'})):
		eight_teams[i] = parse_team_and_score(first_round_winner)
	for i, second_round_winner in enumerate(region.findChildren('td', {'rowspan' : '5'})):
		four_teams[i] = parse_team_and_score(second_round_winner)
	for i, sweet_sixteen_winner in enumerate(region.findChildren('td', {'rowspan' : '11'})):
		two_teams[i] = parse_team_and_score(sweet_sixteen_winner)
	for i, elite_eight_winner in enumerate(region.findChildren('td', {'rowspan' : '23'})):
		region_winner = parse_team_and_score(elite_eight_winner, final = True)
	final_value = [sixteen_teams, eight_teams, four_teams, two_teams, region_winner]
	return final_value

def extract_final_four(final_four):
	final_four_teams = [None for filler in range(4)]
	national_finalist_teams = [None for filler in range(2)]
	national_winner = None
	final_four_search = filter(lambda x: 'rowspan' not in x.attrs,
							   final_four.findChildren('td', {'class' : ''}))
	for i, final_four_team in enumerate(final_four_search):
		final_four_teams[i] = parse_team_and_score(final_four_team)
	for i, national_finalist_team in enumerate(final_four.findChildren('td', {'rowspan' : '2'})):
		national_finalist_teams[i] = parse_team_and_score(national_finalist_team)
	for i, national_winner_team in enumerate(final_four.findChildren('td', {'rowspan' : 5})):
		national_winner = parse_team_and_score(national_winner_team, final = True)
	final_value = [final_four_teams, national_finalist_teams, national_winner]
	return final_value

def find_regions(soup):
	bracket_area = soup.find(id = "page_content")
	regions = [x.text.replace(' ', '').replace('.', '') for x in bracket_area.findChildren('div')[0].findChildren('span')]
	return regions[2:-1]

def analyze_one_tournament(tournament_structure_file):
	print('Analyzing %s' % tournament_structure_file)
	year = tournament_structure_file.split("_")[0]
	f = open(tournament_structure_file)
	soup = BeautifulSoup(f.read(), "html.parser")
	f.close()
	region_ids = find_regions(soup)
	regions = [soup.find(id = region_id) for region_id in region_ids]
	region_teams = [extract_teams(x) for x in regions]
	final_id = "National"
	final_four = soup.find(id = final_id)
	finals = extract_final_four(final_four)
	order = {i : None for i in range(4)}
	for i, (team_name, team_score) in enumerate(finals[0]):
		for j, (region_id, set_of_teams) in enumerate(zip(region_ids, region_teams)):
			if team_name in [first_round_team_info[0] for first_round_team_info in set_of_teams[0]]:
				order[i] = (j, region_id)
				break
	out_data = [None for filler in range(64)]
	count = 0
	for key in order:
		(index, region_id) = order[key]
		for team in region_teams[index][0]:
			team_name = team[0]
			seed = team[1]
			should_continue = True
			scores = []
			for i, round_info in enumerate(region_teams[index]):
				if not should_continue:
					break
				if i == len(region_teams[index]) - 1:
					continue
				team_names = [x[0] for x in round_info]
				team_index = -1 if team_name not in team_names else team_names.index(team_name)
				if team_index == -1:
					should_continue = False
				else:
					scores.append(round_info[team_index][-1])
			for i, round_info in enumerate(finals):
				if not should_continue:
					break
				if i == len(finals) - 1:
					continue
				team_names = [x[0] for x in round_info]
				team_index = -1 if team_name not in team_names else team_names.index(team_name)
				if team_index == -1:
					should_continue = False
				else:
					scores.append(round_info[team_index][-1])
			out_data[count] = [team_name, seed, ','.join(scores)]
			count += 1
	listing_file = open(listing_format % year, 'w')
	for data in out_data:
		listing_file.write(';'.join(data))
		listing_file.write('\n')
	listing_file.close()

def analyze_all_tournaments():
	files_to_analyze = filter(lambda x: x.endswith('.html') and '2016' not in x,
					          os.listdir(tournament_structure_folder))
	for tournament in files_to_analyze:
		analyze_one_tournament(os.path.join(tournament_structure_folder, tournament))

if __name__ == '__main__':
	analyze_all_tournaments()