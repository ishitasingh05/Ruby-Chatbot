import mysql.connector

def executequery(id):
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "ishi@2308",
        database = "Rasa_chatbot"
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT Name, Phone_number, Status FROM Rasa_data WHERE ID='{id}'")

    result = mycursor.fetchall()

    return result



if __name__ == "__main__":
    m = executequery('eMJyN2AQ')
    print(m)


