import os
import sys
import sqlite3

######################################
# Helper functions

def safeMakeDir(d):
  if os.path.exists(d):
    return
  os.makedirs(d)

def setDir(d):
  safeMakeDir(d)
  os.chdir(d)

######################################
# Let's do shit

# Process input
input_filename = sys.argv[1]
dirname = input_filename[0:input_filename.index('.')]

# This will fail if there is already a directory.
# I could make a better error message, but I intend for this to fail,
# because it's better to not delete data.
os.makedirs(dirname)
print(input_filename)
# Database connection boilerplate
connection = sqlite3.connect(input_filename)
cursor = connection.cursor()

print(cursor.execute('SELECT name from sqlite_master where type= "table"').fetchall())

cursor.execute("SELECT value FROM metadata WHERE name='format'")
img_format = cursor.fetchone()
print(img_format)

if img_format[0] == 'png':
    out_format = '.png'
elif img_format[0] == 'jpg':
    out_format = '.jpg'
elif img_format[0] == 'pbf':
    out_format = '.pbf'
else:
    out_format = ''
#print(cursor.execute("SELECT * FROM map").fetchall())
# The mbtiles format helpfully provides a table that aggregates all necessary info
#print(cursor.execute("SELECT * FROM images").fetchall())
cursor.execute("SELECT * FROM images")
os.chdir(dirname)
for row in cursor:
    print(row[0])
    if row[0]=="background":
      continue
    z, x, y = row[0].split("/")
    setDir(str(z))
    setDir(str(x))
    output_file = open(str(y) + out_format, 'wb')
    output_file.write(row[1])
    output_file.close()
    os.chdir('..')
    os.chdir('..')

