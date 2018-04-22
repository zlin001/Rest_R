from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re

def crawl_pages(base_url):
    count = 0
    reviews_in_page = []
    next_button = True

    while next_button:
        current_url = base_url + str(count)
        html = requests.get(current_url)
        soup = BeautifulSoup(html.text, "html.parser")

        review_container = soup.findAll('div', attrs={ 'class': 'review-content'})

        for review in review_container:
            reviews_in_page.append(review.find('p').text)

        next_button = soup.findAll('a', attrs={'class': 'next'})
        count = count + 20

    return reviews_in_page

url = "https://www.yelp.com/biz/aria-kabab-flushing-3?start="
#print(crawl_pages(url))
reviews = crawl_pages(url)
f = open('reviews_clean.txt','r+')
for i in range(len(reviews)):
    f.write(reviews[i] + '\n')
f.close()
