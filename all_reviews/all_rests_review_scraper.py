from urllib.request import urlopen
from joblib import Parallel, delayed
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

def get_30_rests_urls():
    headers = {"Authorization":"Bearer 5uVEBGiZ40XPkmlPEw-fb478unHY3MG2j2KvwVNcQF61OUjLs1lwjWTDIZfHgRwzcf3aWC7McbdWqs4qz-Z3XB0HGR7rOsxD-sbQsbbOeMfl8c8xNoGW3Sbv4NvUWnYx"}
    response = requests.get("https://api.yelp.com/v3/businesses/search?location=11355&term=restaurants&limit=30", headers=headers).json()
    restaurants = response["businesses"]
    rest_urls = []

    for rest in restaurants:
        rest_urls.append(rest["url"])

    return rest_urls


url = "https://www.yelp.com/biz/aria-kabab-flushing-3?start="

all_rests_urls = get_30_rests_urls()

file_count = 0
for url in all_rests_urls:
    print(file_count)
    # # file_name = "file_name" + str(file_count) + ".txt"
    # file_count += 1

    url = re.sub("\?(.*)", '', url)
    url = url + "?start="
    reviews = crawl_pages(url)

    f = open("all_reviews.txt",'ab+')
    for i in range(len(reviews)):
        f.write((reviews[i] + '\n').encode("utf-8"))
    f.close()


# reviews = crawl_pages(url)
# f = open('reviews_clean.txt','r+')
# for i in range(len(reviews)):
#     f.write(reviews[i] + '\n')
# f.close()
