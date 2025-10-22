# Copyright (c) 2025 Alessandra Darino, Laura D’Aiello
# This file is part of the NEWBREATH project and is licensed under the GNU AGPL v3.
# See the LICENSE file for details.


from flask import Flask, render_template, request, redirect, url_for,flash
import user_dao, models, device_dao
from models import User

  # import DictCursor to make dictionaries out of db tables 
  # colums names become the dictionary keys  
from psycopg2.extras import DictCursor

  # import LoginManager after installing flask-login (python3 -m pip install flask-login) 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

  # Then import os to make sure that usernames and passwords are not visible in the source code 
#from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

  # password for the developer. Must need it otherwhise the program won't run
app.config['SECRET_KEY'] = 'SECRET'

  # create an instance of login manager and initialize it 
login_manager = LoginManager()
login_manager.init_app(app)


#Home page: it contains general informations about the app and the log in  button
@app.route('/')
def index(): 
 return render_template('HomePage.html')
 


#########################################  LOGIN  ############################################



#login page 
@app.route('/login')
def login(): 
   return render_template('login.html')

#login form: enter username and password to access to doctorHomePage, it uses login_manager 
@app.route('/login', methods= ['POST'])
def post_login(): 
  user_form = request.form.to_dict()
  print(user_form)  
  user_db = user_dao.getUserByUsername(user_form['username'])
  

  if not user_db or not user_db['password'] == user_form['password']: #check_password_hash(user_db['password'], user_form['password']):
    flash('Error, invalid credentials, please try again.', 'error')
    print("entra qui") 
    return redirect(url_for('login'))
  else:
    new = User(user_db['id'], user_db['user_type'], user_db['user_first_name'], user_db['user_last_name'],  username=user_db['username'], password=user_db['password'] )
    login_user(new, True) 

    flash('Bentornato ' + user_db['username'] + '!', 'success')
    if user_db['user_type']== 1:
      
      print("non va")
      return redirect(url_for('DoctorHomePage'))
    elif user_db['user_type']== 0:
      print("va") 
      return redirect(url_for('ManHomePage'))

# non ho capito cosa faccia ma so che è necessaio 
# id is actually the username
@login_manager.user_loader
def load_user(id): 
  user_db = user_dao.getUserByUsername(id)
  print("CALLED USER LOADER")
  print("USERNAME:"+id)
  if user_db is not None:
      user = models.User(user_db['id'], user_db['user_type'], user_db['user_first_name'], user_db['user_last_name'],  username=user_db['username'], password=user_db['password'] )
  else:
      user = None 
  return user 



######################################## DOCTOR HOME PAGE #################################################



# doctorHomePage: user is logged, shows the names of the associated patients and trigger warnings. Button for add patient
@app.route("/user/DoctorHomePage")
@login_required 
def DoctorHomePage():

  
  
  devices = device_dao.getDevices()
  users = user_dao.getUsers()
  users_devices = user_dao.getUsersDevices()
  readings = user_dao.getReadings()

    # return a template in html and pass it the list of devices, users,users_devices and readings from the db
  return render_template('DoctorHomePage.html',devices = devices, users=users,  current_user=current_user, users_devices=users_devices, readings=readings) 



###################################### ADD PATIENT #######################################################



#Add patient page (to make the html page work)
@app.route('/AddPatient') 
@login_required
def AddPatient():
   users = user_dao.getUsers()
   
   return render_template('AddPatient.html', users=users) # return a template in html and pass it the list of  users from the db

