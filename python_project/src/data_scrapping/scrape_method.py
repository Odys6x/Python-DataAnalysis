import re


def get_name(soup):
    """
    Extracts and returns the name of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: The name of the hotel.
    """
    try:
        title = soup.find("h1", attrs={"id": "HEADING"})

        title_value = title.text

        title_string = title_value.strip()

    except AttributeError:
        title_string = " "

    return title_string


def get_address(soup):
    """
    Extracts and returns the address of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: The address of the hotel.
    """
    try:
        title = soup.find("span", attrs={"class": "oAPmj _S"}).text.strip()

    except:
        title = "None"

    return title


def get_price(soup):
    """
    Extracts and returns the price information of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: The price information of the hotel.
    """
    try:
        price = str(soup.find("div", attrs={"class": "gbXAQ"}).text.strip())

    except:
        price = "None"

    return price


def get_amenities(soup):
    """
    Extracts and returns a string containing the amenities of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: A comma-separated string of amenities.
    """
    amen = []
    amenstr = ""

    try:
        for div in soup.find_all("div", attrs={"class": "OsCbb K"}):
            for Sdiv in soup.find_all("div", attrs={"class": "yplav f ME H3 _c"}):
                amen.append(Sdiv.text.strip())

        for i in amen:
            amenstr = amenstr + i + ", "

    except:
        amenstr = "None"

    return amenstr


def hotel_rating(soup):
    """
    Extracts and returns the rating of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: The rating of the hotel.
    """
    try:
        ratings = soup.find_all("svg", attrs={"class": "UctUV d H0 hzzSG"})
        ratings = ratings[0].get("aria-label")

        new_ratings = ratings[:3]

    except:
        new_ratings = "None"

    return new_ratings


def descrip(soup):
    """
    Extracts and returns the description of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: The description of the hotel.
    """
    try:
        desc = soup.find("div", attrs={"class": "fIrGe _T"}).text.strip()

    except:
        desc = "None"
    return desc


def get_near_Restaurant(soup):
    """
    Extracts and returns information about nearby restaurants from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: Information about nearby restaurants.
    """
    res = []
    restr = ""
    try:
        for Sdiv in soup.find_all("div", attrs={"class": "hpjtb"}):
            res.append(Sdiv.text.strip())
    except:
        restr = "None"

    for ele in res:
        restr += ele
    return restr


def get_near_attr(soup):
    """
    Extracts and returns information about nearby attractions from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        str: Information about nearby attractions.
    """
    atr = []
    atrr = ""
    try:
        for Sdiv in soup.find_all("div", attrs={"class": "hpjtb"}):
            atr.append(Sdiv.text.strip())

    except:
        atrr = "None"

    for ele in atr:
        atrr += ele
    return atrr


def get_name(soup):
    """
    Extracts and returns the review dates of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        list: A list of review dates.
    """
    try:
        title = soup.find("h1", attrs={"id": "HEADING"})

        title_value = title.text

        title_string = title_value.strip()

    except AttributeError:
        title_string = " "

    return title_string


def get_reviewdate(soup):
    """
    Extracts and returns the titles of the reviews of a hotel from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
        list: A list of review titles.
    """
    allreviewsdate = []
    try:
        for review in soup.find_all("span", attrs={"class": "teHYY _R Me S4 H3"}):
            allreviewsdate.append(review.text.strip())

    except AttributeError:
        allreviewsdate = "None"

    return allreviewsdate


def get_reviewtitle(soup):
    """
    Extracts and returns the titles of reviews from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the review information.

    Returns:
    list: A list of review titles or "None" if not found.
    """
    alltitle = []
    try:
        for div in soup.find_all("div", attrs={"class": "KgQgP MC _S b S6 H5 _a"}):
            alltitle.append(div.text.strip())

    except AttributeError:
        alltitle = "None"

    return alltitle


def get_review(soup):
    """
    Extracts and returns the contents of reviews from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the review information.

    Returns:
    list: A list of review contents or "None" if not found.
    """
    allReview = []
    try:
        for div in soup.find_all("span", attrs={"class": "QewHA H4 _a"}):
            allReview.append(div.text.strip())

    except AttributeError:
        allReview = "None"

    return allReview


def get_rating(soup):
    """
    Extracts and returns the ratings of reviews from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the review information.

    Returns:
    list: A list of review ratings or None if not found.
    """
    allRatings = []
    try:
        rating_elements = soup.find_all("div", class_="Hlmiy F1")

        for element in rating_elements:
            rating_span = element.find(
                "span", class_=re.compile(r"ui_bubble_rating bubble_\d+")
            )
            if rating_span:
                rating_class = rating_span["class"]
                rating_value = (
                    int(
                        [cls for cls in rating_class if cls.startswith("bubble_")][
                            0
                        ].replace("bubble_", "")
                    )
                    / 10
                )
                allRatings.append(rating_value)
            else:
                allRatings.append(None)

    except Exception as e:
        print("An error occurred:", e)

    return allRatings


def get_average_rating(soup):
    """
    Extracts and returns the average rating of a hotel from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
    str: The average rating of the hotel or "None" if not found.
    """
    try:
        average_rating_class = soup.find("span", attrs={"class": "uwJeR P"})

        average_rating_value = average_rating_class.text

        average_rating_string = average_rating_value.strip()

    except AttributeError:
        average_rating_string = "None"

    return average_rating_string


def get_overall_exp(soup):
    """
    Extracts and returns the overall experience ratings of a hotel from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
    list: A list of overall experience ratings or "None" if not found.
    """
    overall = []
    try:
        overall_exp_class = soup.find_all("div", attrs={"class": "WdWxQ"})
        for element in overall_exp_class:
            overall_span = element.find("span", attrs={"class": "CzVMJ"})
            if overall_span:
                rating = overall_span.get_text()
                overall.append(float(rating))
    except AttributeError:
        overall = "None"

    return overall


def get_review_count(soup):
    """
    Extracts and returns the review count of a hotel from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
    str: The review count of the hotel or "None" if not found.
    """
    try:
        review_count = soup.find("span", attrs={"class": "hkxYU q Wi z Wc"})

        review_count_value = review_count.text

        review_count_string = review_count_value.strip()

    except AttributeError:
        review_count_string = "None"

    return review_count_string


def get_hotel_class(soup):
    """
    Extracts and returns the hotel class (if available) from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
    str: The hotel class or "None" if not found.
    """
    try:
        hotel_class = soup.find("svg", class_="JXZuC d H0")
        aria_label = hotel_class.get("aria-label")

    except AttributeError:
        aria_label = "None"
    return aria_label


def get_overall_details(soup):
    """
    Extracts and returns additional details about the hotel from a BeautifulSoup object.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the hotel information.

    Returns:
    list: A list of additional details or "None" if not found.
    """
    good_to_know = []

    try:
        for div in soup.find_all("div", attrs={"class": "euDRl _R MC S4 _a H"}):
            good_to_know.append(div.text.strip())
    except AttributeError:
        good_to_know = "None"

    return good_to_know
