import mysql.connector as ms


class school:
    def __init__(self):
        self.st_id = ""
        self.st_name = ""
        self.f_name = ""
        self.M_name = ""
        self.st_city = ""
        self.Contact = ""
        self.DOJ = ""

    def connectDb(self):
        conn = ms.connect(host="localhost", user="admin",
                          passwd="1234", database="student")
        if conn.is_connected():
            print("connection established")
            return conn
        else:
            print("Error in connection")

    def checklogin(self, uname, pswd):
        con = self.connectDb()
        cur = con.cursor()
        cur.execute("select * from login")
        row = cur.fetchall()
        for r in row:
            if r[0] == uname and r[1] == pswd:
                print("Access Granted")
            else:
                print("Invalid login id or password")
                username1 = input("Enter User ID:- ")
                pswd1 = input("Enter Password:- ")
                self.checklogin(username1, pswd1)

    def menu(self):
        print("\n--- 1-Add New Student ---")
        print("--- 2-Update Student---")
        print("--- 3-Student Details---")
        print("--- 4-Fees Payment---")
        print("--- 5-Student Fee Details---")
        print("--- 6-Student Conveyance Details---")
        print("--- 0-Exit ---")

    def AddStudent(self):
        self.st_name = input("Enter Student Name:-")
        self.f_name = input("Enter Student Father Name:-")
        self.M_name = input("Enter Student Mother Name:-")
        self.st_city = input("Enter Student's City:-")
        self.Contact = input("Enter  Mobile No:-")
        self.DOJ = input("Enter Admission date:-")
        conn = self.connectDb()
        cur = conn.cursor(buffered=True)
        cur.execute("select * from studentmaster order by st_id desc")
        x = cur.fetchone()
        yy = x[0]
        if x == None:
            cur.execute("insert into studentmaster values(1,'"+self.st_name+"','"+self.f_name +
                        "','"+self.M_name+"','"+self.st_city+"','"+self.Contact+"','"+self.DOJ+"')")
            conn.commit()
            print("New Student Added")
            print("Your Unique Student ID Is:-", "1")
        else:
            stid = (yy)+1
            Unqe_id = stid
            cur.execute("insert into studentmaster values('"+str(stid)+"','"+self.st_name+"','" +
                        self.f_name+"','"+self.M_name+"','"+self.st_city+"','"+self.Contact+"','"+self.DOJ+"')")
            conn.commit()
            print("New Student Added")
            print("Your Unique Student ID Is:-", Unqe_id)
            ch = input("Do You Want ADD  More Student (y/n)")
            if ch == 'y' or ch == 'Y':
                obj.AddStudent()
            else:
                exit

    def UpdateStudent(self):
        self.st_id = input("Enter Student ID:-")
        conn = self.connectDb()
        cur = conn.cursor(buffered=True)
        cur.execute(
            "select St_Id from studentmaster where St_Id='"+self.st_id+"'")
        x = cur.fetchone()
        if x == None:
            print("Student ID Not found")
        else:
            self.N_st_name = input("Enter Student Name:-")
            self.N_F_name = input("Enter Student Father Name:-")
            self.N_M_name = input("Enter Student Mother Name:-")
            self.N_st_city = input("Enter Student's City:-")
            self.N_Contact = input("Enter  Mobile No:-")
            self.N_DOJ = input("Enter Admission date:-")
            conn = self.connectDb()
            cur = conn.cursor(buffered=True)
            cur.execute("update studentmaster set St_name='" +
                        self.N_st_name+"' where st_id='"+self.st_id+"'")
            cur.execute("update studentmaster set f_name='" +
                        self.N_F_name+"'where st_id='"+self.st_id+"'")
            cur.execute("update studentmaster set M_name='" +
                        self.N_M_name+"'where st_id='"+self.st_id+"'")
            cur.execute("update studentmaster set St_city='" +
                        self.N_st_city+"'where st_id='"+self.st_id+"'")
            cur.execute("update studentmaster set Contact='" +
                        self.N_Contact+"'where st_id='"+self.st_id+"'")
            cur.execute("update studentmaster set DOJ='" +
                        self.N_DOJ+"'where st_id='"+self.st_id+"'")
            print("Student Details Updated")
            conn.commit()

            ch = input("Do You Want To Update Any Other Student(y/n)")
            if ch == 'y' or ch == 'Y':
                obj.UpdateStudent()
            else:
                exit

    def StudentDetails(self):
        self.St_Id = input("Enter Student ID:-")
        conn = self.connectDb()
        cur = conn.cursor(buffered=True)
        cur.execute("select * from studentmaster where St_Id='"+self.St_Id+"'")
        x = cur.fetchone()
        if x == None:
            print("Student ID Not found")
            obj.StudentDetails()
        else:
            print("Student Name=", x[1])
            print("Student Father Name=", x[2])
            print("Student Mother Name=", x[3])
            print("Student Student city=", x[4])
            print("Student contact=", x[5])
            print("Student DOJ=", x[6])
            conn.commit()
            ch = input("Do You Want To Show More Student Details(y/n)")
            if ch == 'y' or ch == 'Y':
                obj.StudentDetails()
            else:
                exit

    def FeePayment(self):
        self.st_id = input("Enter Student ID")
        conn = self.connectDb()
        cur = conn.cursor(buffered=True)
        cur.execute("select * from FeeDetails where st_id='" +
                    str(self.st_id)+"'")
        x = cur.fetchall()
        if x == None:
            print("Student ID Not found")
        elif x != None:
            cur.execute(
                "select  Quater from FeeDetails where st_id='"+str(self.st_id)+"'")
            x = cur.fetchall()
            for i in x:
                if i in ['1', '2', '3', '4']:
                    pass
                else:
                    cur.execute(
                        "select St_ID, Year,Penalty,Total  from FeeDetails where St_Id='"+str(self.st_id)+"'")
                    A = cur.fetchone()
                    print("insert into FeeDetails values('"+str(A[0])+"','"+str(
                        A[1])+"','"+str(i[0])+"','"+str(A[2])+"','"+str(A[3])+"')")
                    cur.execute("insert into FeeDetails values('"+str(A[0])+"','"+str(
                        A[1])+"','"+str(i[0:len(i)-1])+"','"+str(A[2])+"','"+str(A[3])+"')")
                    conn.commit()
                    print("Fees Payment is Successfull")
                    cur.execute("select St_ID, Year,Quater,Penalty,Total  from FeeDetails where St_Id='"+str(
                        self.st_id)+"' and Quater="+str(i[0])+"")
                    x1 = cur.fetchall()
                    for B in x1:
                        print("\nStudent ID:-", B[0])
                        print("Year:-", B[1])
                        print("Quater:-", B[2])
                        print("Penalty:-", B[3])
                        print("Total Fees:-", B[4])
                    ch = input("Do You Want To Show Student Fees Details(y/n)")
                    if ch == 'y' or ch == 'Y':
                        obj.StudentFee_Details(self)
                    else:
                        exit

    def StudentFee_Details(self):
        self.st_id = input("Enter Student ID:-")
        conn = self.connectDb()
        cur = conn.cursor(buffered=True)
        cur.execute("select St_ID, Year,Quater,Penalty,Total  from FeeDetails where St_Id='" +
                    str(self.st_id)+"' and quater in ('1','2','3','4')")
        x = cur.fetchall()
        if x == None:
            print("Student ID Not found")
        elif x == []:
            print("No Fee Details Found  In this St_ID")
        else:
            print("---Press 1 for Show Student Fee Details Of All Time----")
            print("---press 2 For Show Student Fee Details Of Particular Year----")
            ask = int(input("Enter Your Choice"))
            cur.execute(
                "select St_ID, Year,Quater,Penalty,Total  from FeeDetails where St_Id='"+str(self.st_id)+"'")
            x = cur.fetchall()
            if ask == 1:
                for i in x:
                    print("\nStudent ID:-", i[0])
                    print("Year:-", i[1])
                    print("Quater:-", i[2])
                    print("Penalty:-", i[3])
                    print("Total Fees:-", i[4])
            elif ask == 2:
                self.Yr = str(input("Enter Year"))
                cur.execute("select * from FeeDetails where St_Id='" +
                            self.st_id+"',year='"+self.Yr+"")
                x2 = cur.fetchall()
                for k in x2:
                    print(x2)
            ch = input("Do You Want To Show  Student Fees Details(y/n)")
            if ch == 'y' or ch == 'Y':
                obj.StudentFee_Details(self)
            else:
                exit


#    def Student_Conveyance(self):
#        self.st_id=input("Enter Student ID:-")
#        conn=self.connectDb()
#        cur=conn.cursor(buffered=True)


print("---- WELCOME TO VIPIN MITTAL PROGRAM-----")
username = input("Enter User ID:- ")
pswd = input("Enter Password:- ")
obj = school()
# obj.checklogin(username,pswd)
ch = 'y'
choice = 1
while choice > 0:
    obj.menu()
    choice = eval(input("Enter your choice:-"))

    if choice == 1:
        obj.AddStudent()

    elif choice == 2:
        obj.UpdateStudent()

    elif choice == 3:
        obj.StudentDetails()

    elif choice == 4:
        obj.FeePayment()

    elif choice == 5:
        obj.StudentFee_Details()

#    elif choice==6:
#      obj.StudentConveyance_Details()

    elif choice == 0:
        exit
    else:
        print("Invalid choice")
        ch = input("Do You Want To Continue(y/n)")
        if ch == 'y' or ch == 'Y':
            obj.menu()
        else:
            exit
            choice = 0
