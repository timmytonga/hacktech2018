#!/usr/bin/python

import mysql.connector
from mysql.connector import errorcode

class Database:
    host="hacktech.cgbpz4xtbq6x.us-west-2.rds.amazonaws.com"
    user="brian"
    passwd="hacktech"
    db="hacktech"

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=self.user,
                                                  password=self.passwd,
                                                  host=self.host,
                                                  database=self.db)
            
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        
        self.cursor = self.connection.cursor()

    def insert(self, query, data=""):
        cursor = self.connection.cursor()
        cursor.execute(query,data)
        self.connection.commit()

    def query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

    def close(self):
        self.connection.close()

class receipt:
    """ receipt(l) -> l is a list of [date, item, cost, place, category]
    simple struct to store receipt's info """
    total = 5  # total number of items or info receiving
    def __init__(self, l):
        if len(l) != 5:
            raise MyError
        self.date = l[0]        # int in format yyyymmdd
        self.item = l[1]        # string
        self.cost = l[2]        # int
        self.place = l[3]       # string
        self.category = l[4]    # string --> specific category

    def getMySQLValues(self):
        ''' return a string that can be insert into a mysql database'''
        result = '(' + str(self.date) + ', '        # an int in format yyyymmdd
        result += "'" + self.item + "', "      # a string 
        result += "" + str(self.cost) + ", "
        result += "'" + self.place + "', "
        result += "'" + self.category + "')"
        return result
    
    def __str__(self):
        return self.getMySQLValues()
    
def sendQuery(receipt): # send receipt to MySQL database
    """ Input must be receipt object """
    print(receipt)
    db = Database()
    tableName = "detail"
    #query = "INSERT INTO " + tableName + " ('issueDate', 'item', 'cost', 'place', 'category') " + \
    #       "VALUES " + receipt.getMySQLValues()
    query = "INSERT INTO " + tableName + " (issueDate, item, cost, place, category) " + \
          "VALUES (%s, %s, %s, %s, %s)"
    addData = (receipt.date, receipt.item, receipt.cost, receipt.place, receipt.category)
    print(query)
    db.insert(query, addData)
    db.close()

def getURL():       # return a string for the URL
    db = Database()
    tableName = "receipt"
    select_query = """SELECT url FROM receipt"""
    result = db.query(select_query)
    db.close()
    return result
 
if __name__ == "__main__":
    print("Sending a test receipt and also trying to get a URL")
    print("Getting URL...")
    url = getURL()
    print("URL is: " + str(url))
    print("Sending receipt..." )
    test = ['20180303', 'shoes', '30', 'Target', 'clothings']
    test2 = ['20180304', 'gas', '50', 'Chevron', 'gas'] 
    testReceipt = receipt(test2)
    sendQuery(testReceipt)
    #print(testReceipt)
    print("done.")
    
    
