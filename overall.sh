#! /usr/bin/env bash
./get_tournament_structure_data.py delete-cache
./analyze_tournament_structure.py
./generate_tournament_results.py
./scrape_team_data.py delete-cache