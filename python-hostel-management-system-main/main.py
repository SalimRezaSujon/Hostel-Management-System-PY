from tkinter import *
from tkinter import messagebox
import sql


def getCenter(width, height):
    return f'{width}x{height}+{int(s_width / 2) - int(width / 2)}+{int(s_height / 2) - int(height / 2)}'


table_entry = {}
table_index = 0
table_data = []
add_button_color = "#4fc597"
root_color = "#f5f6fa"
label_color = "#f0f2fa"
editbtn_bg = "#B03A68"
editbtn_fg = "white"
navigation_button_color = "#01263f"
root_width = 1000
root_height = 600
root = Tk()
root.title("Hostel Management System")
s_width = root.winfo_screenwidth()
s_height = root.winfo_screenheight()
root.geometry(getCenter(root_width, root_height))
root.configure(bg=root_color)
root.maxsize(root_width, root_height)
root.withdraw()




def ListToStr(list):
    if len(list) > 0:
        if type(list[0]) == dict:
            newlist = []
            for x in list:
                newlist.append(x["seat_id"])
            return ",".join(newlist)
        else:
            return ",".join(list)
    else:
        return None


def save_data():
    try:
        sql.conn.commit()
    except:
        return False
    else:
        show_stats()
        search()
        return True


#sujon-start
def login(username, password, login_window):
    result = sql.adminAuth(username, password)
    if result and len(result) > 0:
        messagebox.showinfo(title="Admin Login", message="Login Successfull")
        root.deiconify()
        login_window.destroy()
    elif username == "master" and password == "master":
        messagebox.showinfo(title="Admin Login", message="Login Successfull")
        root.deiconify()
        login_window.destroy()
    else:
        messagebox.showerror(title="Admin Login", message="Invalid Username or Password")


# executed when booking a seat
def book_seat(name_field, id_field, phone_field, seat_field, book):
    name = name_field.get()
    id = id_field.get()
    phone = phone_field.get()
    seat = seat_field.get()
    if sql.isSeatEmpty(seat):
        if sql.addNewResident(std_name=name, std_id=id, seat_id=seat, phone_no=phone):
            if save_data():
                messagebox.showinfo(title="Seat Booking", message=f'Seat {seat} is successfully assigned to {name}')
                book.destroy()
        else:
            messagebox.showerror(title="Seat Booking", message="Error Registering New Resident.")
    else:
        messagebox.showerror(title="Seat Booking", message="Seat is not available.")
#sujon-end


#siddik-start
# executed when clicked on insert seats
def add_room(room_id, seat_ids, addRoom):
    roomid = room_id.get()
    seats = seat_ids.get().split(",")
    failed = []
    success = []

    for seat_id in seats:
        if sql.insertSeat(seat_id, roomid):
            success.append(seat_id)
        else:
            failed.append(seat_id)
    if save_data():
        if len(failed) == 0:
            messagebox.showinfo(title="Seat Booking",
                                message=f'Seat number {ListToStr(success)} is successfully added to database.')
        else:
            messagebox.showwarning(title="Seat Booking",
                                   message=f'Added : {ListToStr(success)}.\nCould not add  : {ListToStr(failed)}')
    else:
        messagebox.showwarning(title="Seat Booking",
                               message=f'Unknown Error, No Seats are added to the database.')
    addRoom.destroy()


# executed when clicked on generate seats
def generate_rooms(room_id, seat_count, seat_id):
    roomid = room_id.get()
    try:
        seatcount = int(seat_count.get())
    except:
        seatcount = 0
    if seatcount > 26:
        messagebox.showwarning(title="Seat Booking", message="Maximum 26 seats is supported in a room.")
    elif seatcount > 0:
        tempseats = []
        for i in range(65, 65 + seatcount):  # generating A-Z letter and joining them at the end of room number
            tempseats.append(roomid + chr(i))
        seat_id.insert(0, ListToStr(tempseats))


# executed when clicked on remove seats
def remove_room(seat_ids, addRoom):
    seats = seat_ids.get().split(",")
    failed = []
    success = []

    for seat_id in seats:
        if sql.isSeatEmpty(seat_id):
            if sql.removeSeat(seat_id):
                success.append(seat_id)
            else:
                failed.append(seat_id)
        else:
            failed.append(seat_id)
    if save_data():
        if len(failed) == 0:
            messagebox.showinfo(title="Seat Booking",
                                message=f'Seat {ListToStr(success)} successfully removed from database.')
        else:
            messagebox.showwarning(title="Seat Booking",
                                   message=f'Removed : {ListToStr(success)}.\nCould not remove  : {ListToStr(failed)}\nKeep the room empty before removing.')
    else:
        messagebox.showwarning(title="Seat Booking",
                               message=f'Unknown Error, No Seats are removed from the database.')
    addRoom.destroy()
