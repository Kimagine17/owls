import mysql.connector
import json
import datetime

class CustcoConnector:
    db = None
    def __init__(self):
        # Create a file named custcoCredentials.json that looks like the following
        #
        # {
        # "host": "your_host",
        # "user": "your_username",
        # "password": "your_password",
        # "database": "custco"
        # }
        file = open("custcoCredentials.json", "r")
        tempString = ""
        for line in file:
            tempString = tempString + line
        print(tempString)
        jsonObj = json.loads(tempString)

        self.db = mysql.connector.connect(
        host=jsonObj["host"],
        user=jsonObj["user"],
        password=jsonObj["password"],
        database=jsonObj["database"]
        ) 

    def format_time(self):
        t = datetime.datetime.now()
        s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
        return s[:-3]
        
    def insert_row(self, interior_owl, perched_owl, chicks, egg, source):
        if(interior_owl == None and perched_owl == None and chicks == None and egg == None):
            print(f"No insertions\n")
            return
        if(interior_owl == None):
            interior_owl = 0
        if(perched_owl == None):
            perched_owl = 0
        if(chicks == None):
            chicks = 0
        if(egg == None):
            egg = 0

        time = self.format_time()
        print(time)

        id = 0

        conn = self.db.connect('custco.db')

        # Create a cursor object
        cursor = conn.cursor()
        #interior_owl (int), perched_owl (int), chick(int), egg (int), time(date_time (utc)), source(text)
        cursor.execute('''
        INSERT INTO owls (interior_owl, perched_owl, chick, egg, source_id, time)
        VALUES (?, ?, ?, ?)
        ''', (interior_owl, perched_owl, chicks, egg, time, id))

        # Commit the transaction
        conn.commit()
        

def main():
    testConnector = CustcoConnector()

main()


##