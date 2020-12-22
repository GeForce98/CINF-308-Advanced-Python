#Quincy Asemota
#INF 308 Programming for Informatics
#Final Project Part 3 - Data Visualization

# Import the sqlite3 module
import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
from graphics import *

# Welcome Message
print('\nWrite a progam that parses the web for a grading scale,')
print('\nAnd uses it to add a letter grade to the "students" database (created in the previous part).')

# Display a message stating its goal
print('====== Connecting to "students" database ======')

# connect to the students database
con = sqlite3.connect("students.db")
cursor = con.cursor()

#BeautifulSoup Parser
page_link = "https://nimdvir.github.io/teaching/inf308/Grading-SUNY.html"
page = urlopen(page_link)
soup = BeautifulSoup(page, "html.parser")
table = soup.find("table")
grades = table.text.strip()
grades = grades.split()
grade_dict = {}
marks = ""
for i in range(len(grades)):
  if i % 2 == 0:
    marks = grades[i]
  else:
    grade_dict[grades[i]] = marks

cursor.execute('DROP TABLE IF EXISTS grading')

sql_command = """CREATE TABLE grading(
  Letter VARCHAR(3),
  MinGrade INTEGER,
  MaxGrade INTEGER
);"""
cursor.execute(sql_command)

for key, value in grade_dict.items():
  sql_command = """INSERT INTO grading (Letter, MinGrade, MaxGrade) VALUES ("{}", {}, {})""".format(key, value.split('-')[0], value.split('-')[1])
  cursor.execute(sql_command)

sql_command = """SELECT * FROM grading"""
grade_dict = {}
result = cursor.execute(sql_command)
for r in result.fetchall():
  grade_dict[r[0]] = "{} {}".format(r[1],r[2])

cursor.execute('DROP TABLE IF EXISTS Students')
cursor.execute('CREATE TABLE Students (studentID NUMBER, departmentName TEXT, standing TEXT, gpa NUMBER)')

ids = []

def no_repeats(num):
    if num not in ids:
        return True
    return False

for i in range(500):
  studentID = 0
  standing = ''
  while True:
      studentID = random.randint(100001, 999999)
      if no_repeats(studentID):
          break
  if i < 100:
      gpa = random.randint(93, 100)
      standing = 'Honors'
  elif i >= 100 and i < 400:
      gpa = random.randint(0, 60)
      standing = 'Probation'
  elif i >= 400:
      gpa = random.randint(61, 92)
      standing = 'Normal'

  cursor.execute('INSERT INTO Students(studentID, departmentName, standing, gpa) VALUES(?,?,?,?)', (studentID, "Science", standing, gpa))

sql_command = """ALTER TABLE Students
ADD Letter VARCHAR(3);"""

cursor.execute(sql_command)

sql_command = """SELECT * FROM Students"""
result = cursor.execute(sql_command)
for r in result.fetchall():
  for key, value in grade_dict.items():
    if(int(r[3]) >= int(value.split(' ')[0]) and int(r[3]) <= int(value.split(' ')[1])):
      cursor.execute('UPDATE Students SET Letter = "{}" WHERE studentID = {} '.format(key, r[0]))
      break

sql_command = """SELECT * FROM Students"""
result = cursor.execute(sql_command)
for r in result.fetchall():
  print(r)

sql_command = """ALTER TABLE grading
ADD total INTEGER;"""

cursor.execute(sql_command)

sql_command = """SELECT * FROM grading"""
result = cursor.execute(sql_command)
for r in result.fetchall():
  count = cursor.execute("""SELECT count(*) FROM Students WHERE Letter = "{}" """.format(r[0]))
  count = count.fetchall()[0][0]
  cursor.execute("""UPDATE grading SET total = {} WHERE Letter = '{}'""".format(count, r[0]))

