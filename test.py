import requests

subscription_key = "72849a2b1dc84c10841e9df1103667ff"

assert subscription_key

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0"

image_url = "http://ricdesign.co/wp-content/uploads/fake-receipt-template-expressexpense-custom-receipt-maker-1.jpg"

headers = {'Ocp-Apim-Subscription-Key': subscription_key }
params = {'language': 'unk', 'detectOrientation' : 'true'}
data = {'url' : image_url}

response = requests.post(ocr_url, headers=headers, params=params, json=data)
response.raise_for_status()

analysis = response.json()

print(analysis)
