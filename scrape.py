import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
mainurl = "https://locode.info"
exportfile = "locodeData.xlsx"
sleeptime = 2  ## delay in seconds between page requests


def getCountries(url):
    ## list for countries/urls
    countryPages = []

    ## get homepage to parse
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ## get all list items from page content
    lItems = soup.find_all("li")

    ## iterate list items to extract url & country
    for item in lItems[1:]:
        data = {"link": url + item.find("a")["href"], "country": item.find("a").text}
        countryPages.append(data)

    ## return data
    return countryPages


def getCountryCodes(country, codeurl, mainurl, cdata):
    print(f"Extract codes from {country}")

    ## get page to parse
    r = requests.get(codeurl, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    ## get all list items from page content
    lItems = soup.find_all("li")

    ## iterate list items to extract code & text
    for item in lItems[2:]:
        code = str(item.find("a")["href"]).replace("/", "")
        data = {
            "country": country,
            "code": code,
            "terminal": str(item.find("a").text).replace(code + ": ", ""),
            "link": f"{mainurl}/{code}",
        }
        ## append new data to passed list
        cdata.append(data)

    ## return updated list back out
    return cdata


## one list to hold all the data
countryData = []

## get main page countries
print(f"Opening {mainurl} and extracting countries")
countries = getCountries(mainurl)

## get each country url of data
for country in countries:
    countryData = getCountryCodes(
        country["country"], country["link"], mainurl, countryData
    )

    ## sleep to prevent hammering site
    time.sleep(sleeptime)


## export
print(f"Exporting data to excel file: {exportfile}")
df = pd.DataFrame(countryData)
df.to_excel(exportfile, index=False)
