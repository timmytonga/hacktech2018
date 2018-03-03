from hacktechdb import *
import random

mapping= {
    "food":["mcdonalds", "ramen", "inandout",
              "pho", "five guys", "kfc", "sushi", "umami burger", "meet fresh",
              "tea station", "half n half", "gyutan tsukasa", "samwoo" ],
    "coffee": ["starbucks", "peets", "coffe tomo", "sootha coffee",
               "the coffee bean and tea leaves", "java city"],
    "shopping":[ "shirts", "skirts", "outfit", "wallet", "belt", "makeup", "haircare", "shaving"],
    "gas" : ["chevron", "shell", "arco", "mobil", ],
    "medical" : ["bandage", "lipbalm", "moisturizer", "aspirin", "ibuprofene"
                 , "hand sanitizer", "'drugs'"],
    "groceries" : ["albertsons", "vons", "ralphs", "99ranch", "mitsuwa"]
    }

costrange = {"food" : (800,3000), "coffee" : (300,600), "shopping" : (1000, 10000),
             "gas" : (4000, 7000), "medical" : (400, 10000), "groceries" : (2000, 5000)}

def generateData(n, cat): # n = number of times and cat is category

    for i in range(n):
        randomDay= 20180300 + random.randrange(1,31)
        randomItem = random.choice(mapping[cat])
        randomCost = random.randrange(costrange[cat][0], costrange[cat][1])
        query = [randomDay, randomItem, randomCost, randomItem, cat]
        sendQuery(receipt(query))

if __name__ == "__main__":
    catlist = ["food", "coffee", "shopping", "gas", "medical", "groceries"]
    for cat in catlist:
        generateData(10,cat)
