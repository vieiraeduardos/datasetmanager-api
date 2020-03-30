import mysql.connector

def insert_actor():
    mydb = init()
    mycursor = mydb.cursor()

    sql = "INSERT INTO Actors (name, email) VALUES (%s, %s)"
    val = ("", "")
    
    mycursor.execute(sql, val)

    mydb.commit()

    print("Uma pessoa foi cadastrada com sucesso!")


def get_last_id():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Actors")

    myresult = mycursor.fetchall()

    last_id = myresult[-1][0]

    return last_id

def init():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="eduardo",
        database="datasetmanagerdb"
    )

    return mydb

def insert_person(name, email):
    mydb = init()
    mycursor = mydb.cursor()

    sql = "INSERT INTO Persons (name, email) VALUES (%s, %s)"
    val = (name, email)
    
    mycursor.execute(sql, val)

    mydb.commit()

    print("Uma pessoa foi cadastrada com sucesso!")


def get_persons(name):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Persons WHERE name LIKE '%{}%'".format(name))

    myresult = mycursor.fetchall()

    return myresult