def check(value):
    sql_command = """SELECT * FROM Students WHERE studentID = {};""".format(value)
    student = cursor.execute(sql_command)
    student = student.fetchall()
    if len(student) > 0:
        grade = student[0][4]
        dept = student[0][1]
        sid = student[0][0]
        standing = student[0][2]
        gpa = student[0][3]
        #Students Academic Record New Window
        result_win = GraphWin("Student's Academic Record {}".format(sid), 640, 480)
        if standing == "Honors":
            result_win.setBackground('Green')
        elif standing == "Normal":
            result_win.setBackground('Grey')
        elif standing == "Probation":
            result_win.setBackground('Red')
        #Student Academic Records Box Information
        studentID_message = Text(Point(150,65), "Student ID: {}".format(sid))
        studentID_message.setSize(14)
        studentID_message.setStyle("bold")
        studentID_message.draw(result_win)
        studentID_message = Text(Point(150,115), "Department: {}".format(dept))
        studentID_message.setSize(14)
        studentID_message.setStyle("bold")
        studentID_message.draw(result_win)
        studentID_message = Text(Point(150,165), "Academic Standing: {}".format(standing))
        studentID_message.setSize(14)
        studentID_message.setStyle("bold")
        studentID_message.draw(result_win)
        studentID_message = Text(Point(150,215), "GPA: {}".format(gpa))
        studentID_message.setSize(14)
        studentID_message.setStyle("bold")
        studentID_message.draw(result_win)
        studentID_message = Text(Point(150,265), "Letter Grade: {}".format(grade))
        studentID_message.setSize(14)
        studentID_message.setStyle("bold")
        studentID_message.draw(result_win)
        pt = Point(150, 300)
        button=Rectangle(Point(255,325), pt)
        button.setFill('blue')
        button.draw(result_win)
        buttonText= Text(Point(205, 312), "Done")
        buttonText.setTextColor('white')
        buttonText.draw(result_win)
        notdone=True
        while notdone:
            p2=result_win.getMouse()
            if 150<p2.x<255 and 300<p2.y<325:
                result_win.close()
                notdone=False
        return True
    else:
        error_win = GraphWin("Invalid ID Error", 350, 150)
        error_message = Text(Point(150,30), "Invalid ID Error. Please enter a VALID ID.")
        error_message.setStyle("bold")
        error_message.setSize(10)
        error_message.draw(error_win)
        pt = Point(80, 60)
        button=Rectangle(Point(120,80), pt)
        button.setFill('red')
        button.draw(error_win)
        buttonText= Text(Point(100, 70), "Exit")
        buttonText.setTextColor('white')
        buttonText.draw(error_win)
        notdone=True
        while notdone:
            p2=error_win.getMouse()
            if 80<p2.x<120 and 60<p2.y<80:
                error_win.close()
                notdone=False
        return False
        
#GUI Student Message
win = GraphWin("Student's Information", 640, 480)
studentID_message = Text(Point(135,65), "Please enter Student ID: ")
studentID_message.setSize(12)
studentID_message.setStyle("bold")
studentID_message.draw(win)

#GUI Welcome Message
studentID_message = Text(Point(300,40), "This program is designed to request and display student's information.")
studentID_message.setSize(12)
studentID_message.setStyle("bold")
studentID_message.draw(win)

#Submit Button
pt = Point(400, 50)
button=Rectangle(Point(500,80), pt)
button.setFill('red')
button.draw(win)
buttonText= Text(Point(450, 65), "Submit")
buttonText.setTextColor('white')
buttonText.draw(win)

#Close Button
pt = Point(300, 150)
button=Rectangle(Point(400,180), pt)
button.setFill('red')
button.draw(win)
buttonText= Text(Point(350, 165), "Close")
buttonText.setTextColor('white')
buttonText.draw(win)

#Student ID Box
studentID_entry = Entry(Point(305, 65),17)
studentID_entry.setText("Enter Student ID")
studentID_entry.draw (win)
not_exit = True
while not_exit:
    #Set numbers to run when button clicked
    notdone=True
    while notdone:
        p1=win.getMouse()
        if 400<p1.x<500 and 50<p1.y<80:
            valA= studentID_entry.getText()
            valA = int(valA)
            if check(valA) == False:
                studentID_entry.setText('')
                continue
            studentID_entry.setText('')
            notdone=False

        if 300<p1.x<400 and 150<p1.y<180:
            win.close()
            notdone=False
            not_exit=False
