import mysql.connector as ms
import sys

class Student:
    def __init__(self):
        self.st_id = ""
        self.st_name = ""
        self.f_name = ""
        self.M_name = ""
        self.st_city = ""
        self.Contact = ""
        self.DOJ = ""
        self.conn = self.connectDb()

    def connectDb(self):
        while True:
            username = input("Enter User ID:- ")
            pswd = input("Enter Password:- ")

            try:
                conn = ms.connect(host="localhost", user=username, passwd=pswd)
                if conn.is_connected():
                    print("Connection established")
                    self.checkSchema(conn)
                    return conn
            except ms.Error as e:
                print("Error in connection. Enter your details again...")

    def checkSchema(self, conn):
        cur = conn.cursor()
        try:
            cur.execute("USE student")
            print("Connected to 'student' database.")
        except ms.Error as error:
            print(f"Error: {error}")
            try:
                cur.execute("CREATE DATABASE student")
                cur.execute("USE student")
                print("Created 'student' database.")
            except ms.Error as create_error:
                print(f"Error creating 'student' database: {create_error}")
                return

        cur.execute("SHOW TABLES LIKE 'login'")
        if cur.fetchone() is None:
            try:
                cur.execute("""CREATE TABLE login (
                    uname VARCHAR(20) NOT NULL UNIQUE,
                    pswd VARCHAR(20) NOT NULL UNIQUE
                );""")
                print("login table created")
            except ms.Error as create_error:
                print(f"Error creating 'login' table : {create_error}")

        cur.execute("SHOW TABLES LIKE 'studentmaster'")
        if cur.fetchone() is None:
            try:
                cur.execute("""CREATE TABLE studentmaster (
                    st_id INT AUTO_INCREMENT PRIMARY KEY,
                    st_name VARCHAR(255) NOT NULL,
                    f_name VARCHAR(255) NOT NULL,
                    m_name VARCHAR(255) NOT NULL,
                    st_city VARCHAR(255) NOT NULL,
                    contact VARCHAR(20) NOT NULL,
                    doj DATE NOT NULL
                );""")
                print("studentmaster table created")
            except ms.Error as create_error:
                print(f"Error creating 'studentmaster' table : {create_error}")

        cur.execute("SHOW TABLES LIKE 'FeeDetails'")
        if cur.fetchone() is None:
            try:
                cur.execute("""CREATE TABLE FeeDetails (
                    FeeDetailID INT AUTO_INCREMENT PRIMARY KEY,
                    st_id INT,
                    Year INT,
                    Semester VARCHAR(20),
                    PaymentAmount DECIMAL(10, 2),
                    FOREIGN KEY (st_id) REFERENCES studentmaster(st_id)
                );""")
                print("FeeDetails table created")
            except ms.Error as create_error:
                print(f"Error creating 'FeeDetails' table : {create_error}")

        conn.commit()

    def checklogin(self):
        cur = self.conn.cursor()
        exitFlag = 0
        while True:
            username = input("Enter login ID:- ")
            pswd = input("Enter Password:- ")

            cur.execute("SELECT * FROM login where uname = '" + username + "' and pswd = '" + pswd + "'")
            rows = cur.fetchone()

            if rows is not None:
                print("Access Granted")
                break
            else:
                print("Invalid login id or password")
                opt = input("Do you want to create new login credentials[1] or retry again[2]?")

                if opt == "1":
                    try:
                        newUsername = input("Enter Username:- ")
                        newpswd = input("Enter Password:- ")
                        cur.execute("INSERT INTO login VALUES('" + newUsername + "', '" + newpswd + "')")
                        self.conn.commit()
                    except ms.Error as create_error:
                        print(f"Error add login credentials : {create_error}")
                        exitFlag = 1
                    break
        return exitFlag

    def menu(self):
        print("\n--- 1-Add New Student ---")
        print("--- 2-Update Student---")
        print("--- 3-Student Details---")
        print("--- 4-Fees Payment---")
        print("--- 5-Student Fee Details---")
        print("--- 0-Exit ---")

    def AddStudent(self):
        n = int(input("Enter No. of Student to be added:- "))
        insertCmnd = "insert into studentmaster(st_name, f_name, m_name, st_city, contact, doj) values"
        for i in range(n):
           print("Enter Details of " + str(i+1) + " student....")
           st_name = input("Enter Student Name:-")
           f_name = input("Enter Student Father Name:-")
           M_name = input("Enter Student Mother Name:-")
           st_city = input("Enter Student's City:-")
           Contact = input("Enter Mobile No:-")
           DOJ = input("Enter Admission date:-(yyyy/mm/dd)")
           insertCmnd = insertCmnd + "('" + st_name+"','"+f_name +"','"+M_name+"','"+st_city+"','"+Contact+"','"+DOJ+"'),"
        
        cur = self.conn.cursor(buffered=True)
        cur.execute(insertCmnd[:len(insertCmnd)-1])
        self.conn.commit()
        print("All Students Added")
            

    def UpdateStudent(self):
        while True:
            self.st_id = input("Enter Student ID (or type 'exit' to stop updating): ")

            if self.st_id.lower() == 'exit':
                break

            cur = self.conn.cursor(buffered=True)
            cur.execute("select St_Id from studentmaster where St_Id='"+self.st_id+"'")
            x = cur.fetchone()

            if x is None:
                print("Student ID Not found")
            else:
                self.N_st_name = input("Enter Student Name:-")
                self.N_F_name = input("Enter Student Father Name:-")
                self.N_M_name = input("Enter Student Mother Name:-")
                self.N_st_city = input("Enter Student's City:-")
                self.N_Contact = input("Enter Mobile No:-")
                self.N_DOJ = input("Enter Admission date:-(yyyy/mm/dd)")

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
                self.conn.commit()

                ch = input("Do You Want To Update Another Student? (y/n): ")
                if ch.lower() != 'y':
                    break

    def StudentDetails(self):
        while True:
            student_ids = input("Enter Student IDs separated by commas (e.g., 1,2,3) or type 'exit' to go back to the main menu: : ").split(',')
            cur = self.conn.cursor(buffered=True)

            for student_id in student_ids:
                student_id = student_id.strip().lower()

                if student_id == 'exit':
                    self.conn.close()
                    return

                cur.execute("select * from studentmaster where St_Id='"+student_id+"'")
                x = cur.fetchone()

                if x is None:
                    print(f"Student ID {student_id} Not found. Please enter a valid student ID.")
                else:
                    print("\nStudent Name:", x[1])
                    print("Student Father Name:", x[2])
                    print("Student Mother Name:", x[3])
                    print("Student City:", x[4])
                    print("Student Contact:", x[5])
                    print("Student DOJ:", x[6])

            more_details = input("Do you want to see more details? (y/n): ")
            if more_details.lower() != 'y':
                break

    def FeePayment(self):
        try:
            while True:
                st_id = input("Enter Student ID or type 'exit' to go back to the main menu: ")

                if st_id.lower() == 'exit':
                    break

                with self.conn.cursor(buffered=True) as cur:
                    cur.execute("SELECT * FROM studentmaster WHERE st_id = %s", (st_id,))
                    student = cur.fetchone()

                    if student is None:
                        print(f"Student with ID {st_id} not found. Please enter a valid Student ID.")
                        continue

                    cur.execute("SELECT * FROM FeeDetails WHERE st_id = %s", (st_id,))
                    existing_fees = cur.fetchall()

                    total_paid = sum(fee[4] for fee in existing_fees) if existing_fees else 0

                    total_fee_year = 100  # Set the total fee for the academic year
                    remaining_fee = total_fee_year - total_paid756

                    print(f"Total Fee for the academic year: {total_fee_year}")
                    print(f"Total Paid so far: {total_paid}")
                    print(f"Remaining Fee: {remaining_fee}")

                    payment_amount = float(input("Enter the payment amount: "))

                    if payment_amount <= 0:
                        print("Invalid payment amount. Please enter a positive value.")
                        continue
                    elif payment_amount > remaining_fee:
                        print("Payment amount exceeds remaining fee. Please enter a valid amount.")
                        continue

                    cur.execute("INSERT INTO FeeDetails (st_id, Year, Semester, PaymentAmount) VALUES (%s, YEAR(CURDATE()), 'Semester 1', %s)",
                                (st_id, payment_amount))
                    self.conn.commit()
                    print("Payment successful.")

        except ms.Error as e:
            print(f"An error occurred: {e}")

    def StudentFee_Details(self):
        try:
            while True:
                self.st_id = input("Enter Student ID or type 'exit' to go back to the main menu: ")

                if self.st_id.lower() == 'exit':
                    break

                cur = self.conn.cursor(buffered=True)
                cur.execute("SELECT * FROM studentmaster WHERE St_Id = %s", (self.st_id,))
                student = cur.fetchone()

                if student is None:
                    print(f"Student with ID {self.st_id} not found. Please enter a valid Student ID.")
                    continue

                while True:
                    print("\n--- 1-Show All Fee Details ---")
                    print("--- 2-Show Fee Details for a Specific Year ---")
                    print("--- 0-Back to Main Menu ---")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        cur.execute("SELECT Year, Semester, PaymentAmount FROM FeeDetails WHERE st_id = %s", (self.st_id,))
                        fee_details = cur.fetchall()
                        if fee_details:
                            for fee in fee_details:
                                print("\nYear:", fee[0])
                                print("Semester:", fee[1])
                                print("Payment Amount:", fee[2])
                        else:
                            print("No fee details found for this student.")

                    elif choice == '2':
                        year = input("Enter the year: ")
                        cur.execute("SELECT Year, Semester, PaymentAmount FROM FeeDetails WHERE st_id = %s AND Year = %s", (self.st_id, year))
                        fee_details = cur.fetchall()
                        if fee_details:
                            for fee in fee_details:
                                print("\nYear:", fee[0])
                                print("Semester:", fee[1])
                                print("Payment Amount:", fee[2])
                        else:
                            print(f"No fee details found for Student ID {self.st_id} in year {year}.")

                    elif choice == '0':
                        break

                    else:
                        print("Invalid choice. Please enter a valid choice.")

        except ms.Error as e:
            print(f"An error occurred: {e}")


print("---- WELCOME TO VIPIN MITTAL PROGRAM-----")
student = Student()
if student.checklogin():
    student.conn.close()
    sys.exit(1)

ch = 'y'
choice = 1
while choice > 0:
    student.menu()
    choice = eval(input("Enter your choice:-"))

    if choice == 1:
        student.AddStudent()

    elif choice == 2:
        student.UpdateStudent()

    elif choice == 3:
        student.StudentDetails()

    elif choice == 4:
        student.FeePayment()

    elif choice == 5:
        student.StudentFee_Details()

    elif choice == 0:
        exit
    else:
        print("Invalid choice")
        ch = input("Do You Want To Continue(y/n)")
        if ch == 'y' or ch == 'Y':
            student.menu()
        else:
            exit
            choice = 0
