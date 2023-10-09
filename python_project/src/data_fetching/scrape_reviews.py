import scrape_method as sc
import time as t
import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import time

# Configure logging file
log_filename = 'scraping_log.txt'
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Use logging to indicate the start of scraping
logging.info("Scraping started.")

# Rest of your code

# Define the base URL with a placeholder for the page number
BASE_URL = "https://www.tripadvisor.com/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

data = pd.read_csv(
    "Refine.csv")

alllinks = data["Links"].tolist()

# Define initial delay and response time threshold
initial_delay = 5  # seconds
response_time_threshold = 3  # seconds

for link in alllinks[199:200]:
    count = 0
    full_url = BASE_URL + link
    print(full_url)
    start_time = time.time()  # Record the start time of the request
    webpage = requests.get(full_url, headers=HEADERS)
    end_time = time.time()  # Record the end time of the request
    response_time = end_time - start_time  # Calculate the response time

    if response_time < response_time_threshold:
        # If the server responds quickly, increase the delay
        adjusted_delay = initial_delay * 2 + 1
    else:
        adjusted_delay = initial_delay

    # Apply the adjusted delay before the next request
    t.sleep(adjusted_delay)

    soup = BeautifulSoup(webpage.content, "html.parser")

    d = {"Name": [], "Review_count": [], "Average_rating": [], "Overall_experience": [], "Rating": [], "Title": [],
         "Comment_content": [], "Date": [], "Hotel_class": [], "Good_to_know": []}

    while True:
        try:
            for i in range(len(sc.get_reviewtitle(soup))):
                # for i in range():

                d['Name'].append(sc.get_name(soup))
                d['Title'].append(sc.get_reviewtitle(soup)[i])
                d['Date'].append(sc.get_reviewdate(soup)[i])
                d['Rating'].append(sc.get_rating(soup)[i])
                d['Average_rating'].append(sc.get_average_rating(soup))
                d['Comment_content'].append(sc.get_review(soup)[i])
                d['Overall_experience'].append(sc.get_overall_exp(soup))
                d['Review_count'].append(sc.get_review_count(soup))
                d['Hotel_class'].append(sc.get_hotel_class(soup))
                d['Good_to_know'].append(sc.get_overall_details(soup))

                count += 1
                print(f"Scraped data from hotel: {count} {t.ctime()}")

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
                next_button_disabled = soup.find(
                    "a", class_="ui_button nav next primary disabled")
                if next_button_disabled:
                    break  # No more pages to scrape
                else:
                    # If "disabled" class is not present but "Next" button is missing, break to avoid an infinite loop
                    break

        except Exception as e:
            logging.error(f"Error: {str(e)}")

        df = pd.DataFrame.from_dict(d)

        # Save the data to a CSV file after each link is scraped
        csv_filename = "rev.csv"
        # df.to_csv(csv_filename, header=True, index=False)
        df.to_csv(csv_filename, mode='a', header=False, index=False)
        # Clear the dictionary for the next hotel
        d = {"Name": [], "Review_count": [], "Average_rating": [], "Overall_experience": [], "Rating": [], "Title": [],
             "Comment_content": [], "Date": [], "Hotel_class": [], "Good_to_know": []}
