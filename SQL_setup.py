import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="drdecardinalco@localhost",
  passwd="Stanford1885",
  database="d_rde_cardinal_comfort"
)

print(mydb)
