from mysql.connector import connect
import os

# flask
cnx = connect(host="127.0.0.1", port=3306, user=os.environ.get("DATABASE_USER") or "root", password=os.environ.get("DATABASE_PASSWORD") or "mypassword", database="flask")
cursor = cnx.cursor()

cursor.execute("CREATE TABLE persons(id INT PRIMARY KEY auto_increment, value JSON not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
cursor.execute("CREATE TABLE birthdays(id INT PRIMARY KEY auto_increment, value JSON not null);")
cursor.execute("CREATE TABLE percentiles(id INT PRIMARY KEY auto_increment, value JSON not null, date datetime not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
cursor.execute("CREATE TABLE booleans(id INT PRIMARY KEY auto_increment, birthday_bool  tinyint(1) not null, percentile_bool  tinyint(1) not null);")

cnx.commit()
cursor.close()
cnx.close()


# flasky
cnx = connect(host="127.0.0.1", port=3306, user="root", password=os.environ.get("DATABASE_PASSWORD") or "mypassword", database="flasky")
cursor = cnx.cursor()


cursor.execute("CREATE TABLE persons(id INT PRIMARY KEY auto_increment, value JSON not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
cursor.execute("CREATE TABLE birthdays(id INT PRIMARY KEY auto_increment, value JSON not null);")
cursor.execute("CREATE TABLE percentiles(id INT PRIMARY KEY auto_increment, value JSON not null, date datetime not null) CHARACTER SET utf8 COLLATE utf8_general_ci;")
cursor.execute("CREATE TABLE booleans(id INT PRIMARY KEY auto_increment, birthday_bool  tinyint(1) not null, percentile_bool  tinyint(1) not null);")

cnx.commit()
cursor.close()
cnx.close()
