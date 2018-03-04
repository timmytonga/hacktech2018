def extract_cost(s):
    """ given a cost string in format of 48 02 or 48.02 or $48.02 or 
        total = 48.02, etc... => extract the number and return
        4802 (can be int or str doesnt matter)  --> result will be in cents"""
    result = [str(i) for i in s if i.isdigit()]
    return "".join(result)

def extract_str_date(s):
    result = [str(i) for i in s if i.isdigit()]
    if len(result) == 6:
        return "".join(["20"]+result[4:]+ result[0:4])
    return "".join(result[4:]+ result[0:4])

def get_category(s):
    """ given an input str, determine the category from the list of available category
    Potential: when user corrects a category, update frequency list and have
    the algorithm predict better category depending on the input
    E.g.: McDonalds -> food, Chevron -> gas, shirts -> clothings, etc.
    -----> Can we search online for word -> use MS API to obtain tags -> scan tags for categories"""
    possible_mapping = {'food':{'mcdonalds','orange'}, 'clothings':{'shirts','pants','skirts', 'dress'}}
    if "mcdonalds" in s:
        return "food"


if __name__== "__main__":
    a = "48.08"
    b = "$48.08"
    c = "48 08"
    d = "Total amount = 48.08 USD"

    da = "Date = 03/ 02 / 2018"
    db = "03/02/2018"
    dc = "03 - 02 -2018"
    dd = " DATE is 03/ 02 2018"
    de = "03/02/18"
    
