import pymysql

host     = "localhost"
user     = "root"
password = ""
db       = "biyometri"

db_connect = pymysql.connect(host,user,password,db)
cursor = db_connect.cursor()






