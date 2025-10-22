# Progetto_interdisciplinare_WebApp
 Web-based application developed as part of an interdisciplinary academic project. It enables remote monitoring of home-based non-invasive ventilation devices, supporting healthcare professionals in managing patient-device associations, visualizing clinical parameters, and responding to device alarms.
##  Project Goals
- Enable real-time monitoring of ventilation devices used in home care
- Manage associations between patients, devices, and healthcare providers
- Display clinical data and alarm states from connected devices
- Support personalized clinical decision-making through a secure web interface

##  Technologies Used
- **Backend**: Python, Flask, Flask-LoginManager, psycopg2
- **Frontend**: HTML, CSS, Bootstrap, Jinja2 templates
- **Database**: PostgreSQL (hosted externally)
- **IDE**: Visual Studio Code

##  System Architecture
- `app.py`: main entry point, route definitions, authentication logic
- `user_dao.py`, `device_dao.py`: data access objects for database interaction
- `templates/`: HTML pages with embedded Jinja2 logic
- `static/style.css`: custom styling layered over Bootstrap
- PostgreSQL schema includes tables for `users`, `devices`, `users_devices`, `alarms`, and `readings`

##  Authentication & Access Control
- Login system implemented using Flask-LoginManager and UserMixin
- Role-based access:
  - **Healthcare providers** (`user_type = 1`): can view and manage patients and device associations
  - **Manufacturers** (`user_type = 0`): limited to viewing device data

## Key Features
- Dynamic rendering of patient-device associations via Jinja2
- Alarm visualization based on real-time device readings
- Functions for adding/dissociating patients and colleagues
- Secure access to pages via `@login_required` and `current_user`

##  Deployment Notes
- Install Flask and psycopg2 via:
  ```bash
  pip install Flask psycopg2
