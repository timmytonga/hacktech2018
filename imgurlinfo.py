import requests
import json
import time
import sys
import hacktechdb
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def extract_cost(s):
    """ given a cost string in format of 48 02 or 48.02 or $48.02 or 
        total = 48.02, etc... => extract the number and return
        4802 (can be int or str doesnt matter)  --> result will be in cents"""
    result = [str(i) for i in s if i.isdigit()]
    return "".join(result)

def extract_str_date(s):
    """given a string s in format of 03 / 02/ 2018 or 03/02/2018 or 
        03-02-2018 or 03 02 2018 
        -> return appropriate format: 20180302 for mysql query"""
    result = "".join([str(i) for i in s if i.isdigit()])
    print(">RESULT IS: " + result)
    start = result.find("2018")
    if start == -1:
        start = result.find("2017")
        if start == -1:
            start = result.find("2016")
            if start == -1:
                raise Exception
    if start <= 3 or int(result[start-4:start-2]) > 12:
        return "".join(result[start:start+4]+ "0" + result[start-3:start])
    return "".join(result[start:start+4]+ result[start-4:start])

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
    elif "Market" in s:
        return "groceries"
    else:
        return "other"

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
    print("Running...")

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
        #print(i[1])
        if "2017" in i[1] or "2018" in i[1] or "2016" in i[1] or \
        "/ 17" in i[1] or "/ 18" in i[1] or "/ 16" in i[1]:
            date = extract_str_date(i[1])
        if first == 1: # assuming users take pictures with title on the top
            place = i[1]
            first = 0
        elif flag == 1:
            cost = extract_cost(i[1])
            flag = 2

        # lots of cases
        if ( flag == 0) and (("total" in i[1].lower() and "sub" not in i[1].lower()\
                              and "donation" not in i[1].lower()) \
              or (("visa" in i[1].lower() or "debit" in i[1].lower()) or \
                  "balance" in i[1].lower())):
           # print(">>> flag on!!!" + i[1])
            flag = 1
    cat = get_category(place)
    l = [date, place, cost, place, cat]
    return hacktechdb.receipt(l)
    

def urltoDB(url):
    """ receive info about the date, item, place, cost """
    hacktechdb.sendQuery(get_text_from_img(url))
    #print(get_text_from_img(url))
    
    
if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        print("ERROR (usage): python imgurlinfo.py URL")
        raise Exception
    url = sys.argv[1]
    urltoDB(url)
