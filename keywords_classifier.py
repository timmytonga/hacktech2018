from searchimage import image_srch
from imgurlinfo.py import get_text_from_img

kc = ['food', 'clothing', 'health']
word_net = {}
# coffee, food, gas, groceries, medical, shopping
word_net['food'] = ('food',
                    'marketplace',
                    'fresh',
                    'produce',
                    'vegetable',
                    'meat',
                    'fast food',
                    'noodle',
                    'rice',
                    'burger',
                    'egg',
                    'cake',
                    'pastry',
                    'meal',
                    'dish',
                    'groceries',
                    'grocery',
                    'restaurant')

word_net['clothing'] = ('clothing',
                        'pants',
                        'shirt',
                        'blouse',
                        'shoe',
                        'shoes',
                        'trouser',
                        'suit',
                        'jacket',
                        'clothes',
                        'dressed',
                        'coat',
                        'wearing',
                        'work-clothing',
                        'hat',
                        'sleeve',
                        'necktie')
word_net['health'] = ('medicine',
                      'toothpaste',
                      'toothbrush',
                      'clean',
                      'cleaning')

def get_category(text):
    """ searches in bing for each word given by the receipt
        and acquires the tags for the first ten images.
        then checks if any of the tags are in our word_net
        if yes, release category

        lol there are only 3 categories and all of them are weak
    """
    item_class = {}
    for t in text:
        all_tags = img_srch(t, max_images=20)
        for tag in all_tags:
            if tag in word_net[kc[0]]:
                item_class[t] = kc[0]
            elif tag in word_net[kc[1]]:
                item_class[t] = kc[1]
            elif tag in word_net[kc[2]]:
                item_class[t] = kc[2]
    return item_class

if __name__ == "__main__":
    url = sys.argv[1]
    receipt, polygons = get_text_from_img(url)
    text = []
    for i in polygons:
        text += i[1]
    item_class = get_category(text)
    print(item_class)
