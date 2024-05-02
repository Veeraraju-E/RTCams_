from django.urls import path

from . import views

urlpatterns = [
    path('', views.student_or_faculty_view, name='Choose User'),
    path('student/login/home/', views.student_home, name = 'Student Home'),
    path('faculty/login/home/', views.faculty_home, name = 'Faculty Home'),
    path('student/login/', views.studentLoginPage, name=' Student login'),
    path('faculty/login/', views.facultyLoginPage, name=' Faculty login'),
    path('student/logout/', views.logoutStudent, name='Student logout'),
    path('faculty/logout/', views.logoutFaculty, name='Faculty logout'),
    path('student/searchattendance/', views.student_searchattendance, name='Student searchattendance'),
    path('faculty/searchattendance/', views.faculty_searchattendance, name='Faculty searchattendance'),
    path('student/account/', views.updateStudentRedirect, name='updateStudentRedirect'),
    path('faculty/account/', views.facultyProfile, name='Faculty account'),
    path('faculty/register', views.register, name='Faculty register' ),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('attendance/', views.takeAttendance, name='attendance'),
    path('start_attendance/<str:branch>/<str:year>/<str:course>/', views.startAttendance, name='start_attendance'),
    path('end_attendance/<str:branch>/<str:year>/<str:course>/', views.endAttendance, name='end_attendance'),
    path('video_feed/', views.videoFeed, name='video_feed'),
    path('videoFeed/', views.getVideo, name='videoFeed'),
    path('download_csv/<str:course>/', views.download_csv, name='download_csv'),
    path('download_excel/<str:course>/', views.download_excel, name='download_excel'),
    path('download_student_csv/<str:course>/<str:roll_num>/', views.download_student_csv, name='download_student_csv'),
    path('download_student_excel/<str:course>/<str:roll_num>/', views.download_student_excel, name='download_student_excel')
]