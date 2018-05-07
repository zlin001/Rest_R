import requests

headers = {"Authorization":"Bearer 5uVEBGiZ40XPkmlPEw-fb478unHY3MG2j2KvwVNcQF61OUjLs1lwjWTDIZfHgRwzcf3aWC7McbdWqs4qz-Z3XB0HGR7rOsxD-sbQsbbOeMfl8c8xNoGW3Sbv4NvUWnYx"}

def find_all_rests(zip_code):
    search_url = "https://api.yelp.com/v3/businesses/search?location=" + zip_code + "&term=restaurants&limit=30"
    response = requests.get(search_url, headers=headers).json()



    restaurants = response["businesses"]
    rest_urls = []

    for rest in restaurants:
        rest_urls.append(rest["url"])

    return rest_urls
