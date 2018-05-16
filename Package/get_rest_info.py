import requests
import re

headers = {"Authorization":"Bearer 5uVEBGiZ40XPkmlPEw-fb478unHY3MG2j2KvwVNcQF61OUjLs1lwjWTDIZfHgRwzcf3aWC7McbdWqs4qz-Z3XB0HGR7rOsxD-sbQsbbOeMfl8c8xNoGW3Sbv4NvUWnYx"}

# {"name": "aria kabab", url: "aria.com", "total_score": 3.2}
def get_rest_info(rest_info):
    search_url = "https://api.yelp.com/v3/businesses/search?location=11355&term=" + str(rest_info["name"]) + "&limit=1"
    response = requests.get(search_url, headers=headers).json()
    restaurants = response["businesses"]

    if len(restaurants) == 0:
        rest_info["address"] = "Not Available"
        rest_info["phone"] = "Not Available"
        rest_info["name"] = str(rest_info["name"])
        # address =  restaurant["location"]["display_address"][0] + " " + restaurant["location"]["display_address"][1]
        rest_info["total_score"] = round((rest_info["total_score"] * 5),1)
        return rest_info

    restaurant = restaurants[0]

    if len( restaurant["location"]["display_address"]) > 0:
        address =  restaurant["location"]["display_address"][0] + " " + restaurant["location"]["display_address"][1]
    else:
        address = "Not Available"
        
    phone = restaurant["phone"]

    rest_info["name"] = str(rest_info["name"])
    rest_info["total_score"] = round((rest_info["total_score"] * 5),1)
    rest_info["address"] = address
    rest_info["phone"] = phone

    return rest_info

def get_all_rest_info(all_rest_info):
    rest_info = []
    for rest in all_rest_info:
        rest_info.append(get_rest_info(rest))
    return rest_info
