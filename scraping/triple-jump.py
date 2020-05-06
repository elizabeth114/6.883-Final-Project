from lxml import html
import requests
import json
import csv
import sys

base_url = "https://www.olympic.org/"
url_options = ["rio-2016", "london-2012", "beijing-2008", "athens-2004", "sydney-2000", "atlanta-1996"]
url_end = "/athletics/triple-jump-women"
#
# for year in url_options:

games = []
for year in url_options:
	url = base_url + year + url_end
	game = {"year": year,
			"athletes": []}
	response = requests.get(url)
	tree = html.document_fromstring(response.text)
	athletes = []
	for index, person in enumerate(tree.xpath("//div[@class='main-holder']")[0].xpath("//div[@class='profile-section']")):
		info = person.text_content().strip().split("\n")
		split_name = info[0][:-1].split()
		first = split_name[0]
		last = " ".join(split_name[1:])
		athlete = {
		"first name": first,
		"last name" : last,
		"games": year,
		"country": info[-1][-3:],
		"distance": person.xpath("//td[@class='col3']")[index].text_content()[2:7]
		}
		game["athletes"].append(athlete)
		if index==11:
			break

	games.append(game)
f = open("results.json", "w")
f.write(json.dumps(games, indent=4, sort_keys=True))
f.close()
