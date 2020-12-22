#Quincy Asemota
#INF 308 Programming for Informatics
#Final Project Part 1 - University Statistics

# Import the sqlite3 module
import random
import contextlib
import sqlite3



def print_header():
    print('{0:<8}{1:<8}   {2:<8}{3:<8}'.format(
        "Name", "Total Students", "Honors", "Probation"))


def print_students_row(row):
    print('{0:<8}{1:<8}\t {2:<8}{3:<8}'.format(
        row[0], row[1], row[2], row[3]))


# Welcome Message
print("\nWrite a program that creates and analyzes databases for a certain university using SQLite")
print("\nFirst,the program creates a database for department's data.")
print("\nThen, the program uses it to create a 'student's database and make various calculations")

# Display a message stating its goal
print('====== Creating "departments" database ======')

with contextlib.closing(sqlite3.connect('departments.sqlite')) as conn, conn, \
        contextlib.closing(conn.cursor()) as cur:
    # Create a table - departments
    cur.execute('DROP TABLE IF EXISTS Departments')
    cur.execute('CREATE TABLE Departments (departmentName TEXT, studentTotal NUMBER, honors FLOAT, probation FLOAT)')

    while True:
        deptName = ''
        while True:
            deptName = input("Please enter a department name: ").upper()
            cur.execute(
                'SELECT count(*) FROM Departments WHERE departmentName = ?', (deptName,))
            result = cur.fetchone()[0]

            if result == 1:
                modify = input(
                    "Would you like to modify (y) or try again (n)?: ")
                if modify is 'y':
                    break
            else:
                break

        numStudents = ''
        honorPercent = ''
        probationPercent = ''

        while True:
            numStudents = input("Please enter the number of students in the department as a whole number: ")
            if not numStudents.isdigit():
                print("This input is not allowed, please enter a whole number.")
            elif(int(numStudents) > 0):
                break
            else:
                print("Out of range.")

        while True:
            honorPercent = input("Please enter the percentage of honor students as a decimal number: ")
            if honorPercent.isdigit():
                print("This input is not allowed, please enter a decimal number.")
            elif(float(honorPercent) > 0 and float(honorPercent) <= 1):
                break
            else:
                print("Out of range.")
        while True:
            probationPercent = input("Please enter the percentage of students on probation as a decimal number: ")
            if probationPercent.isdigit():
                print("This input is not allowed, please enter a decimal number.")
            elif(float(probationPercent) > 0 and float(probationPercent) <= 1):
                break
            else:
                print("Out of range.")

        cur.execute('INSERT INTO Departments(departmentName, studentTotal, honors, probation) VALUES(?,?,?,?)',
                    (deptName, int(numStudents), float(honorPercent), float(probationPercent)))

        cur.execute('SELECT * from Departments')

        all_rows = cur.fetchall()

        print_header()
        for row in all_rows:
            print_students_row(row)

        again = input("Would you like to enter data for another Department enter (y) or calculate statistics with(n): ")

        if 'n' is again:
            break

    cur.execute('DROP TABLE IF EXISTS Students')
    cur.execute('CREATE TABLE Students (studentID NUMBER, departmentName TEXT, standing TEXT, gpa NUMBER)')
    cur.execute('ALTER TABLE Departments ADD averageGPA FLOAT NOT NULL DEFAULT(0.0)')
    cur.execute('SELECT * from Departments')

    all_rows = cur.fetchall()

    ids = []

    def no_repeats(num):
        if num not in ids:
            return True
        return False

    for row in all_rows:
        deptName = row[0]
        numStudents = int(row[1])
        honorsPercent = float(float(row[2]) * numStudents)
        probationPercent = float(float(row[3]) * numStudents)

        averageGPA = 0

        for i in range(numStudents):
            studentID = 0
            standing = ''
            while True:
                studentID = random.randint(100001, 999999)
                if no_repeats(studentID):
                    break
            if i < honorsPercent:
                gpa = random.randint(93, 100)
                standing = 'Honors'
            elif i >= honorsPercent and i < honorsPercent + probationPercent:
                gpa = random.randint(0, 60)
                standing = 'Probation'
            elif i >= honorsPercent + probationPercent:
                gpa = random.randint(61, 92)
                standing = 'Normal'

            averageGPA += gpa

            cur.execute('INSERT INTO Students(studentID, departmentName, standing, gpa) VALUES(?,?,?,?)', (studentID, deptName, standing, gpa))

        aGPA = averageGPA / numStudents
        cur.execute('UPDATE Departments SET averageGPA = (?) where departmentName = (?)',(aGPA, deptName))
        cur.execute('SELECT SUM(studentTotal) FROM Departments')
    
    totalStudents = int(cur.fetchone()[0])
    print('Total number of students in the university: {0}'.format(totalStudents))

    cur.execute('SELECT COUNT(departmentName) FROM Departments')

    totalDepartments = int(cur.fetchone()[0])
    print('Total number of departments in the university: {0}'.format(totalDepartments))
    
    cur.execute('SELECT COUNT(standing) from Students WHERE standing = \'Honors\'')

    honorsStudents = int(cur.fetchone()[0])
    print('Total number of honors students in the university: {0}'.format(honorsStudents))

    cur.execute('SELECT COUNT(standing) from Students WHERE standing = \'Probation\'')

    probationStudents = int(cur.fetchone()[0])
    print('Total number of probation students in the university: {0}'.format(probationStudents))

    cur.execute('SELECT SUM(gpa) from Students')

    totalGPA = cur.fetchone()[0]
    print('Average GPA for all students in university: {0}'.format(totalGPA / totalStudents))

    cur.execute('SELECT MAX(averageGPA) from Departments')

    maxDepartment = float(cur.fetchone()[0])

    cur.execute('SELECT * from Departments WHERE averageGPA = (?)',(maxDepartment,))

    numStudents = 0
    honorP = 0
    probP = 0
    name = ''

    dept = cur.fetchone()

    numStudents = int(dept[1])
    honorP = float(dept[2])
    probP = float(dept[3])
    name = dept[0]

    cur.execute('SELECT departmentName, AVG(gpa) from Students where departmentName = (?) AND standing = (?)', (name, 'Honors',))

    averageHonorGPA = float(cur.fetchone()[1])

    cur.execute('SELECT departmentName, AVG(gpa) from Students where departmentName = (?) AND standing = (?)', (name, 'Probation'))

    averageProbationGPA = float(cur.fetchone()[1])

    print("\nDepartment with highest average GPA: ")

    print("\nName: {0}\nNumber of students and percentage: {1}\nNumber of honor students and average: {2}\nNumber of probation students and average: {3}".format(
        name, '{0} + {1}%'.format(numStudents, int((numStudents / totalStudents) * 100)), '{0} + {1}'.format(numStudents * honorP, averageHonorGPA), '{0} + {1}'.format(numStudents * probP, averageProbationGPA)))

    cur.execute('SELECT MAX(gpa) from Students where departmentName = (?)', (name,))

    highGPA = cur.execute('SELECT studentID from Students where gpa = (?)', (int(cur.fetchone()[0]),))

    print("Highest GPA ID: {0}".format(cur.fetchone()[0]))

    cur.execute('SELECT MIN(gpa) from Students where departmentName = (?)', (name,))

    highGPA = cur.execute('SELECT studentID from Students where gpa = (?)', (int(cur.fetchone()[0]),))

    print("Lowest GPA ID: {0}".format(cur.fetchone()[0]))

    # Highest Student 

    cur.execute('SELECT MAX(studentTotal) from Departments')

    maxDepartment = float(cur.fetchone()[0])

    cur.execute('SELECT * from Departments WHERE studentTotal = (?)',(maxDepartment,))

    numStudents = 0
    honorP = 0
    probP = 0
    name = ''
    
    dept = cur.fetchone()

    numStudents = int(dept[1])
    honorP = float(dept[2])
    probP = float(dept[3])
    name = dept[0]

    cur.execute('SELECT departmentName, AVG(gpa) from Students where departmentName = (?) AND standing = (?)', (name, 'Honors',))

    averageHonorGPA = float(cur.fetchone()[1])

    cur.execute('SELECT departmentName, AVG(gpa) from Students where departmentName = (?) AND standing = (?)', (name, 'Probation'))

    averageProbationGPA = float(cur.fetchone()[1])

    print("\nDepartment with the most students is: ")
    print("\nName: {0}\nNumber of students and percentage: {1}\nNumber of honor students and average: {2}\nNumber of probation students and average: {3}".format(
        name, '{0} + {1}%'.format(numStudents, int((numStudents / totalStudents) * 100)), '{0} + {1}'.format(numStudents * honorP, averageHonorGPA), '{0} + {1}'.format(numStudents * probP, averageProbationGPA)))

    # Highest GPA and lowest  GPA students with id
    cur.execute('SELECT MAX(gpa) from Students where departmentName = (?)', (name,))

    highGPA = cur.execute('SELECT studentID from Students where gpa = (?)', (int(cur.fetchone()[0]),))

    print("Highest GPA ID: {0}".format(cur.fetchone()[0]))

    cur.execute('SELECT MIN(gpa) from Students where departmentName = (?)', (name,))

    highGPA = cur.execute('SELECT studentID from Students where gpa = (?)', (int(cur.fetchone()[0]),))

    print("Lowest GPA ID: {0}".format(cur.fetchone()[0]))

    
