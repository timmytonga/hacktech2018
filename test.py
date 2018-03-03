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
        



if __name__ == "__main__":
    url = "https://www.blogography.com/photos70/McDonaldsEggAndCheese.jpg"
    get_text_from_img(url)
