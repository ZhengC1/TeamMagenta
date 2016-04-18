# @version 3.4
# @date 3/2/2016
# Massey Brackets
# This file gives you which stats fare the best
# in predicting the winner. 

import numpy as np
import json
import sys
list_keys = ["freethrow","3shooting","shooting","ftm", "dreb", "ast", "stl", "fgm", "fga", "oreb", "to", "reb", "fta", "3pa", "pts", "blk", "pf", "3pm"]
display_keys = ["freethrow","3shooting","shooting", "dreb", "ast", "stl", "oreb", "to", "reb",  "pts", "blk", "pf", ]
teams = {}
#inverse team - assign number to team.
inv_teams = {}

# creates a dictionary of the teams from data
def get_teams(data):
	for game in data:
		teams.setdefault(game['home']['team'], len(teams))
	inv_teams = {v: k for k, v in teams.items()}

def main(args):
    # opens file, loads data from games
	with open(args[1]) as data_file:
		games = json.load(data_file)

	get_teams(games)

    # creates the m matrix(games * teams)
	m = {}
	r = {}
	y = {}
	num_y = {}
	num_m = {}
	for key in list_keys:
		y[key] = []
		r[key] = []
		m[key] = []

	equation = {}
	for game in games:
		row = [0] * len(teams)
		row[teams[game['home']['team']]] = 1
		row[teams[game['away']['team']]] = -1

		for key in list_keys:
			try:
				if key == "shooting":
					equation[key] = (game['home']['fgm'] / game['home']['fga']) - (game['away']['fgm'] / game['away']['fga'])
				elif key == "3shooting":
					equation[key] = (game['home']['3pm'] / game['home']['3pa']) - (game['away']['3pm'] / game['away']['3pa'])
				elif key == "freethrow":
					try:
                                                equation[key] = (game['home']['ftm'] / game['home']['fta']) - (game['away']['ftm'] / game['away']['fta'])
					except ZeroDivisionError:
						print ("Zero error")
				else:
					equation[key] = game['home'][key] - game['away'][key]
			except KeyError:
				print ("Keyerror2")

		for key in list_keys:
			try:
				y[key].append(equation[key])
				m[key].append(row)
			except KeyError:
				print ("error")

	for key in list_keys:
		m[key].append([1] * len(teams))

	# Calcuates matrix for each different stat
	for key in y:
		try:
			y[key].append(0)
			num_m[key] = np.array(m[key])
			num_y[key] = np.array(y[key])
			print(len(num_m),len(num_y[key]))
			r[key] = np.linalg.lstsq(num_m[key], num_y[key])[0]
		except KeyError:
			print ("error")
		print (r[key])

        # adds homecourt advantage
        # A - B + h = Sa - Sb
        # Add column of 1s to m for homecourt advantage * A B C H = y
	for key in list_keys:
		for row in m[key][:-1]:
			row.append(1)
		m[key][-1].append(0)

	num_m = np.array(m)
	num_y = np.array(y)

        # print(np.dot(m.T, m))
        # print(np.dot(m.T, y))
	#r = np.linalg.lstsq(num_m, num_y)[0]
	'''
	sorted_list  = []
	for i in range(len(r) -1) :
		sorted_list.append((r[i],inv_teams[i]))
	sorted_list = sorted(sorted_list,reverse=True)

	for (rating,team) in sorted_list:
		print(team,"\t",rating)
	'''

	rate_matchup(r)





def cmp_teams(team1,team2,rating,stat):
	difference = ((rating[stat][team1] - rating[stat][team2]) / ((rating[stat][team1] + rating[stat][team2])/2))
	print (difference)
	return difference

def rate_matchup(ratings):

	while 1:
		t1 = "a"
		t2 = "a"
		team1 = input("Team 1:")
		for team in teams:
			if (team1 in team):
				print (team)
				t1 = teams[team]

		team2 = input("Team 2:")
		for team in teams:
			if (team2 in team):
				print (team)
				t2 = teams[team]

		for key in display_keys:
			#for i,item in enumerate(r[key]):
                        #print (item,)
			try:
				print(key)
				print ("Key: ", r[key][t1], r[key][t2])
			except KeyError:
				print("Team not found")

		matchup = (0.33 * cmp_teams(t1,t2,r,'reb')) + (0.33 * cmp_teams(t1,t2,r,'shooting')) - (.33 * cmp_teams(t1,t2,'to'))
		print (matchup)

if __name__ == '__main__':
	main(sys.argv)
