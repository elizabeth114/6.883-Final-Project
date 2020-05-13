import convert_data
import time_series
import json
import datetime
import plot as myplot
# from numpy import array
from numpy import concatenate

from convert_data import do_the_stuff, do_the_stuff_one_net
from time_series import load_athlete, load_athlete_only_years_before

result_list = []
index = 1

oly_dates = {"2016": datetime.datetime(2016, 8, 14),
            "2012": datetime.datetime(2012, 8, 5),
            "2008": datetime.datetime(2008, 8, 17),
            "2004": datetime.datetime(2004, 8, 23),
            "2000": datetime.datetime(2000, 9, 24),
            "1996": datetime.datetime(1996, 7, 31),
            "1992": datetime.datetime(1992, 1, 1)} # added 1992 fake date

with open('../scraping/olympic_results.json') as json_file:
    x_data = []
    y_data = []
    test_x = []
    test_y = []
    oly_data = json.load(json_file)
    max_length = 0
    for oly in oly_data:
        for athlete in oly["athletes"]:
            olympic_date = oly_dates[oly["year"][-4:]]
            athlete_name = [athlete["first name"], athlete["last name"]]
            previous_oly_date = oly_dates[str(int(oly["year"][-4:])-4)]
            loaded_data = load_athlete_only_years_before(athlete_name, olympic_date, previous_oly_date)
            if loaded_data is None or len(loaded_data) == 0:
                continue
            try:
                if oly["year"][-4:] == "2016":
                    # test_y.append(array(float(athlete["distance"])))
                    # test_x.append(array(loaded_data))
                    test_y.append(float(athlete["distance"]))
                    test_x.append(loaded_data)
                else:
                    # y_data.append(array(float(athlete["distance"])))
                    # x_data.append(array(loaded_data))
                    y_data.append(float(athlete["distance"]))
                    x_data.append(loaded_data)
                if len(loaded_data) > max_length:
                    max_length = len(loaded_data)
            except ValueError:
                continue

    # add padding with minimum distance at beginning of lists
    for i in range(len(x_data)):
        if len(x_data[i]) < max_length:
            x_data[i] = concatenate([(max_length-len(x_data[i]))*[min(x_data[i])],x_data[i]])
    for i in range(len(test_x)):
        if len(test_x[i]) < max_length:
            test_x[i] = concatenate([(max_length-len(test_x[i]))*[min(test_x[i])],test_x[i]])
    print("loaded all athletes")
    results = do_the_stuff_one_net(x_data, y_data, test_x)

    result_list = []
    rio_data = oly_data[0]["athletes"]
    for index in range(len(rio_data)):
        athlete = rio_data[index]
        athlete_name = [athlete["first name"], athlete["last name"]]
        athlete_data = {"name": athlete_name,
                        "actual place": index+1,
                        "predicted place": 0,
                        "predicted distance": str(results[index][0])}
        result_list.append(athlete_data)
    index = 12
    error = 0
    for person in sorted(result_list, key = lambda athlete: float(athlete["predicted distance"])):
        error += (index-person["actual place"])**2
        person["predicted place"] = index
        index -= 1
    print(error)

    f = open("rio_predictions_one_net.json", "w")
    f.write(json.dumps(result_list, indent=4, sort_keys=True))
    f.close()
