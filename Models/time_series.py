import json
import csv
import datetime
from datetime import timedelta

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
                    fieldnames = ['date', 'distance']#, 'mos_since_oly']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    data = []
                    for year in athlete["results by year"]:
                        for result in year["results"]:
                            date = result["date"]
                            year_value = int(year["year"])
                            month_value = months[date[3:6].lower()]
                            if year_value % 4 > 0:
                                last_olympics_year = year_value - (year_value % 4)
                            else:
                                last_olympics_year = year_value if month_value > 8 else (year_value - 4) # olympics mid-August
                            date = datetime.datetime(year_value, months[date[3:6].lower()], int(date[:2]))
                            mos_since_last_olympics = (year_value - last_olympics_year) * 12 + (month_value - 8)
                            if date <   olympic_date:
                                data.append({'date': date, 'distance': float(result["result"])})#, 'mos_since_oly': mos_since_last_olympics})
                    data = sorted(data, key = lambda dic: dic["date"])
                    writer.writerows(data)
                    print("loaded ", athlete["first name"], " ", athlete["last name"], "\'s data")
                    break

def load_athlete_only_years_before(athlete_name, olympic_date, previous_oly_date):
    with open('../scraping/general_results.json') as json_file:
        data = json.load(json_file)
        for athlete in data:
            if athlete["first name"].lower() == athlete_name[0].lower() and athlete["last name"].lower() == athlete_name[1].lower():
                data = []
                for year in athlete["results by year"]:
                    for result in year["results"]:
                        date = result["date"]
                        year_value = int(year["year"])
                        month_value = months[date[3:6].lower()]
                        date = datetime.datetime(year_value, month_value, int(date[:2]))
                        if date > previous_oly_date and date < olympic_date:
                            data.append({'date': date, 'distance': float(result["result"])})
                data = sorted(data, key = lambda dic: dic["date"])
                data = [d['distance'] for d in data]
                return data
