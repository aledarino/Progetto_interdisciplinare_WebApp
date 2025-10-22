import psycopg2 
from psycopg2.extras import DictCursor

 # open a connection to the database and returns the conn (connection) 
def get_db_connection (): 
      # Connect to the database 
    conn = psycopg2.connect(dbname="aliseo2", user="admin", password="frittomisto", host="aliseo2.omniastudios.it", port="9090") 
    return conn 

#get all devices (and patients) 
def getDevices():
 # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    # Select all products from the table 
  cur.execute('SELECT * FROM devices;') 

    # Fetch the data = save the data in a variable called devices
  devices = cur.fetchall() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return devices

#get device by id 
def getDeviceById(id):
 # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
  print(id)
    # Select all products from the table 
  cur.execute('SELECT * FROM devices WHERE ID = '+id) 

    # Fetch the data = save the data in a variable called device
  device = cur.fetchone() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return device

def getDeviceByIdDevice(id_device):
# pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
  print(id_device)
    # Select all products from the table 
  cur.execute('SELECT * FROM devices WHERE id_device =\'' + (id_device) + "\';") 

    # Fetch the data = save the data in a variable called device
  device = cur.fetchone() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return device

def addPatient(isassociated, patient, id_device):
    # pen a database connection
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    cur.execute('UPDATE devices SET device_isassociated = %s, patient_first_name= %s, patient_last_name = %s WHERE id_device = %s',(isassociated,  patient['patient_first_name'], patient['patient_last_name'], id_device)) 
    conn.commit()
    success = True

  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success

def deletePatient(isassociated, id_device):
  conn = get_db_connection()

    # create a cursor 
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
   
  success = False
  try:
    cur.execute('UPDATE devices SET device_isassociated = %s, patient_first_name = NULL, patient_last_name = NULL WHERE id_device = %s',(isassociated, id_device)) 
    conn.commit()
    success = True

  except Exception as e:
    print('Error', str(e))
    conn.rollback() 

    # close the cursor and connection 
  cur.close() 
  conn.close() 

  return success


