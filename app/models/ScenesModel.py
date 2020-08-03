from app.models.ConnectionFactory import ConnectionFactory 

class ScenesModel():
    def __init__(self, videosCode=0, description="", startTime="", endTime=""):
        self.videosCode = videosCode
        self.description = description
        self.startTime = startTime
        self.endTime = endTime


    def createDescription(self):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        sql = "INSERT INTO Scenes (Videos_code, description, startTime, endTime) VALUES (%s, %s, %s, %s)"
        val = (self.videosCode, self.description, self.startTime, self.endTime)
    
        mycursor.execute(sql, val)

        mydb.commit()

        Scene_code = mycursor.lastrowid

        print("Uma descrição foi cadastrada com sucesso!")

        return Scene_code

    def getAllScenesByVideo(self):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM Scenes WHERE Videos_code={}".format(self.videosCode))

        myresult = mycursor.fetchall()

        return myresult

    def deleteSceneByCode(self, code):
        mydb = ConnectionFactory().getConnection()
        mycursor = mydb.cursor()

        sql = "DELETE FROM Scenes WHERE code = {}".format(code)
    
        mycursor.execute(sql)

        mydb.commit()

        print("Uma descrição foi cadastrada com sucesso!")

        return True