# add patient function: associate patients with non associated devices and associate the doctor to the patient
@app.route('/AddPatient', methods= ['POST'])
@login_required
def add_patint(): 
  
    
    # request from Add patient form
  id_device = request.form['id_device']
  patient_first_name = request.form['patient_first_name']
  patient_last_name = request.form['patient_last_name']
  isassociated = True 
 
    # check if fields are empty and redirect to AddPatient
  if  id_device=='':
    app.logger.error('field empty')
    flash('All fields must be filled', 'empty')
    return redirect(url_for('AddPatient'))
     
  
  if patient_first_name=='': 
    app.logger.error('field empty')
    flash('All fields must be filled', 'empty')
    return redirect(url_for('AddPatient')) 
  
  
  if patient_last_name=='':
     app.logger.error('field empty')
     flash('All fields must be filled', 'empty')
     return redirect(url_for('AddPatient')) 
  
    # check if the device exists in the device table and is not associated 
  devices = device_dao.getDevices()
  Device_IsReal = False
  for device in devices:
    if device['id_device']==id_device:
      Device_IsReal= True  

      # check that is not associated 
      if device['patient_last_name'] is None:
         print( 'il device non è associato' )
         break 
      else:
         print('il device è associato')
         flash('The device is already associated, please dissociate the previous patient before associating another one', 'error')
         return redirect(url_for('AddPatient')) 

    else:
      print('no funziona')
      
     
  if Device_IsReal == False:
    flash('This device does not exist', 'error')
    return redirect(url_for('AddPatient'))
     


  if Device_IsReal == True :
    success = device_dao.addPatient(isassociated, {'patient_first_name':patient_first_name, 'patient_last_name':patient_last_name},
                          id_device)
    # if success add the association between the doctor and the patient   
    if success:
      flash('Success, the patient is correctly associated to the device', 'success')
      app.logger.info('paziente si')
      
      AddDoctor = user_dao.addDoctor({'id_device':id_device, 'username': current_user.username})
      if AddDoctor:
         flash('the doctor is correctly associated to the patient', 'success')
         app.logger.info('dottore sì')
      else:
          flash('doctor is not associated', 'error')
          app.logger.info('dottore no')
    else :
      flash('Something went wrong, please try again', 'error')
      app.logger.info('paziente no')
    

    return redirect(url_for('DoctorHomePage'))
    
  
  else: 
      
      print('non esiste dispositivo')
      return redirect(url_for('AddPatient'))




################################################ PATIENT DATA ######################################################


 #Patient data page  
@app.route('/PatientData/<id_device>')
@login_required
def PatientData(id_device):
   device = device_dao.getDeviceByIdDevice(id_device)
   alarms = user_dao.getAlarms()
   readings = user_dao.getReadings()
   users = user_dao.getUsers()
   # return a template in html and pass it the list of  users, readings and alarms from the db, instead id_device depends by what user 
   #clicks in the DoctorHomePage, it is a variable of the route 

   return render_template('PatientData.html', id_device=id_device, device = device, readings=readings, alarms=alarms,users=users)  



########################################## DISSOCIATE PATIENT ###########################################################



#DissociatePatient page (to make html page work)
@app.route('/DissociatePatient/<id_device>')
@login_required 
def DissociatePatient(id_device):
   device = device_dao.getDeviceByIdDevice(id_device)
   users = user_dao.getUsers()
   # return a template in html and pass it the list of  users from the db, instead id_device depends by what (patient) user 
   #clicks in the DoctorHomePage, it is a variable of the route 
   return render_template('DissociatePatient.html', id_device = id_device, users=users, device=device)

#Dissociate Patient function (to dissociate patient from a device ) and all doctors from this patient
@app.route('/DissociatePatient/<id_device>', methods= ['POST'])
@login_required 
def Dissociate_Patient(id_device): 

  
  isassociated = False 
  id_device = request.form['staticIdDevice']
   #id_device is taken automatically
  print('è uguale a',id_device)
  check = request.form.get('AreYouSure')
  print("il check è uguale a ", check)
  #check if the user has checked
  if check == "1" :  
    #dissociate patient from device in the table "devices"
    success = device_dao.deletePatient(isassociated, id_device)
    
    
    if success:

      app.logger.info('PAZIENTE SCOMPARSO')
      flash('Success, the patient is correctly dissociated from the device', 'success')
      doctors = user_dao.getUsersByIdDevice(id_device)
      print(doctors)
      
      
      #username = current_user.username
      #DelateDoctors = user_dao.DeleteDoctor(username,id_device)
      #Dissociate all doctors from this patient in the table "users_devices"
      DelateDoctors = user_dao.DeleteAllDoctors(id_device)
      if DelateDoctors:
        app.logger.info('DOTTORI SCOMPARSI')
        flash('All doctors are correctly dissociated from the patient', 'success')
        return redirect(url_for('DoctorHomePage'))
      else :
        app.logger.info('DOTTORI NON SCOMPARSI')
        flash(' Error, the patient is correctly dissociated from the device, but doctors are not correctly dissociated from the patient', 'error')
    else :
      app.logger.info('DPAZIENTE NON SCOMPARSO')
      flash('Error, the patient is not correctly dissociated from the device, please try again', 'error')
      return redirect(f'/DissociatePatient/{id_device}')
    
    
  else: 
     flash('Are you sure? (Please put the check)', 'sure')
     return redirect(f'/DissociatePatient/{id_device}')  




####################################### ADD COLLEAGUE ####################################################


#AddColleague page (to make the html page work)
@app.route('/AddColleague/<id_device>') 
@login_required

