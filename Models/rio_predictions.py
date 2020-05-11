import convert_data
import time_series
import json
import datetime

from convert_data import do_the_stuff
from time_series import load_athlete

result_dict = []
index = 1
with open('../scraping/results.json') as json_file:
    data = json.load(json_file)[0]
    for athlete in data["athletes"]:
        olympic_date = datetime.datetime(2016, 8, 14)
        athlete_name = [athlete["first name"], athlete["last name"]]
        load_athlete(athlete_name, olympic_date)
        results = do_the_stuff()
        result_dict.append((index, " ".join(athlete_name), results[0][0]))
        index += 1

    print(sorted(result_dict, key = lambda element : element[2]))
