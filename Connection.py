import mysql.connector

def insert_actor():
    mydb = init()
    mycursor = mydb.cursor()

    sql = "INSERT INTO Actors (name, email) VALUES (%s, %s)"
    val = ("", "")
    
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, " record was inserted.")

def get_last_id():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Actors")

    myresult = mycursor.fetchall()

    last_id = myresult[-1][0]

    print(last_id)

    return last_id

def init():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="eduardo",
        database="datasetmanagerdb"
    )

    print(mydb)

    return mydb