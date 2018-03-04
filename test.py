import requests
import json
import time

def get_text_from_img(url):
    subscription_key = "72849a2b1dc84c10841e9df1103667ff"
    assert subscription_key
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    image_url = url

    headers = {'Ocp-Apim-Subscription-Key': subscription_key }
    params = {'handwriting' :True} 
    data = {'url' : image_url}

    text_recognition_url = vision_base_url + "RecognizeText"
    print(text_recognition_url)

    response = requests.post(text_recognition_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    operation_url = response.headers["Operation-Location"]

    analysis = {}

    while not "recognitionResult" in analysis:
        response_final = requests.get(response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        time.sleep(1)

    polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResult"]["lines"]]

    flag = 0
    first = 1
    for i in polygons:
        if "2017" in i[1] or "2018" in i[1] or "2016" in i[1]:
            print("DATE IS: " + i[1])
        if first == 1:
            print("RESTAURANT IS: " + i[1])
            first = 0
        elif flag == 1:
            print("COST IS: " + i[1])
        else:
            #print(i[1])
            pass
        if ( "Total" in i[1]):
            flag = 1
    
        
def extract_str_date(s):
    """given a string s in format of 03 / 02/ 2018 or 03/02/2018 or 
        03-02-2018 or 03 02 2018 
        -> return appropriate format: 20180302 for mysql query"""
    pass

def extract_cost(s):
    """ given a cost string in format of 48 02 or 48.02 or $48.02 or 
        total = 48.02, etc... => extract the number and return
        4802 (can be int or str doesnt matter)  --> result will be in cents"""
    pass

def get_category(s):
    """ given an input str, determine the category from the list of available category
    Potential: when user corrects a category, update frequency list and have
    the algorithm predict better category depending on the input
    E.g.: McDonalds -> food, Chevron -> gas, shirts -> clothings, etc.
    -----> Can we search online for word -> use MS API to obtain tags -> scan tags for categories"""

    list_of_cat = ['food', 'clothings', 'gas', 'groceries', 'medical']
    possible_mapping = {'food':{'mcdonalds','orange'}, 'clothings':{'shirts','pants','skirts', 'dress'}}
    pass


def uploadtoDB(date, item, place, cost):
    """ receive info about the date, item, place, cost """
if __name__ == "__main__":
    url = "https://www.blogography.com/photos70/McDonaldsEggAndCheese.jpg"
    get_text_from_img(url)
