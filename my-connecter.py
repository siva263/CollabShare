import mysql.connector
import app

try:
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'mysqlcodesharing',
        password = 'Mysqlsiva26%',
        port = '3306',
        database = 'code_sharing_system'
    )
    record=py.load(open('app.py'))
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO usermast ( name, lastname, emailid, passwords, confrimpassword) VALUES (%s, %s, %s, %s, %s) ",(name,lastname,email,password,confpassword) )
    mydb.commit()
    print(mycursor.rowcount, "Record inserted successfully into Laptop table")

except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))
finally:
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySQL connection is closed")



