import MySQLdb as mysql
DB_HOST = '10.129.149.7'
DB_READER = 'reader'
DB_WRITER = 'writer'
DB_PSWD = 'datapool'
DB = 'datapool'
sql = "select * from temperature_sensors"
results=[]
try:
        con = mysql.connect( DB_HOST, DB_READER, DB_PSWD, DB )
        cursor = con.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        # print results
        if len(results) == 0:
            print 'Empty result set after query execution at %0.3f' % time.time()
except mysql.MySQLError, e:
        print "error"


# print results[1]

import sqlite3
db=sqlite3.connect('abc.sql')
cursor=db.cursor()
# # cursor.execute('''CREATE TABLE sensors (sensorID TEXT PRIMARY KEY, zone INTEGER, lane INTEGER, class INTEGER)''')
# for res in results:
#      sql_="INSERT INTO sensors (sensorID, zone , lane , class) VALUES ("+ "'"+str(res[0])+"'"  +","+str(int(res[1]))+","+str(int(res[2]))+","+str(int(res[3])) +")"
#      print sql_
#      # break
#      cursor.execute(sql_)
cursor.execute('''SELECT * FROM sensors where class =205''')
all_rows = cursor.fetchall()
print all_rows
#
#
# db.commit()
db.close()