def AddColleague(id_device):
   
   users = user_dao.getUsers()
   device = device_dao.getDeviceByIdDevice(id_device)
   
   return render_template('AddColleague.html', id_device= id_device, users=users, device=device)
#Add colleague function: add colleague username in the table "users_devices"
@app.route('/AddColleague/<id_device>', methods= ['POST'])
@login_required
def add_colleague(id_device):
  print(id_device)
  #colleague = request.form.to_dict()
  # request from Add colleague form, but id_device is taken automatically
  id_device = request.form['staticIdDevice']
  username = request.form['username'] 
  #check if field is empty
  if username =='':
     app.logger.error('field empty')
     flash('All fields must be filled', 'empty')
     return redirect(f'/AddColleague/{id_device}')
  #if colleague['username']=='':
  #   app.logger.error('field empty')
  #   return redirect(url_for('AddColleague'))
  
  
  #""" if colleague['id_device']=='':
  #   app.logger.error('field empty')
  #   return redirect(url_for('AddColleague')) """
  
  success = user_dao.addColleague({'username':username, 'id_device': id_device})# add colleague username in the table "users_devices"
  if success:
     
     app.logger.info('collega si')
     flash('Success, your colleague is correctly associated to the patient', 'success')
     return redirect(f'/PatientData/{id_device}')
  else :
     
     app.logger.info('collega no')
     flash('Error, something went wrong, it is likely that your colleague was already associated with this patient', 'error')
     return redirect(f'/AddColleague/{id_device}')


   



############################################# DISSOCIATE DOCTOR #############################################


#DissociateDoctor page (to make the html page work)
@app.route('/DissociateDoctor/<id_device>')
@login_required
def DissociateDoctor(id_device):
  device = device_dao.getDeviceByIdDevice(id_device)
  users = user_dao.getUsers()
  return render_template('DissociateDoctor.html', device=device, users=users)
 #Dissociate doctor function   (to dissociate a doctor from a patient) 
@app.route('/DissociateDoctor/<id_device>', methods= ['POST'] )
@login_required
def Dissociate_Doctor(id_device):
  
   # request check from DissociateDoctor form, but id_device and username are taken automatically
  id_device = request.form['staticIdDevice']
  print(id_device)
  check = request.form.get('AreYouSure')
  print("il check è uguale a ", check)
  username = current_user.username
  print(username)
  devices = user_dao.getUsersDevices()
  countAssociations = 0
  #check if the user has checked
  if check == "1" :
    for device in devices:
      #check if the doctor that is trying to dissociate himself is not the last who can see that patient
      if device['id_device']== id_device:
        countAssociations = countAssociations + 1
      else :
        pass

    print('il numero di associazioni è ', countAssociations)
    if countAssociations == 1:
      print('sei lultimo a dissociarti') 
      app.logger.info('ULTIMO ')  
      flash ('Error, you are the last user associated with this patient. Dissociate the patient from the device before dissociating yourself', 'error')
      return redirect(f'/DissociateDoctor/{id_device}') 
    else :    
      success = user_dao.DeleteDoctor(username, id_device)
      if success:  
        print(username, id_device)  
        app.logger.info('DOTTORE SCOMPARSO')
        flash ('Success, you were correctly disassociated from the patient.', 'success')
        return redirect(url_for('DoctorHomePage'))    
      else :
        app.logger.info('DOTTORE NON SCOMPARSO') 
        flash ('Error, something went wrong, please try again', 'error')
        return redirect(f'/DissociateDoctor/{id_device}') 
     
  else :
     print('no funziona') 
     app.logger.info('CHECK')
     flash('Are you sure? (Please put the check)', 'sure')
     return redirect(f'/DissociateDoctor/{id_device}')
  
 
#logout function
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '_main_': 
	app.run(debug=True) 
#Manufacturer Home Page
@app.route("/user/ManHomePage")
@login_required 
def ManHomePage():
  
  devices = device_dao.getDevices()
  users = user_dao.getUsers()
  users_devices = user_dao.getUsersDevices()
  readings = user_dao.getReadings()
    # return a template in html and pass it the list of users from the db
  return render_template('ManHomePage.html',devices = devices, users=users,  current_user=current_user, users_devices=users_devices, readings=readings) 
#DeviceData page for devices seen by the manufacturer
@app.route('/DeviceData/<id_device>')
@login_required
def DeviceData(id_device):
   users = user_dao.getUsers()
   device = device_dao.getDeviceByIdDevice(id_device)
   alarms = user_dao.getAlarms()
   readings = user_dao.getReadings()
   return render_template('DeviceData.html', id_device= id_device, device = device, readings=readings, alarms=alarms, users=users)