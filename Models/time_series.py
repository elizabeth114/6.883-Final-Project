import json
import csv
import datetime

months = {"jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12}

def load_athlete(athlete_name, olympic_date):
    with open('../scraping/general_results.json') as json_file:
        with open("csv_dates.csv", 'w', newline='') as csvfile:
            data = json.load(json_file)
            for athlete in data:
                if athlete["first name"].lower() == athlete_name[0].lower() and athlete["last name"].lower() == athlete_name[1].lower():
                    fieldnames = ['date', 'distance']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    data = []
                    for year in athlete["results by year"]:
                        for result in year["results"]:
                            date = result["date"]
                            date = datetime.datetime(int(year["year"]), months[date[3:6].lower()], int(date[:2]))
                            if date <   olympic_date:
                                data.append({'date': date, 'distance': float(result["result"])})
                    data = sorted(data, key = lambda dic: dic["date"])
                    writer.writerows(data)
                    print("loaded ", athlete["first name"], " ", athlete["last name"], "\'s data")
                    break
