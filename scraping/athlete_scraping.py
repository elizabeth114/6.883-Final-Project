from lxml import html
import requests
import json
import csv
import sys

#['Qiuyan HUANG', 'Cristina Elena NICOLAU']
#No profiles on world athletics for girls listed above

class Gsearch_python:
   def __init__(self,name_search):
      self.name = name_search
   def Gsearch(self):
      count = 0
      try :
         from googlesearch import search
      except ImportError:
         print("No Module named 'google' Found")
      for i in search(query=self.name,tld='co.in',lang='en',num=10,stop=10,pause=10):
         count += 1
         if "worldathletics.org/athletes" in i:
            return i

found_athletes = set()
base_url = "http://api.scraperapi.com?api_key=da6856bde4ae33e54a9356a16aea2213&url="
world_athletics = "world athletics"

error_athletes = []
with open('results.json') as json_file:
   data = json.load(json_file)
   rio = data[0]
   all_athletes = []
   for games in data:
      all_athletes += games["athletes"]

   all_results = []
   for athlete in all_athletes:
      athlete_results = {"first name": athlete["first name"],
                    "last name": athlete["last name"],
                    "results by year": []}
      athlete_name = athlete["first name"] + " " + athlete["last name"]
      if athlete_name not in found_athletes:
         found_athletes.add(athlete_name)
         try:
            url = base_url + Gsearch_python(world_athletics + " " + athlete["first name"] + " " + athlete["last name"]).Gsearch()
            # url = base_url + search_url_start + athlete_name + search_url_end
            # url = base_url + "https://worldathletics.org/athletes/colombia/caterine-ibarguen-170921"
            response = requests.get(url)
            tree = html.document_fromstring(response.text)
            get_id = tree.xpath("//span[@class='_label _label--athlete-id']")[0].text_content().split()
            id = "0" + get_id[-1]

            years = ["1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016"]
            url_start = "https://www.worldathletics.org/data/GetCompetitorResultsByYearHtml?resultsByYear="
            url_end = "&resultsByYearOrderBy=discipline&aaId="
            # id = "014263994"
            all_years = athlete_results["results by year"]
            for year in years:
               url = base_url + url_start + year + url_end + id
               year_results = {"year": year,
                               "results": []}
               response = requests.get(url)
               tree = html.document_fromstring(response.text)
               events = tree.xpath("//div[@class='results-by-event-wrapper results-wrapper']")

               dates = tree.xpath("//td[@data-th='Date']")
               results = tree.xpath("//td[@data-th='Result']")
               # wind = tree.xpath("//td[@data-th='Wind']")
               for index in range(len(dates)):
                  try:
                     if 10 < float(results[index].text_content().strip()) and 20> float(results[index].text_content().strip()):
                        single_result = {"result": results[index].text_content().strip(), "date": dates[index].text_content().strip()}
                        year_results["results"].append(single_result)
                  except:
                     print("error")

               all_years.append(year_results)
            all_results.append(athlete_results)
         except:
            error_athletes.append(athlete_name)

   f = open("athlete_results.json", "w")
   f.write(json.dumps(all_results, indent=4, sort_keys=True))
   f.close()
   print(error_athletes)
