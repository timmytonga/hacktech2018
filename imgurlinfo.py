import requests
import json
import time
import sys
import hacktechdb

def extract_cost(s):
    """ given a cost string in format of 48 02 or 48.02 or $48.02 or 
        total = 48.02, etc... => extract the number and return
        4802 (can be int or str doesnt matter)  --> result will be in cents"""
    result = [str(i) for i in s if i.isdigit()]
    return "".join(result)

def extract_str_date(s):
    result = [str(i) for i in s if i.isdigit()]
    if len(result) == 6:
        return "".join(["20"]+result[4:8]+ result[0:4])
    return "".join(result[4:8]+ result[0:4])

def get_category(s):
    """ given an input str, determine the category from the list of available category
    Potential: when user corrects a category, update frequency list and have
    the algorithm predict better category depending on the input
    E.g.: McDonalds -> food, Chevron -> gas, shirts -> clothings, etc.
    -----> Can we search online for word -> use MS API to obtain tags -> scan tags for categories"""
    possible_mapping = {'food':{'mcdonalds','orange'}, 'clothings':{'shirts','pants','skirts', 'dress'}}
    # stupid algorithm --> just for testing
    if "Restaurant" in s:
        return "food"
    else:
        return "unknown"

def get_text_from_img(url):
    ''' return a receipt object'''
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

    date = ''
    cost = ''
    item = ''
    cat = ''
    place = ''
    
    flag = 0
    first = 1
    for i in polygons:
        # detect date
        if "2017" in i[1] or "2018" in i[1] or "2016" in i[1]:
            date = extract_str_date(i[1])
        
        if first == 1:
            place = i[1]
            first = 0
        elif flag == 1:
            cost = extract_cost(i[1])
            
        if ( "Total" in i[1]):
            flag = 1

    cat = get_category(place)
    l = [date, place, cost, place, cat]
    return hacktechdb.receipt(l)
    

def urltoDB(url):
    """ receive info about the date, item, place, cost """
    hacktechdb.sendQuery(get_text_from_img(url))
    
    
    
if __name__ == "__main__":
    url = sys.argv[1]
    urltoDB(url)
