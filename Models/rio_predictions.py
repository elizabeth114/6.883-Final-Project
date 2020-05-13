import convert_data
import time_series
import json
import datetime
import plot as myplot

from convert_data import create_and_predict
from time_series import load_athlete

result_list = []
index = 1
with open('../scraping/results.json') as json_file:
    data = json.load(json_file)[0]
    for athlete in data["athletes"]:
        olympic_date = datetime.datetime(2016, 8, 14)
        athlete_name = [athlete["first name"], athlete["last name"]]
        load_athlete(athlete_name, olympic_date)
        results = create_and_predict()
        myplot.plot_original_and_prediction(results, athlete_name)
        athlete_data = {"name": athlete_name,
                        "actual place": index,
                        "predicted place": 0,
                        "predicted distance": str(results[0][0])}
        result_list.append(athlete_data)
        index += 1
    index = 12
    error = 0

    for person in sorted(result_list, key = lambda athlete: float(athlete["predicted distance"])):
        error += (index-person["actual place"])**2
        person["predicted place"] = index
        index -= 1

    print(error)
    f = open("rio_predictions.json", "w")
    f.write(json.dumps(result_list, indent=4, sort_keys=True))
    f.close()