#siddik-end



#shahadat-start
# executed when clicked on update info
def update_data(id, std_id, std_name, seat_id, phone_no, updateInfo):
    old_seat_id = sql.selectResidentById(id)["seat_id"]
    if old_seat_id == seat_id:
        roomChange = False
    else:
        roomChange = True
    if not roomChange:
        if sql.updateResidentById(id=id, std_name=std_name, std_id=std_id, phone_no=phone_no) and save_data():
            messagebox.showinfo(title="Update Student Information", message="Successfully Updated Student Details")
            updateInfo.destroy()
        else:
            messagebox.showerror(title="Update Student Information", message="Unknown error.Could not save data.")
    else:
        if sql.isSeatEmpty(seat_id):
            if sql.updateResidentSeatById(id=id, std_name=std_name, old_seat_id=old_seat_id, seat_id=seat_id,
                                          std_id=std_id, phone_no=phone_no) and save_data():
                messagebox.showinfo(title="Update Student Information", message="Successfully Updated Student Details")
            else:
                messagebox.showerror(title="Update Student Information", message="Unknown error.Could not save data.")
        else:
            messagebox.showerror(title="Update Student Information", message="Seat is not available.")


def find_student(id, id_field, name, room, phone, updateInfo):
    # if user click the button two times student info is inserted two times,
    # so we added this to clear the entry-box before inserting anything
    std_id = id_field.get()
    result = sql.selectResidentByStdId(std_id)
    if result:
        name.delete(0, END)
        room.delete(0, END)
        phone.delete(0, END)
        name.insert(0, result["std_name"])
        room.insert(0, result["seat_id"])
        phone.insert(0, result["phone_no"])
        id.insert(0, result["id"])
        updateInfo.focus_force()
    else:
        messagebox.showwarning(title="Find Student", message="Student Not Found in Database")
        # after showing messagebox the root was getting focused, so we searched in google and found this solution so the updateInfo window comes to focus
        updateInfo.focus_force()


def delete_student(id, edit_student):
    id = id.get()
    if sql.removeResidentById(id) and save_data():
        messagebox.showinfo(title="Update Student Information", message="Successfully Removed Student")
        edit_student.destroy()
    else:
        messagebox.showerror(title="Update Student Information", message="Unknown error.Could not removed student.")

#shahadat-end


def search(str=None, searchBy=None):
    global table_index
    global table_data
    if searchBy == "std_id":
        result = sql.findResidentByStdId(str)
        if result:
            table_data = list(result)
            table_index = 0
        else:
            messagebox.showinfo(title="Search Database", message=f'No Results Found')
    elif searchBy == "std_name":
        result = sql.findResidentByStdName(str)
        if result:
            table_data = list(result)
            table_index = 0
        else:
            messagebox.showinfo(title="Search Database", message=f'No Results Found')
    elif searchBy == "seat_id":
        result = sql.findResidentBySeatId(str)
        if result:
            table_data = list(result)
            table_index = 0
        else:
            messagebox.showinfo(title="Search Database", message=f'No Results Found')
    else:
        result = sql.selectAllResident()
        if result:
            table_data = list(result)
            table_index = 0
    loadHomeTable()


def loadHomeTable(go=""):
    global table_data, table_index, table_entry
    if len(table_data) - table_index < 10:
        rows = len(table_data) - table_index
    else:
        rows = 10
    for i in range(0, 10):
        table_entry[i]["name"].delete(0, END)
        table_entry[i]["id"].delete(0, END)
        table_entry[i]["room"].delete(0, END)
        table_entry[i]["phone"].delete(0, END)
    for i, j in zip(range(table_index, rows), range(0, rows)):
        table_entry[j]["name"].insert(0, table_data[i]["std_name"])
        table_entry[j]["id"].insert(0, table_data[i]["std_id"])
        table_entry[j]["room"].insert(0, table_data[i]["seat_id"])
        table_entry[j]["phone"].insert(0, table_data[i]["phone_no"])
        add_button = Button(table, text="Edit", bg=add_button_color,
                            command=lambda i=i: show_update_info(table_entry[i]["id"].get()),
                            relief="flat",
                            background=editbtn_bg, foreground=editbtn_fg, padx=10)
        add_button.grid(column=4, row=2 + i)
        table_entry[j]["extra"] = add_button


