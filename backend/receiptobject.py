import MySQLdb


host="hacktech2018.cgbpz4xtbq6x.us-west-2.rds.amazonaws.com"
user="brian"
passwd="hacktech"
db=""
conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
x = conn.cursor()
try:
    x.execute("")
    conn.commit()
except:
    conn.rollback()

conn.close()
class MyError(Exception):
    pass

class receipt:
    def __init__(self, l):
        if len(l) != 5:
            raise MyError
        self.date = l[0]
        self.item = l[1]
        self.cost = l[2]
        self.place = l[3]
        self.category = l[4]


def test():
    
        
