from app.models.ConnectionFactory import ConnectionFactory 

class ActorsModel():
    def __init__(self, name, email):
        self.name = name
        self.email = email

    
    def create(self):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        sql = "INSERT INTO Actors (name, email) VALUES (%s, %s)"
        val = ("", "")
        
        mycursor.execute(sql, val)

        mydb.commit()

        print("Uma pessoa foi cadastrada com sucesso!")


    def update_actor(self, actor, person):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        p = get_actor(person)

        print(person)
        sql = ("update Actors set name=%s, email=%s, Persons_code=%s where code=%s")
        val = (p[1], p[2], person, actor)

        mycursor.execute(sql, val)

        mydb.commit()
