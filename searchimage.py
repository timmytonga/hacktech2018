import requests
import json
from grab_img_tags import grab_tags
import time

def image_srch(word, max_images):
    subscription_key = "96d05359d76f4e758906539daeab939e"
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    search_term = word

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # print(analysis['tags'][1]['name'])
    urls = [search_dict['thumbnailUrl'] for search_dict in search_results['value']]

    all_tags = []
    for url in urls[0:max_images]:
        tag_list = grab_tags(url)
        all_tags += (tag_list)
        time.sleep(3)
        print(tag_list)
    return all_tags
