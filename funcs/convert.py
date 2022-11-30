import os
import sys
import sqlite3

######################################
# Helper functions


######################################
# Let's do shit

# Process input
input_filename = "../stored_data_catalogue/tiles_test.mbtiles"
dirname = "tiles_test"

# This will fail if there is already a directory.
# I could make a better error message, but I intend for this to fail,
# because it's better to not delete data.
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

print(cursor.execute("PRAGMA table_info(tiles)").fetchall())

# cursor.execute("ALTER TABLE tiles RENAME COLUMN tile TO tile_data")
# cursor.execute("ALTER TABLE tiles RENAME COLUMN tile_id TO tile")
# cursor.execute("ALTER TABLE tiles ADD COLUMN zoom_level")
# cursor.execute("ALTER TABLE tiles ADD COLUMN tile_column")
# cursor.execute("ALTER TABLE tiles ADD COLUMN tile_row")
# cursor.execute("SELECT * FROM tiles")
# # os.chdir(dirname)
# for row in cursor.fetchall():
#     if row[0]=="background":
#       continue
#     tile = row[0].split("/")
#     while len(tile)<3:
#       tile.append("")
#     print(tile)
#     update = """
#       UPDATE tiles 
#           SET zoom_level = ?, tile_column= ?, tile_row =?
#            WHERE tile = ?;
#     """
#     cursor.execute(update, tile + [row[0],])

# connection.commit()
# connection.close()
    

