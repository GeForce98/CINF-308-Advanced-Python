#Quincy Asemota
#INF 308 Programming for Informatics
#Final Project Part 2 - Letter Grading

# Import the sqlite3 module
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
import random

print('\nWrite a progam that parses the web for a grading scale,')
print('\nAnd uses it to add a letter grade to the "students" database (created in the previous part).')

#BeautifulSoup  Parser
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

# Display a message stating its goal
print('====== Connecting to "students" database ======')

# connect to the students database
con = sqlite3.connect("students.db")
cursor = con.cursor()

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

sql_command = """ALTER TABLE grading
ADD total INTEGER;"""

cursor.execute(sql_command)

sql_command = """SELECT * FROM grading"""
result = cursor.execute(sql_command)
for r in result.fetchall():
  count = cursor.execute("""SELECT count(*) FROM Students WHERE Letter = "{}" """.format(r[0]))
  count = count.fetchall()[0][0]
  cursor.execute("""UPDATE grading SET total = {} WHERE Letter = '{}'""".format(count, r[0]))

sql_command = """SELECT * FROM grading ORDER BY Letter"""
result = cursor.execute(sql_command)
r = result.fetchall()
i = 0
while i < len(r):
  if i < len(r) - 1:
    if(r[i][0][0] == r[i+1][0][0] and r[i+1][0][1] == "+"):
      print("{} | {} students".format(r[i+1][0],r[i+1][3]))
      print("{} | {} students".format(r[i][0],r[i][3]))
      i += 1
    else:
      print("{} | {} students".format(r[i][0],r[i][3]))
  else:
    print("{} | {} students".format(r[i][0],r[i][3]))
  i += 1
