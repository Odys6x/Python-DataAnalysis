import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import scrape_method as sc
import time as t
import sys
import streamlit.web.cli as stcli
import os
from streamlit import runtime

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

base_url = "https://www.tripadvisor.com/Hotels-g294265-oa{}-Singapore-Hotels.html"

start_page = 30
end_page = 840

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}

all_data = []


def scrape_hotel():
    """
    Scrapes hotel data from multiple pages of TripAdvisor, including hotel names, addresses, prices, amenities,
    ratings, descriptions, nearby restaurants and attractions, hotel classes, and other details. The scraped data
    is stored in a CSV file named 'Hotel_List.csv' in the '../data/raw/' directory.

    Note:
    - The scraping starts from page 1 and continues until page 840 (last page) (in increments of 30).
    - The HEADERS simulate a user-agent for making web requests.
    - The 'scrape_method' module is assumed to contain scraping functions (not shown here).



    Example usage:
    If this script is executed directly, it will scrape hotel data and save it to 'Hotel_List.csv'.
    """

    for page in range(start_page, end_page + 1, 30):
        url = base_url.format(page)
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        links = soup.find_all(
            "a", attrs={"class": "BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS"}
        )
        links_list = []

        for link in links:
            links_list.append(link.get("href"))

        d = {
            "Name": [],
            "Address": [],
            "Price": [],
            "Amenities": [],
            "Hotel_ratings": [],
            "Description": [],
            "Near_Restaurant": [],
            "Near_Attractions": [],
            "Hotel_class": [],
            "Good_to_know": [],
        }

        count = 0
        for link in links_list:
            new_link = requests.get(
                "https://www.tripadvisor.com/" + link, headers=HEADERS
            )
            new_soup = BeautifulSoup(new_link.content, "html.parser")
            d["Name"].append(sc.get_name(new_soup))
            d["Address"].append(sc.get_address(new_soup))
            d["Price"].append(sc.get_price(new_soup))
            d["Amenities"].append(sc.get_amenities(new_soup))
            d["Hotel_ratings"].append(sc.hotel_rating(new_soup))
            d["Description"].append(sc.descrip(new_soup))
            d["Near_Restaurant"].append(sc.get_near_Restaurant(new_soup))
            d["Near_Attractions"].append(sc.get_near_attr(new_soup))
            d["Hotel_class"].append(sc.get_hotel_class(soup))
            d["Good_to_know"].append(sc.get_overall_details(soup))

            count += 1

            print(f"Scraped data from page {page}, hotel {count},{t.ctime()}")

        df = pd.DataFrame.from_dict(d)
        df = df[df["Address"] != "None"]
        df = df.drop_duplicates()

        all_data.append(df)

    final_df = pd.concat(all_data, ignore_index=True)

    print(final_df)

    final_df.to_csv("../../data/raw/Hotel_List.csv", header=True, index=False)


if __name__ == "__scrape_hotel__":
    if runtime.exists():
        scrape_hotel()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