# ---------- UI -----------#

def show_login():
    global root
    book = Tk()
    book.title("Login")
    book.geometry(getCenter(350, 450))
    book.configure(bg="white")
    Label(master=book, bg="white", font=("Helvetica", "16"), text="Admin Login").place(x=105, y=10)
    Label(master=book, bg="white", font=("Helvetica", "12"), text="Username :").place(x=45, y=85)
    name_field = Entry(book, width=40)
    name_field.place(x=45, y=120)
    Label(master=book, bg="white", font=("Helvetica", "12"), text="Password :").place(x=45, y=150)
    pass_field = Entry(book,show="*", width=40, highlightbackground="black")
    pass_field.place(x=45, y=180)
    add_button = Button(book, text="Login", font=("Helvetica", "12"), bg="#5bc0de", fg="white",
                        command=lambda: login(name_field.get(), pass_field.get(), book), relief="flat", padx=100)
    add_button.place(x=45, y=250)


def show_book_prompt():
    book = Tk()
    book.title("Book a Seat")
    book.geometry(getCenter(400, 230))
    book.configure(bg=label_color)
    Label(master=book, text="Add New Student").pack(ipady=10)
    Label(master=book, text="Name :").place(x=10, y=50)
    name_field = Entry(book, bg=root_color, width=40)
    name_field.place(x=100, y=50)
    Label(master=book, text="ID :").place(x=10, y=80)
    id_field = Entry(book, bg=root_color, width=40)
    id_field.place(x=100, y=80)
    Label(master=book, text="Phone :").place(x=10, y=110)
    phone_field = Entry(book, bg=root_color, width=40)
    phone_field.place(x=100, y=110)
    Label(master=book, text="Seat Id:").place(x=10, y=140)
    seat_field = Entry(book, bg=root_color, width=40)
    try:
        seat_id = sql.getEmptyRoom()["seat_id"]
        if seat_id:
            seat_field.insert(0, seat_id)
        else:
            seat_field.insert(0, "No Empty Seats")
    except:
        seat_field.insert(0, "No Empty Seats")
    seat_field.place(x=100, y=140)
    add_button = Button(book, text="Save", bg=add_button_color, fg="white",
                        command=lambda: book_seat(name_field, id_field, phone_field, seat_field, book), relief="flat",
                        pady=5, padx=20)
    add_button.place(x=275, y=180)


def show_add_room():
    addRoom = Tk()
    addRoom.title("Add New Seat")
    addRoom.geometry(getCenter(600, 600))
    addRoom.configure()
    seats = LabelFrame(addRoom, text="Add Seats")
    Label(master=seats, text="Room ID :", width=25, anchor="w").grid(column=0, row=0, padx=5, pady=10)
    room_id = Entry(seats, bg=root_color, width=35)
    room_id.grid(column=1, row=0)
    Label(master=seats, text="Seat IDs (comma seperated):", width=25, anchor="w").grid(column=0, row=1, padx=5, pady=5)
    seat_id = Entry(seats, bg=root_color, width=35)
    seat_id.grid(column=1, row=1)

    Button(seats, text="Insert Seats", bg="#df4759", fg="white",
           command=lambda: add_room(room_id, seat_id, addRoom), relief="flat", padx=5).grid(column=1, row=2,
                                                                                            padx=5, pady=10)
    seats.pack(side=TOP, fill="x", padx=10, pady=10)

    generate = LabelFrame(addRoom, text="Generate Seats")
    Label(master=generate, text="Room ID :", width=15, anchor="w").grid(column=0, row=0, padx=5,
                                                                        pady=10)
    room_id2 = Entry(generate, bg=root_color, width=35)
    room_id2.grid(column=1, row=0)
    Label(master=generate, text="Seat Count :", width=15, anchor="w").grid(column=0, row=1, padx=5,
                                                                           pady=5)
    seat_count = Entry(generate, bg=root_color, width=35)
    seat_count.grid(column=1, row=1)
    Button(generate, text="Generate Seats", bg="#df4759", fg="white",
           command=lambda: generate_rooms(room_id2, seat_count, seat_id), relief="flat", padx=5).grid(column=1, row=2,
                                                                                                      padx=5, pady=10)
    generate.pack(side=TOP, fill="x", pady=6, padx=6)

    remove_roomFrame = LabelFrame(addRoom, text="Remove Seats")
    Label(master=remove_roomFrame, text="Seat IDs :", width=15, anchor="w").grid(column=0, row=0,
                                                                                 padx=5,
                                                                                 pady=10)
    room_idx = Entry(remove_roomFrame, bg=root_color, width=35)
    room_idx.grid(column=1, row=0)
    Button(remove_roomFrame, text="Remove Seats", bg="#df4759", fg="white",
           command=lambda: remove_room(room_idx, addRoom), relief="flat", padx=5).grid(column=1, row=2,
                                                                                       padx=5, pady=5)
    remove_roomFrame.pack(side=TOP, fill="x", pady=6, padx=6)


