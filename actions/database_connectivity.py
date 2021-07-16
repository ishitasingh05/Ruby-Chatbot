import mysql.connector
from actions.unique_id import random_generator_id


def dataupdate(id, name, email_id, phone_number, service, information):
    data = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "ishi@2308",
        database = "Rasa_chatbot"
    )

    mycursor = data.cursor()

    #sql = "CREATE TABLE Rasa_data(ID VARCHAR(16), Name VARCHAR(40), Email_id VARCHAR(40), Phone_number BIGINT, Service VARCHAR(40), Information VARCHAR(200), Status VARCHAR(200))"
    sql = f"INSERT INTO Rasa_data(ID, Name, Email_id, Phone_number, Service, Information) VALUES ('{id}', '{name}', '{email_id}', {phone_number}, '{service}', '{information}');"
    mycursor.execute(sql)

    data.commit()
    print(mycursor.rowcount, "Record Inserted")



if __name__ == "__main__":
    m = random_generator_id()
    dataupdate(m, "Sana", "sana.singh@gmail.com", 9334615376, "Feedback", "The service can be made better.",)