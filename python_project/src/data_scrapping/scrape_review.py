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
    
    # Configure logging file
    log_filename = '../log_message/scraping_log.txt'
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Use logging to indicate the start of scraping
    logging.info("Scraping started.")

    # Define the base URL with a placeholder for the page number
    BASE_URL = "https://www.tripadvisor.com/"

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    data = pd.read_csv("/data/raw/01 scrape_all_hotel/Refine.csv")
    scrape_links = data["Scrape_links"].tolist()

    count=0
    # Define initial delay and response time threshold
    initial_delay = 5  # seconds
    response_time_threshold = 3  # seconds



    # Rest of your code for processing the link
    for index, link in enumerate(scrape_links):
        filename=data["Links"][index]
        full_url = BASE_URL + link
        start_time = time.time()  # Record the start time of the request
        webpage = requests.get(full_url, headers=HEADERS)
        end_time = time.time()  # Record the end time of the request
        response_time = end_time - start_time  # Calculate the response time

        if response_time < response_time_threshold:
            # If the server responds quickly, increase the delay slightly
            adjusted_delay = initial_delay + 1
        else:
            # If the server responds slowly, keep the delay the same
            adjusted_delay = initial_delay

        # Apply the adjusted delay before the next request
        time.sleep(adjusted_delay)

        soup = BeautifulSoup(webpage.content, "html.parser")

        # Initialize the dictionary for each hotel
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

                # Check if there's a "Next" button for pagination
                next_button = soup.find("a", class_="ui_button nav next primary")
                if next_button:
                    next_page_url = BASE_URL + next_button.get("href")
                    start_time = time.time()  # Record the start time of the request
                    webpage = requests.get(next_page_url, headers=HEADERS)
                    end_time = time.time()  # Record the end time of the request
                    response_time = end_time - start_time  # Calculate the response time
                    soup = BeautifulSoup(webpage.content, "html.parser")
                else:
                    # Check for the "disabled" class to determine if there are no more pages
                    next_button_disabled = soup.find("a", class_="ui_button nav next primary disabled")
                    if next_button_disabled:
                        break  # No more pages to scrape
                    else:
                        # If "disabled" class is not present but "Next" button is missing, break to avoid an infinite loop
                        break
                
            except Exception as e:
                logging.error(f"Error: {str(e)}")

            df = pd.DataFrame.from_dict(d)
     
            # Save the data to a CSV file after each hotel page is scraped 
            csv_filename = f"../data/raw/02 individual_hotel/{filename}.csv"
            df.to_csv(csv_filename, mode='a', header=True, index=False)
            # Clear the dataframe
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