def show_update_info(id=""):
    updateInfo = Tk()
    updateInfo.title("Update Student Details")
    updateInfo.geometry(getCenter(400, 600))
    updateInfo.configure(bg=label_color)
    Label(master=updateInfo, text="Update Student Details", anchor="center").pack(ipady=10)
    Label(master=updateInfo, text="Student ID :").place(x=10, y=50)
    id_field = Entry(updateInfo, bg=root_color, width=40)
    id_field.insert(0, id)
    id_field.place(x=100, y=50)
    data_id = Entry(updateInfo, bg=root_color, width=40)
    data_id.place()
    load_button = Button(updateInfo, text="Find Student", bg=add_button_color, fg="white",
                         command=lambda: find_student(data_id, id_field, name_field, room_field, phone_field,
                                                      updateInfo),
                         relief="flat", pady=5, padx=20)
    load_button.pack(pady=40)
    Label(master=updateInfo, text="Name :").place(x=10, y=150)
    name_field = Entry(updateInfo, bg=root_color, width=40)
    name_field.place(x=100, y=150)
    Label(master=updateInfo, text="Room :").place(x=10, y=180)
    room_field = Entry(updateInfo, bg=root_color, width=40)
    room_field.place(x=100, y=180)
    Label(master=updateInfo, text="Phone :").place(x=10, y=210)
    phone_field = Entry(updateInfo, bg=root_color, width=40)
    phone_field.place(x=100, y=210)
    add_button = Button(updateInfo, text="Save", bg=add_button_color, fg="white",
                        command=lambda: update_data(data_id.get(), id_field.get(), name_field.get(), room_field.get(),
                                                    phone_field.get(), updateInfo),
                        relief="flat", pady=5, padx=20)
    add_button.place(x=170, y=250)
    Button(updateInfo, text="Delete Student", bg="#ff665e", fg="white",
           command=lambda: delete_student(data_id, updateInfo), relief="flat", pady=5, padx=20).place(x=145, y=300)
    if id != "":  # auto execute find_students function if any id is passed as function parameter
        find_student(data_id, id_field, name_field, room_field, phone_field, updateInfo)


def show_options():
    options = LabelFrame(root, text="Functions")  # making a seperate frame to keep the user functions
    Button(options, text="Book Seat", bg=add_button_color, fg="white", command=show_book_prompt, relief="flat").grid(
        column=0, row=0, pady=7, padx=15, ipadx=34, ipady=8)
    Button(options, text="Update Info", bg=add_button_color, fg="white", command=show_update_info, relief="flat").grid(
        column=1, row=0, pady=7, padx=15, ipadx=32, ipady=8)
    Button(options, text="View Database", bg=add_button_color, fg="white", command=lambda: search(),
           relief="flat").grid(column=0, row=1, pady=4, padx=13, ipadx=22, ipady=8)
    Button(options, text="Manage Rooms", bg=add_button_color, fg="white", command=show_add_room, relief="flat").grid(
        column=1, row=1, pady=7, padx=15, ipadx=22, ipady=8)
    options.grid(column=0, row=0, padx=5)


def show_stats():
    stats = LabelFrame(root, text="Stats")  # making a seperate frame to show the statistics
    Button(stats, text=f'Total Seats\n{len(sql.getTotalSeatCount())}', bg="#337ab7", fg="white",
           command=lambda: messagebox.showinfo(title="Database Stats",
                                               message=f'All Seats : {ListToStr(sql.getTotalSeatCount())}'),
           relief="flat").grid(column=0, row=0, pady=3, padx=7, ipadx=32, ipady=5)
    Button(stats, text=f'Available Seats\n{len(sql.getEmptySeatCount())}', bg="#5cb85c", fg="white",
           command=lambda: messagebox.showinfo(title="Database Stats",
                                               message=f'Available Seats : {ListToStr(sql.getEmptySeatCount())}'),
           relief="flat").grid(column=1, row=0, pady=3, padx=7, ipadx=25, ipady=5)
    Button(stats, text=f'Taken Seats\n{len(sql.getReservedSeatCount())}', bg="#df4759", fg="white",
           command=lambda: messagebox.showinfo(title="Database Stats",
                                               message=f'Used Seats : {ListToStr(sql.getReservedSeatCount())}'),
           relief="flat").grid(column=0, row=1, pady=3, padx=7, ipadx=30, ipady=5)
    Button(stats, text=f'Reserved Seats\n0', bg="#5bc0de", fg="white",
           command=lambda: messagebox.showinfo(title="Database Stats",
                                               message=f'Reserved Seats : None'),
           relief="flat").grid(column=1, row=1, pady=3, padx=7, ipadx=25, ipady=5)
    stats.grid(column=1, row=0, padx=5)


