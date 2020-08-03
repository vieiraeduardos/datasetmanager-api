import mysql.connector

class ConnectionFactory():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="eduardo",
            database="datasetmanagerdb",
        )

    def getConnection(self):
        return self.mydb
