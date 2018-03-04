import requests
import json

def grab_tags(url):
    """ Retrieves image tags of a Google-searched image given
    url of the image.

    Returns: list of strings containing tags
    """

    subscription_key = "cfa2ac95fcf04101b79b839837876d16"
    assert subscription_key
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"

    vision_analyze_url = vision_base_url + "analyze"

    image_url = url

    headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
    params   = {'visualFeatures': 'Tags'}
    data     = {'url': image_url}
    response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
    response.raise_for_status()
    analysis = response.json()
    # print(analysis['tags'])
    # print(analysis['tags'][1]['name'])
    keywords = [tag_dict['name'] for tag_dict in analysis['tags']]

    return keywords


if __name__ == "__main__":
    url = 'https://www.mcdonalds.com/content/dam/usa/nutrition/items/evm/h-mcdonalds-Double-Quarter-Pounder-with-Cheese-Extra-Value-Meals.png'
    analyze_img(url)
