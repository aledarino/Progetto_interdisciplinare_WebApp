import psycopg2 
from psycopg2.extras import DictCursor

 # open a connection to the database and returns the conn (connection) 
def get_db_connection (): 
      # Connect to the database 
    conn = psycopg2.connect(dbname="aliseo2", user="admin", password="frittomisto", host="aliseo2.omniastudios.it", port="9090") 
    return conn 




########################## USERS CONNECTION #############################




# get all users 
def getUsers():
 # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM users;') 

    # Fetch the data = save the data in a variable called users 
  users = cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return users

def getUserByUsername(username):
   # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
    # Select all products from the table 
  cur.execute('SELECT * FROM users WHERE USERNAME = \'' + (username) + "\';") 

    # Fetch the data = save the data in a variable called user
  user = cur.fetchone() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return user



########################## USERS DEVICES CONNECTION ###################################



# get all users devices associations 
def getUsersDevices():
   # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM users_devices;') 

    # Fetch the data = save the data in a variable called users_devices
  users_devices = cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 
  return users_devices


def addColleague(colleague):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    cur.execute('INSERT INTO users_devices(id_device, username) VALUES (%s,%s)', (colleague['id_device'], colleague['username'])) 
    conn.commit()
    success = True

  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success

def addDoctor(doctor):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    cur.execute('INSERT INTO users_devices(id_device, username) VALUES (%s,%s)', (doctor['id_device'], doctor['username'])) 
    conn.commit()
    success = True

  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success

def DeleteDoctor(username, id_device):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    #if ("AreYouSure" in DeleteDoctor):
      #AreYouSure = 1
    cur.execute('DELETE FROM users_devices WHERE username = %s AND id_device = %s',( username, id_device)) 
    conn.commit()
    success = True
    #else:
      #AreYouSure = 0
  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success
def getUsersByIdDevice(id_device):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM users_devices WHERE id_device = %s;', (id_device,)) 

    # Fetch the data = save the data in a variable called users_devices
  users_devices = cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 
  return users_devices

def DeleteAllDoctors(id_device):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    #if ("AreYouSure" in DeleteDoctor):
      #AreYouSure = 1
    cur.execute('DELETE FROM users_devices WHERE id_device = %s',(id_device,)) 
    conn.commit()
    success = True
    #else:
      #AreYouSure = 0
  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success

  





############################## ALARM AND READINGS CONNECTION #########################################




def getAlarms():
   # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM alarms  ;') 

    # Fetch the data = save the data in a variable called alarms
  alarms= cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close()
  

  return alarms

def getReadings():
   # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM readings;') 

    # Fetch the data = save the data in a variable called readings
  readings = cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close()
  return readings





