# RTCams
This project is built to perform real-time camera-based attendance management. It's deployed using Streamlit.

# Tech Stack
- Front-End: HTML, CSS, Bootstrap
- Back-End: Django Framework
- Database: MySQL

# Key Features
- Two different login features - Faculty and Student.
- Students can perform profile updation and course-wise attendance searches. The search functionalities can be done using none, one or more filters - course, date, etc.
- Faculties can perform student registration, profile updation, attendance searches, and attendance captures at two different times - at the start and the end of the class.
- 3-way Status display - Present, Absent, and Proxy.
- Includes basic proxy-checking features based on time stamps recorded for check-in and out for every student.

**Note**: Python version 3.8 was used for this project. The dlib package required for the installation of face_recognition API is also uploaded.
To run the web application on your local computer, install the required libraries(requirements.txt) using the command:
```python 
pip install -r requirements.txt
```
Ensure to create your superuser, with suitable credentials using the command:
```python 
python manage.py createsuperuser
```
Finally run the server using:
```python 
python manage.py runserver
```
# Project Directory Structure
```bash
├───attendance_sys
│   ├───migrations
│   │   └───__pycache__
│   ├───templates
│   │   └───attendance_sys
│   └───__pycache__
├───attendance_System
│   └───__pycache__
├───dlib
│   └───examples
├───dlib-19.8.1.dist-info
├───static
│   └───images
│       ├───Faculty_Images
│       └───Student_Images
│           └───CSE
│               ├───1
│               │   └───A
│               └───2
│                   ├───A
│                   └───C
├───manage.py
├───db.sqlite3
└───requirements.txt
```
# Live Video of Attendance Management System
