from app.models.ConnectionFactory import ConnectionFactory 

class ActorsModel():
    def __init__(self, code="", name="", email="", Persons_code=None):
        self.code = code
        self.name = name
        self.email = email
        self.Persons_code = Persons_code

    def getPersonByCode(self, code):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM Persons WHERE code = {}".format(code))

        myresult = mycursor.fetchone()

        return myresult

    def create(self):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        sql = "INSERT INTO Actors (name, email, Persons_code) VALUES (%s, %s, %s)"
        val = (self.name, self.email, self.Persons_code)
        
        mycursor.execute(sql, val)

        mydb.commit()

        actor_code = mycursor.lastrowid

        print("Um ator foi cadastrado com sucesso!")

        return actor_code


    #def create(self):
    #    mydb = ConnectionFactory().getConnection()
    #    mycursor = mydb.cursor()

    #    sql = "INSERT INTO Actors (name, email) VALUES (%s, %s)"
    #    val = ("", "")
        
    #    mycursor.execute(sql, val)

    #    mydb.commit()

    #    print("Uma pessoa foi cadastrada com sucesso!")

    #    return True

    def update(self):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        person = self.getPersonByCode(self.Persons_code)

        name = person[1]
        email = person[2]

        sql = "UPDATE Actors SET name=%s, email=%s, Persons_code=%s WHERE code=%s"
        val = (name, email, self.Persons_code, self.code)

        mycursor.execute(sql, val)

        mydb.commit()
        
        print("O ator foi atualizado com sucesso!")

        return True
