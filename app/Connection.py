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
        database="datasetmanagerdb",
    )

    return mydb

def insert_person(name, email, actor):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT Annotations.path FROM Actors INNER JOIN Annotations WHERE Actors.code = {}".format(actor))

    myresult = mycursor.fetchone()

    path = myresult[0]

    mydb = init()
    mycursor = mydb.cursor()

    sql = "INSERT INTO Persons (name, email, profile_photo) VALUES (%s, %s, %s)"
    val = (name, email, path)
    
    mycursor.execute(sql, val)

    mydb.commit()

    print("Uma pessoa foi cadastrada com sucesso!")

def createActor(name="", email="", persons_code=0):
    mydb = init()
    mycursor = mydb.cursor()

    sql = "INSERT INTO Actors (name, email, Persons_code) VALUES (%s, %s, %s)"
    val = (name, email, persons_code)
    
    mycursor.execute(sql, val)

    mydb.commit()

    actor_code = mycursor.lastrowid

    print("Uma pessoa foi cadastrada com sucesso!")

    return actor_code

def getVideoCodeByFilename(filename):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT code FROM Videos WHERE filename = '{}'".format(filename))

    myresult = mycursor.fetchone()

    return myresult[0]

def updateAnnotations(code):
    mydb = init()
    mycursor = mydb.cursor()

    sql = ("update Annotations set isRight=false where code={}".format(code))

    mycursor.execute(sql)

    mydb.commit()

    print("Annotation was successfully updated!")



def getAnnotationsByPerson(person_code):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select Annotations.code, Actors.name, Annotations.path from Annotations inner join Actors inner join Persons on Actors.code = Annotations.Actors_code and Persons.code = Actors.Persons_code and Persons.code = {} order by Annotations.Actors_code".format(person_code))

    myresult = mycursor.fetchall()

    return myresult

def getAllPersons():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Persons")

    myresult = mycursor.fetchall()

    return myresult

def getPersonCodeByName(name):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT code FROM Persons WHERE name = '{}'".format(name))

    myresult = mycursor.fetchone()

    return myresult[0]

def createPerson(name="", email="", profile_photo=""):
    mydb = init()
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO Persons (name, email, profile_photo) VALUES (%s, %s, %s)"
    val = (name, email, profile_photo)
    
    mycursor.execute(sql, val)

    mydb.commit()

    print("Uma pessoa foi cadastrada com sucesso!")

    person_code = mycursor.lastrowid

    return person_code


def get_persons(name):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM Persons WHERE name LIKE '%{}%'".format(name))

    myresult = mycursor.fetchall()

    return myresult


def insert_video(filename="", path="", duration="", tags=""):
    mydb = init()
    mycursor = mydb.cursor()

    sql = ("INSERT INTO Videos(filename, path, duration, tags) VALUES (%s, %s, %s, %s)")
    val = (filename, path, duration, tags)

    mycursor.execute(sql, val)

    mydb.commit()

    video_code = mycursor.lastrowid

    print("Video was successfully inserted!")
    print(video_code)

    return video_code


def insert_annotation(video_code, actor_video, x, y, w, h, time, path):
    mydb = init()
    mycursor = mydb.cursor()

    sql = ("INSERT INTO Annotations(Videos_code, Actors_code, x, y, w, h, time, path, isRight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (int(video_code), int(actor_video), int(x), int(y), int(w), int(h), int(time), path, True)

    mycursor.execute(sql, val)

    mydb.commit()

    print("Annotation was successfully inserted!")


def get_annotations_by_video(video):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select * from Annotations inner join Actors inner join Persons where Videos_code={} and Actors.code = Annotations.Actors_code and Persons.code = Actors.Persons_code order by Annotations.Actors_code".format(video))

    myresult = mycursor.fetchall()

    return myresult

def get_all_annotations():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select Annotations.code, Annotations.path, Actors.name, Actors.Persons_code, Actors.code, Annotations.isRight from Annotations inner join Actors  where Annotations.Actors_code = Actors.code order by Annotations.Actors_code")

    myresult = mycursor.fetchall()

    return myresult

def get_videos():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select code, filename from Videos")

    myresult = mycursor.fetchall()

    return myresult


def get_all_videos():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT Videos.code, Videos.path FROM Videos")

    myresult = mycursor.fetchall()

    return myresult

def get_actor(code):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select * from Persons where code = {}".format(code))

    myresult = mycursor.fetchone()

    return myresult


def update_actor(actor, person):
    mydb = init()
    mycursor = mydb.cursor()

    p = get_actor(person)

    print(person)
    sql = ("update Actors set name=%s, email=%s, Persons_code=%s where code=%s")
    val = (p[1], p[2], person, actor)

    mycursor.execute(sql, val)

    mydb.commit()

    print("Actor was successfully updated!")


def delete_image(code): 
    mydb = init()
    mycursor = mydb.cursor()

    sql = ("delete from Annotations where code = {}".format(code))
    
    mycursor.execute(sql)

    mydb.commit()

    print("Image was successfully removed!")

def update_image(image, person):
    mydb = init()
    mycursor = mydb.cursor()

    sql = ("delete from Annotations where code = {}".format(image))
    
    mycursor.execute(sql)

    mydb.commit()

    print("Image was successfully updated!")
