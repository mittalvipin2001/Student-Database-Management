# Import the mysql.connector library and alias it as 'ms' for convenience
import mysql.connector as ms
import sys

# Define a class named 'school'
class school:
    def __init__(self):
        # Initialize instance variables for student information
        self.st_id = ""
        self.st_name = ""
        self.f_name = ""
        self.M_name = ""
        self.st_city = ""
        self.Contact = ""
        self.DOJ = ""


    def checkSchema(self, conn):
        cur = conn.cursor()
        try:
            # Try using the "student" database
            cur.execute("USE student")
            print("Connected to 'student' database.")
        except Exception as error:
            print(f"Error: {error}")
            try:
                # Create the "student" database if it doesn't exist
                cur.execute("CREATE DATABASE student")
                cur.execute("USE student")
                print("Created 'student' database.")
            except Exception as create_error:
                print(f"Error creating 'student' database: {create_error}")
                return  # Exit the function if the database cannot be created

        # Check if the "login" table exists and create it if it doesn't
        cur.execute("SHOW TABLES LIKE 'login'")
        if cur.fetchone() is None:
            try:
                cur.execute("""CREATE TABLE login (
                    uname VARCHAR(20) NOT NULL UNIQUE,
                    pswd VARCHAR(20) NOT NULL UNIQUE
                );""")
                print("login table created")
            except Exception as create_error:
                print(f"Error creating 'login' table : {create_error}")

        # Check if the "studentmaster" table exists and create it if it doesn't
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
            except Exception as create_error:
                print(f"Error creating 'studentmaster' table : {create_error}")

        # Check if the "FeeDetails" table exists and create it if it doesn't
        cur.execute("SHOW TABLES LIKE 'FeeDetails'")
        if cur.fetchone() is None:
            try:
                cur.execute("""CREATE TABLE FeeDetails (
                    FeeDetailID INT AUTO_INCREMENT PRIMARY KEY,
                    st_id INT,
                    Year INT,
                    Quarter VARCHAR(10),
                    Penalty DECIMAL(10, 2),
                    TotalFees DECIMAL(10, 2),
                    FOREIGN KEY (st_id) REFERENCES studentmaster(st_id)
                );""")
                print("FeeDetails table created")
            except Exception as create_error:
                print(f"Error creating 'FeeDetails' table : {create_error}")

        # Commit changes
        conn.commit()


        
        
    def connectDb(self):
        while True:
            # Prompt the user for username and password
            username = input("Enter User ID:- ")
            pswd = input("Enter Password:- ")   

            # Attempt to establish a database connection using the provided credentials
            conn = ms.connect(host="localhost", user=username, passwd=pswd) 

            if conn.is_connected():
                # Connection successful
                print("Connection established")
                
                # Call the checkSchema function to ensure the database and tables are set up correctly
                self.checkSchema(conn)
                
                # Return the established connection
                return conn
            else:
                # Connection failed, prompt the user to enter credentials again
                print("Error in connection. Enter your details again...")

    def checklogin(self):
        # Create a cursor to execute SQL queries
        cur = conn.cursor()
        exitFlag = 0
        while True:
            username = input("Enter login ID:- ")
            pswd = input("Enter Password:- ")
            
            # Execute a query to select all records from the 'login' table
            cur.execute("SELECT * FROM login where uname = '" + username + "' and pswd = '" + pswd + "'")
            
            # Fetch all the rows from the result set
            rows = cur.fetchone()
            
            if rows is not None:
                # Access granted if the provided username and password match a record in the 'login' table
                print("Access Granted")
                break
            else:
                # Invalid login credentials
                print("Invalid login id or password")
                opt = input("Do you want to create new login credentails[1] or retry again[2]?")

                if opt == "1":
                    try:
                        newUsername = input("Enter Username:- ")
                        newpswd = input("Enter Password:- ")
                        cur.execute("INSERT INTO login VALUES('" + newUsername + "', '" + newpswd + "')")
                        conn.commit()
                    except Exception as create_error:
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
        # Prompt user for student information
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
        
        # refresh connection
        cur = conn.cursor(buffered=True)
        cur.execute(insertCmnd[:len(insertCmnd)-1])
        conn.commit()
        print("All Students Added")
            

    def UpdateStudent(self):
        while True:
            self.st_id = input("Enter Student ID (or type 'exit' to stop updating): ")

            if self.st_id.lower() == 'exit':
                break  # Exit the loop if the user types 'exit'

            # Establish a database connection
            cur = conn.cursor(buffered=True)

            # Check if the entered student ID exists
            cur.execute("select St_Id from studentmaster where St_Id='"+self.st_id+"'")
            x = cur.fetchone()

            if x is None:
                print("Student ID Not found")
            else:
                # Prompt user for updated student information
                self.N_st_name = input("Enter Student Name:-")
                self.N_F_name = input("Enter Student Father Name:-")
                self.N_M_name = input("Enter Student Mother Name:-")
                self.N_st_city = input("Enter Student's City:-")
                self.N_Contact = input("Enter Mobile No:-")
                self.N_DOJ = input("Enter Admission date:-(yyyy/mm/dd)")

                # Update the student details in the database
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

                # Ask if the user wants to update more students
                ch = input("Do You Want To Update Another Student? (y/n): ")
                if ch.lower() != 'y':
                    break  # Exit the loop if the user does not want to update another student



    def StudentDetails(self):
        while True:
            student_ids = input("Enter Student IDs separated by commas (e.g., 1,2,3): ").split(',')
            cur = conn.cursor(buffered=True)

            for student_id in student_ids:
                # Remove leading/trailing spaces and convert to lowercase for 'exit' check
                student_id = student_id.strip().lower()

                if student_id == 'exit':
                    conn.close()
                    return  # Exit the function if 'exit' is entered

                # Check if the entered student ID exists
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
                self.st_id = input("Enter Student ID or type 'exit' to go back to the main menu: ")

                if self.st_id.lower() == 'exit':
                    break

                # Check if the entered student ID exists
                cur = conn.cursor(buffered=True)
                cur.execute("SELECT * FROM studentmaster WHERE St_Id = %s", (self.st_id,))
                student = cur.fetchone()

                if student is None:
                    print(f"Student with ID {self.st_id} not found. Please enter a valid Student ID.")
                    continue

                while True:
                    cur = conn.cursor(buffered=True)
                    cur.execute("SELECT COUNT(*) FROM FeeDetails WHERE st_id = %s", (self.st_id,))
                    count = cur.fetchone()[0]

                    if count == 0:
                        print("The FeeDetails table is empty. No unpaid quarters found for Student ID", self.st_id)
                        break

                    cur.execute("SELECT DISTINCT Quarter FROM FeeDetails WHERE st_id = %s AND Quarter NOT IN ('1', '2', '3', '4')", (self.st_id,))
                    unpaid_quarters = cur.fetchall()

                    if unpaid_quarters:
                        print(f"Unpaid Quarters for Student ID {self.st_id}:")
                        for quarter in unpaid_quarters:
                            print(quarter[0])

                        quarter_to_pay = input("Enter the quarter you want to pay (e.g., '1st Quarter'): ")
                        payment_amount = float(input("Enter the payment amount: "))

                        cur.execute("SELECT TotalFees, Penalty FROM FeeDetails WHERE st_id = %s AND Quarter = %s", (self.st_id, quarter_to_pay))
                        fees_penalty = cur.fetchone()

                        if fees_penalty:
                            total_fees, penalty = fees_penalty
                            total_payment = total_fees + penalty

                            if payment_amount >= total_payment:
                                cur.execute("INSERT INTO FeeDetails (st_id, Year, Quarter, Penalty, TotalFees) VALUES (%s, YEAR(CURDATE()), %s, 0, %s)",
                                            (self.st_id, quarter_to_pay, total_fees))
                                conn.commit()
                                print("Payment successful.")
                            else:
                                print(f"Payment amount ({payment_amount}) is less than the total amount due ({total_payment}). Payment failed.")
                        else:
                            print(f"Quarter {quarter_to_pay} not found for Student ID {self.st_id}. Payment failed.")
                    else:
                        print(f"No unpaid quarters found for Student ID {self.st_id}.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def StudentFee_Details(self):
        try:
            while True:
                self.st_id = input("Enter Student ID or type 'exit' to go back to the main menu: ")

                if self.st_id.lower() == 'exit':
                    break

                # Check if the entered student ID exists
                cur = conn.cursor(buffered=True)
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
                        # Show all fee details for the student
                        cur.execute("SELECT Year, Quarter, Penalty, TotalFees FROM FeeDetails WHERE st_id = %s", (self.st_id,))
                        fee_details = cur.fetchall()
                        if fee_details:
                            for fee in fee_details:
                                print("\nYear:", fee[0])
                                print("Quarter:", fee[1])
                                print("Penalty:", fee[2])
                                print("Total Fees:", fee[3])
                        else:
                            print("No fee details found for this student.")

                    elif choice == '2':
                        # Show fee details for a specific year
                        year = input("Enter the year: ")
                        cur.execute("SELECT Year, Quarter, Penalty, TotalFees FROM FeeDetails WHERE st_id = %s AND Year = %s", (self.st_id, year))
                        fee_details = cur.fetchall()
                        if fee_details:
                            for fee in fee_details:
                                print("\nYear:", fee[0])
                                print("Quarter:", fee[1])
                                print("Penalty:", fee[2])
                                print("Total Fees:", fee[3])
                        else:
                            print(f"No fee details found for Student ID {self.st_id} in year {year}.")

                    elif choice == '0':
                        break

                    else:
                        print("Invalid choice. Please enter a valid choice.")

        except Exception as e:
            print(f"An error occurred: {e}")






print("---- WELCOME TO VIPIN MITTAL PROGRAM-----")
obj = school()
conn=obj.connectDb()
if obj.checklogin():
    conn.close()
    sys.exit(1)

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
