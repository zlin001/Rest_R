from urllib.request import urlopen
from joblib import Parallel, delayed
from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests
import re
import time
import win_unicode_console

def get_all_reviews(all_rest_urls):
    win_unicode_console.enable()
    start_time = time.time()

    with Pool(35) as p:
        all_reviews = p.map(crawl_pages, all_rest_urls)
        p.terminate()
        p.join()

    elapsed_time = time.time() - start_time

    print(elapsed_time/60)

    return(all_reviews)


def crawl_pages(all_restaraunts_init_data):
    count = 0
    base_url = all_restaraunts_init_data[1]
    reviews_in_page = []
    review_name_text = []

    next_button = True

    crawl_start_time = time.time()
    elapsed_time = 0

    while next_button and elapsed_time <  45:
        current_url = base_url + str(count)
        html = requests.get(current_url)
        soup = BeautifulSoup(html.text, "html.parser")

        review_container = soup.findAll('div', attrs={ 'class': 'review-content'})

        for review in review_container:
            reviews_in_page.append((review.find('p').text))
            # reviews_in_page.append("reviews in page")

        next_button = soup.findAll('a', attrs={'class': 'next'})
        count = count + 20

        elapsed_time = time.time() - crawl_start_time

    review_name_text.append(all_restaraunts_init_data[0])
    review_name_text.append(reviews_in_page)
    review_name_text.append(base_url)


    return review_name_text

if __name__ == '__main__':
    get_all_reviews(all_rest_urls)
