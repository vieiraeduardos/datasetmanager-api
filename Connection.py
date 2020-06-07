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
        auth_plugin='mysql_native_password'
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

    sql = ("INSERT INTO Annotations(Videos_code, Actors_code, x, y, w, h, time, path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    val = (int(video_code), int(actor_video), int(x), int(y), int(w), int(h), int(time), path)

    mycursor.execute(sql, val)

    mydb.commit()

    print("Annotation was successfully inserted!")


def get_annotations_by_video(video):
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select * from Annotations inner join Actors where Videos_code={} and Actors.code = Annotations.Actors_code order by Annotations.Actors_code".format(video))

    myresult = mycursor.fetchall()

    return myresult

def get_all_annotations():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select * from Annotations inner join Actors where Actors.code = Annotations.Actors_code and Annotations.isClusterized = 'false' order by Annotations.Actors_code")

    myresult = mycursor.fetchall()

    return myresult

def get_videos():
    mydb = init()
    mycursor = mydb.cursor()

    mycursor.execute("select code, filename from Videos")

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