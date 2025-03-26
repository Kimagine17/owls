import mysql.connector
import json

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
        
    def insert_row(self):
        pass

def main():
    testConnector = CustcoConnector()

main()
