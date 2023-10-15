import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import scrape_method as sc
import time as t
import sys
import streamlit.web.cli as stcli
from streamlit import runtime
# Define the base URL with a placeholder for the page number
base_url = "https://www.tripadvisor.com/Hotels-g294265-oa{}-Singapore-Hotels.html"

# Define the range of page numbers to scrape
start_page = 30
end_page = 840

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Create an empty list to store the scraped data
all_data = []

def scrape_hotel():
    
    # Iterate over the range of page numbers
    for page in range(start_page, end_page +1, 30):
        # Construct the URL with the current page number
        url = base_url.format(page)
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
    
        links = soup.find_all("a", attrs={'class': 'BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS'})
        links_list = []

        for link in links:
            links_list.append(link.get('href'))

        d = {"Name": [], "Address": [], "Price": [], "Amenities": [], 'Hotel_ratings': [], 'Description': [],
         'Near_Restaurant': [], 'Near_Attractions': [], "Hotel_class": [],
            "Good_to_know": []}

        count = 0
        for link in links_list:
            new_link = requests.get("https://www.tripadvisor.com/" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_link.content, "html.parser")
            d['Name'].append(sc.get_name(new_soup))
            d['Address'].append(sc.get_address(new_soup))
            d['Price'].append(sc.get_price(new_soup))
            d['Amenities'].append(sc.get_amenities(new_soup))
            d['Hotel_ratings'].append(sc.hotel_rating(new_soup))
            d['Description'].append(sc.descrip(new_soup))
            d['Near_Restaurant'].append(sc.get_near_Restaurant(new_soup))
            d['Near_Attractions'].append(sc.get_near_attr(new_soup))
            d['Hotel_class'].append(sc.get_hotel_class(soup))
            d['Good_to_know'].append(sc.get_overall_details(soup))
            
            count += 1
        
            print(f"Scraped data from page {page}, hotel {count},{t.ctime()}")


        # Convert the dictionary to a DataFrame
        df = pd.DataFrame.from_dict(d)
        # Drop rows where the "Address" column is "None"
        df = df[df['Address'] != 'None']
        # Remove duplicate rows
        df = df.drop_duplicates()

        # Append the DataFrame to the all_data list
        all_data.append(df)

    # Concatenate all DataFrames in the list into one DataFrame
    final_df = pd.concat(all_data, ignore_index=True)

    # Do further processing or analysis on the DataFrame as needed
    print(final_df)

    # Save the cleaned data to a CSV file named "Hotel_30_855.csv"
    final_df.to_csv("../data/raw/01 scrape_all_hotel/Hotel_30_840.csv", header=True, index=False)

if __name__ == "__scrape_hotel__":
    if runtime.exists():
        scrape_hotel()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
