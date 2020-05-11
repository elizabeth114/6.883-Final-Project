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
with open('../scraping/general_results.json') as json_file:
    with open("csv_dates.csv", 'w', newline='') as csvfile:
        fieldnames = ['date', 'distance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        data = json.load(json_file)
        print(data[0]["first name"])
        for year in data[0]["results by year"]:
            print(year)
            for result in year["results"]:
                date = result["date"]
                date = datetime.datetime(int(year["year"]), months[date[3:6].lower()], int(date[:2]))
                writer.writerow({'date': date, 'distance': float(result["result"])})
