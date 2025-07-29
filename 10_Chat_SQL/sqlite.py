import sqlite3

# Connect to sqlite 
connection = sqlite3.connect('student.db')

## Create a cursor object to insert record and create table 
cursor = connection.cursor()

# create a table 

table_info = '''
create table STUDENT(NAME VARCHAR(25) , 
                    CLASS VARCHAR(25), 
                    SECTION VARCHAR(25), 
                    MARKS INT)
'''

cursor.execute(table_info)


## Insert record into table

cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Ovi', '10th', 'A', 60)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Ritik', '11th', 'B', 10)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Vivek', '10th', 'B', 66)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Abbaya', '11th', 'B', 10)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Om', '11th', 'A', 90)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Raju', '10th', 'B', 95)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Viraj', '11th', 'A', 13)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Abhi', '11th', 'A', 10)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Omkar', '10th', 'G', 100)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Rahul', '11th', 'G', 10)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Vijay', '10th', 'G', 10)")
cursor.execute("INSERT INTO STUDENT(NAME, CLASS, SECTION, MARKS) VALUES ('Abhishek', '11th', 'G', 16)")


## Display all the records in table

print("All the records in table")
for row in cursor.execute("SELECT * FROM STUDENT"):
    print(row)



# Close the connection to the database commit
connection.commit()
connection.close()