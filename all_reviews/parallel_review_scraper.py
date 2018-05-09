from urllib.request import urlopen
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
import requests
import re
import time

def crawl_pages(base_url):
    count = 0
    reviews_in_page = []
    next_button = True

    while next_button:
        current_url = base_url + str(count)
        html = requests.get(current_url)
        soup = BeautifulSoup(html.text, "lxml")

        review_container = soup.findAll('div', attrs={ 'class': 'review-content'})

        for review in review_container:
            reviews_in_page.append((review.find('p').text).encode("utf-8"))

        next_button = soup.findAll('a', attrs={'class': 'next'})
        count = count + 20

    print(base_url)
    print("\n")

    # print(reviews_in_page)
    return reviews_in_page

def get_30_rests_urls():
    headers = {"Authorization":"Bearer 5uVEBGiZ40XPkmlPEw-fb478unHY3MG2j2KvwVNcQF61OUjLs1lwjWTDIZfHgRwzcf3aWC7McbdWqs4qz-Z3XB0HGR7rOsxD-sbQsbbOeMfl8c8xNoGW3Sbv4NvUWnYx"}
    response = requests.get("https://api.yelp.com/v3/businesses/search?location=11355&term=restaurants&limit=30", headers=headers).json()
    restaurants = response["businesses"]
    rest_urls = []

    for rest in restaurants:
        rest_urls.append(rest["url"])

    return rest_urls

if __name__ == '__main__':
    start_time = time.time()

    all_rests_urls = get_30_rests_urls()
    fixed_urls = []

    for url in all_rests_urls:
        url = re.sub("\?(.*)", '', url)
        url = url + "?start="
        fixed_urls.append(url)


    reviews = Parallel(n_jobs=-1)(map(delayed(crawl_pages), fixed_urls))

    elapsed_time = start_time - time.time()

    print(elapsed_time)

    # print(reviews)
