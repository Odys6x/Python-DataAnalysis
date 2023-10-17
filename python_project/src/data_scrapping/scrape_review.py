import logging
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import scrape_method as sc
import sys
import streamlit.web.cli as stcli
from streamlit import runtime


def scraping():
    
    log_filename = '../log_message/scraping_log.txt'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Scraping started.")

    BASE_URL = "https://www.tripadvisor.com/"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    data = pd.read_csv("/data/raw/01 scrape_all_hotel/Refine.csv")
    scrape_links = data["Scrape_links"].tolist()

    count=0
    initial_delay = 5  # seconds
    response_time_threshold = 3  # seconds



    for index, link in enumerate(scrape_links):
        filename=data["Links"][index]
        full_url = BASE_URL + link
        start_time = time.time()  
        webpage = requests.get(full_url, headers=HEADERS)
        end_time = time.time()  
        response_time = end_time - start_time  

        if response_time < response_time_threshold:
            adjusted_delay = initial_delay + 1
        else:
            adjusted_delay = initial_delay

        time.sleep(adjusted_delay)

        soup = BeautifulSoup(webpage.content, "html.parser")

        d = {
            "Name": [],
            "Review_count": [],
            "Average_rating": [],
            "Overall_experience": [],
            "Rating": [],
            "Title": [],
            "Comment_content": [],
            "Date": [],
 
        }

        while True:
            try:
                for i in range(len(sc.get_reviewtitle(soup))):
                    d['Name'].append(sc.get_name(soup))
                    d['Title'].append(sc.get_reviewtitle(soup)[i])
                    d['Date'].append(sc.get_reviewdate(soup)[i])
                    d['Rating'].append(sc.get_rating(soup)[i])
                    d['Average_rating'].append(sc.get_average_rating(soup))
                    d['Comment_content'].append(sc.get_review(soup)[i])
                    d['Overall_experience'].append(sc.get_overall_exp(soup))
                    d['Review_count'].append(sc.get_review_count(soup))
                    
                count += 1
                print(f"Scraped data from hotel: {count} + {d['Name'][i]}")

                next_button = soup.find("a", class_="ui_button nav next primary")
                if next_button:
                    next_page_url = BASE_URL + next_button.get("href")
                    start_time = time.time()  
                    webpage = requests.get(next_page_url, headers=HEADERS)
                    end_time = time.time()  
                    response_time = end_time - start_time
                    soup = BeautifulSoup(webpage.content, "html.parser")
                else:
                    next_button_disabled = soup.find("a", class_="ui_button nav next primary disabled")
                    if next_button_disabled:
                        break  
                    else:
                        break
                
            except Exception as e:
                logging.error(f"Error: {str(e)}")

            df = pd.DataFrame.from_dict(d)
     
            csv_filename = f"../data/raw/02 individual_hotel/{filename}.csv"
            df.to_csv(csv_filename, mode='a', header=True, index=False)
            d = {
                "Name": [],
                "Review_count": [],
                "Average_rating": [],
                "Overall_experience": [],
                "Rating": [],
                "Title": [],
                "Comment_content": [],
                "Date": [],
                "Hotel_class": [],
                "Good_to_know": []
                }

if __name__ == "__scraping__":
    if runtime.exists():
        scraping()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
