import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    db="hosteldb"
)
db = conn.cursor(dictionary=True)


def adminAuth(username, password):
    sql = f"select * from user where username='{username}' and password='{password}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchone()


# add new resident in hostel(book seat)
def addNewResident(std_name, std_id, seat_id, phone_no):
    if reserveSeat(seat_id, std_id):
        sql = "insert into resident (std_name,std_id,seat_id,phone_no) values(%s,%s,%s,%s)"
        value = (std_name, std_id, seat_id, phone_no)
        try:
            db.execute(sql, value)
        except:
            return False
        else:
            return True
    else:
        return False



# update resident info using unique id(update info)
def updateResidentById(id, std_name, std_id, phone_no):
    id = int(id)
    sql = f"update resident set std_name='{std_name}',std_id='{std_id}',phone_no='{phone_no}' where id={id}"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return True


# update resident info including seat using unique id(update info)
def updateResidentSeatById(id, std_name, std_id, old_seat_id, seat_id, phone_no):
    id = int(id)
    sql = f"update resident set std_name='{std_name}',std_id='{std_id}',seat_id='{seat_id}',phone_no='{phone_no}' where id={id}"
    try:
        db.execute(sql)
    except:
        return False
    else:
        if setSeatEmpty(old_seat_id):
            if reserveSeat(seat_id, std_id):
                return True
            else:
                return False
        else:
            return False


# remove resident from database using id
def removeResidentById(id):
    id = int(id)
    db.execute(f"select seat_id from resident where id={id}")
    seat_id = db.fetchone()
    sql = f"delete from resident where id={id}"
    try:
        db.execute(sql)
    except:
        return False
    else:
        sql = f"update room set std_id=NULL where seat_id='{seat_id['seat_id']}'"
        try:
            db.execute(sql)
        except:
            return False
        else:
            return True


# return all resident info from database
def selectAllResident():
    sql = f"select * from resident"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# return resident info from database using id
def selectResidentById(id):
    sql = f"select * from resident where id={id}"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchone()


# return resident info from database using student id
def selectResidentByStdId(std_id):
    sql = f"select * from resident where std_id='{std_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchone()


# set an seat to empty
def setSeatEmpty(seat_id):
    sql = f"update room set std_id=NULL where seat_id='{seat_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return True


# check if a seat is empty
def isSeatEmpty(seat_id):
    sql = f"select std_id from room where seat_id='{seat_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        res = db.fetchone()
        if res != None and res["std_id"] == None:
            return True
        else:
            return False


# reserve a seat for a student
def reserveSeat(seat_id, std_id):
    sql = f"update room set std_id='{std_id}' where seat_id='{seat_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return True


# insert new seat into room table
def insertSeat(seat_id, room_id):
    sql = "insert into room (seat_id,room_id) values(%s,%s)"
    value = (seat_id, room_id)
    try:
        db.execute(sql, value)
    except:
        return False
    else:
        return True


# remove a seat from room table
def removeSeat(seat_id):
    sql = f"delete from room where seat_id='{seat_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return True


# find resident by student name
def findResidentByStdName(std_name):
    sql = f"select * from resident where std_name='{std_name}' or  std_name LIKE '%{std_name}' or  std_name LIKE  '{std_name}%'  or  std_name LIKE '%{std_name}%' "
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# find resident by student id
def findResidentByStdId(std_id):
    sql = f"select * from resident where std_id='{std_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# find resident by seat id
def findResidentBySeatId(seat_id):
    sql = f"select * from resident where seat_id='{seat_id}'"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# fetching info from table based on id
def getInfoFromDb(id):
    sql = f"select * from resident where id>='{id}' order by id limit 10"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# fetching previous 10 info from table based on id
def getPrevInfoFromDb(id):
    sql = f"select * from resident where id<='{id}' order by id limit 10"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# return an empty seat from room table
def getEmptyRoom():
    sql = f"select seat_id from room where std_id is NULL limit 1"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchone()


# get total empty seat count
def getEmptySeatCount():
    sql = f"select seat_id from room where std_id is NULL"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# get total taken seat count
def getReservedSeatCount():
    sql = f"select seat_id from room where std_id is not NULL"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()


# get total seat count
def getTotalSeatCount():
    sql = f"select seat_id from room"
    try:
        db.execute(sql)
    except:
        return False
    else:
        return db.fetchall()