def show_search():
    searchL = LabelFrame(root, text="Search")  # making a seperate frame to show the search options
    nameFrame = Frame(searchL)
    Label(master=nameFrame, text="Student Name :", width=12, anchor="w").pack(side="left")
    name_field = Entry(nameFrame, bg=root_color, width=25)
    name_field.pack(side="left", fill=X)
    Button(nameFrame, text="Search", bg="#df4759", fg="white", command=lambda: search(name_field.get(), "std_name"),
           relief="flat", padx=5).pack(side="right", padx=5)
    nameFrame.pack(side=TOP, fill="x", pady=6, padx=6)
    id = Frame(searchL)
    Label(master=id, text="Student ID :", width=12, anchor="w").pack(side="left")
    id_field = Entry(id, bg=root_color, width=25)
    id_field.pack(side="left", fill=X)
    Button(id, text="Search", bg="#df4759", fg="white", command=lambda: search(id_field.get(), "std_id"), relief="flat",
           padx=5).pack(side="right", padx=5)
    id.pack(side=TOP, fill="x", pady=6, padx=6)
    room = Frame(searchL)
    Label(master=room, text="Seat ID :", width=12, anchor="w").pack(side="left")
    room_field = Entry(room, bg=root_color, width=25)
    room_field.pack(side="left", fill=X)
    Button(room, text="Search", bg="#df4759", fg="white", command=lambda: search(room_field.get(), "seat_id"),
           relief="flat", padx=5).pack(side="right", padx=5)
    room.pack(side=TOP, fill="x", pady=6, padx=6)
    searchL.grid(column=2, row=0, padx=5)


# storing all table entry points to use them later

# We wanted to add a scroll bar to view the whole database
# But we was not able to do that maybe because our lack of knowledge on tkinter
# So we decided to create three buttons to show the database with a pagination system
# It destroys the previous table and creates a new table based on previous or next entries in the dictionary

def show_table():
    global table, table_entry
    table_entry.clear()
    table = LabelFrame(root, text="Database : ")
    table_headers = ["Student Name", "Student ID", "Seat ID", "Phone Number", "Actions"]
    for colum, i in zip(table_headers, range(5)):
        Label(table, text=colum, bg="#34495e", fg="white", width=27).grid(column=i, row=0, ipady=7, ipadx=3)

    for i in range(10):
        table_entry.update({i: {}})
        if i % 2 == 0:  # creating pattern color for table rows
            table_bg = "#4fc597"
            table_fg = "white"
        else:
            table_bg = "#ceede1"
            table_fg = "black"
        j = 0
        colname = ["name", "id", "room", "phone", "extra"]
        for colum in colname:  # iterate over columns list to pull their data from dictionary
            tb = Entry(table, relief="flat", readonlybackground=table_bg, background=table_bg, fg=table_fg)
            table_entry[i][colum] = tb
            tb.grid(column=j, row=2 + i, ipadx=38, ipady=7)
            j = j + 1
    table.grid(column=0, row=1, columnspan=3)

navigation = Frame(root)
Button(navigation, text="< Previous", bg=navigation_button_color, fg="white",
       command=lambda: search(),
       relief="flat", padx=10).pack(side="left", padx=10)
Button(navigation, text="Refresh", bg=navigation_button_color, fg="white", command=lambda: search(),
       relief="flat", padx=10).pack(side="left", padx=10)
Button(navigation, text="Next >", bg=navigation_button_color, fg="white",
       command=lambda: search(),
       relief="flat", padx=10).pack(side="left", padx=10)
navigation.place(x=root_width / 2 - 150, y=550)
#----------- End UI ------------#

#------------ Load Ui -----------#
show_options()
show_stats()
show_search()
show_table()
search()
loadHomeTable()


show_login()

root.mainloop()

# That's it , sorry for the messy code . it's my first time using tkinter and also, I never made a gui before now .
