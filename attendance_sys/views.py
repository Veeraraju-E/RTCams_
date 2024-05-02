from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse

from django.conf import settings
# User = settings.AUTH_USER_MODEL
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendance, Course, Branch
from .filters import studentAttendanceFilter, facultyAttendanceFilter

from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date, datetime

import cv2, csv, openpyxl

@login_required(login_url = 'login')
def student_home(request):
    print("in student/login/home")
    if not request.user.is_authenticated:  # Check if the user is authenticated
        return redirect('studentLoginPage')
    studentForm = CreateStudentForm()
    print(request.GET.get('roll_num'))
    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        print(request.POST['roll_num'])
        stat = False 
        try:
            student = Student.objects.get(roll_num = request.POST['roll_num'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('student_home')
        else:
            messages.error(request, 'Student with Roll Number ' + request.POST['roll_num'] + ' already exists.')
            return redirect('student_home')

    context = {'studentForm':studentForm}
    return render(request, 'attendance_sys/student_home.html', context)

@login_required(login_url = 'login')
def faculty_home(request):
    if not request.user.is_authenticated:  # Check if the user is authenticated
        return redirect('facultyLoginPage')
    print("in facultylogin/home")
    print(request.method)
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data = request.POST, files=request.FILES)
        print(studentForm)
        # print(request.POST)
        stat = False 
        try:
            student = Student.objects.get(roll_num = request.POST['roll_num'])
            print(student)
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get('firstname') +" " +studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name + ' was successfully added.')
            return redirect('faculty_home')
        else:
            messages.error(request, 'Student with Roll Number '+request.POST['roll_num']+' already exists.')
            return redirect('faculty_home')

    context = {'studentForm':studentForm}
    print(context)
    return render(request, 'attendance_sys/faculty_home.html', context)

def studentLoginPage(request):
    print("in studentLoginPage")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            # print(user)
            return redirect('home/')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/student_login.html', context)

def facultyLoginPage(request):
    print("in facultyLoginPage")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home/')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/faculty_login.html', context)

def student_or_faculty_view(request):
    print("in student_or_faculty_view")
    context = {}
    return render(request, "attendance_sys/student_or_faculty.html", context)

def student_login(request):
    print("in student_login")
    return redirect("student/login")

def faculty_login(request):
    print("in faculty_login")
    return redirect("faculty/login")

@login_required(login_url = 'student/login')
def logoutStudent(request):
    logout(request)
    return redirect('../../student/login')

@login_required(login_url = 'faculty/login')
def logoutFaculty(request):
    logout(request)
    return redirect('../../faculty/login')

@login_required(login_url = 'login')
def updateStudentRedirect(request):
    print('in updateStudentRedirect')
    context = {}
    print(request.method)
    if request.method == 'GET':
        try:
            # print(request.user)
            roll_num = str(request.user)[:-11].upper()
            branch = roll_num[3:5]
            branch = Branch.objects.get(abbr=branch)
            student = Student.objects.get(roll_num = roll_num, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_roll_num':roll_num, 'student':student}
        except:
            messages.error(request, 'Student Does Not Exist')
            return redirect('student_home')
    return render(request, 'attendance_sys/student_update.html', context)

@login_required(login_url = 'login')
def updateStudent(request):
    print('in updateStudent')
    context = {}
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(roll_num = request.POST['prev_roll_num'])
            print(student, request.POST)
            updateStudentForm = CreateStudentForm(data = request.POST, files=request.FILES, instance = student)
            # print(updateStudentForm.as_p)
            context = {'form':updateStudentForm}
            print('in try')
            if updateStudentForm.is_valid():
                print('in try in if')
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('Student Home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('Student Home')
    return render(request, 'attendance_sys/student_update.html', context)

@login_required(login_url = 'login')
def update(request):
    print('in update')
    if request.method == 'POST':
        return redirect('updateStudent')
    studentForm = CreateStudentForm()
    context = {'studentForm':studentForm}
    return render(request, 'attendance_sys/faculty_update.html', context)

@login_required(login_url = 'login')
def register(request):
    studentForm = CreateStudentForm()
    context = {'studentForm':studentForm}
    print(request.method)
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        roll_num = request.POST.get('roll_num')
        print(roll_num)
        user = User.objects.create(
                        username = str(roll_num).lower() + '@iitj.ac.in',
                        password = make_password(roll_num),
                        is_student=True,
                        )
        
        student = Student.objects.create(
            user=user,
            firstname = request.POST.get('firstname'),
            lastname = request.POST.get('lastname'),
            branch = request.POST.get('branch'),
            roll_num = roll_num,
            year = request.POST.get('year'),
            course = request.POST.get('course'),
            profile_pic = request.POST.get('profile_pic'),
        )

        messages.success(request, 'Student Succesfully Added')
        user.save()
        student.save()

    return render(request, 'attendance_sys/faculty_update.html', context)

@login_required(login_url = 'login')
def startAttendance(request, branch, year, course):
    print(request.method)
    if request.method == 'GET':
        # print(request.user)
        details = {
            'branch':branch,
            'year': year,
            'course':course,
            # 'faculty':request.user.faculty
            }
        students = Student.objects.filter(branch=details['branch'], year=details['year'], course=details['course'])
        print(students)
        course_qs = Course.objects.filter(code=details['course'])
        roll_nums = Recognizer(details)
        print('if 1')
        for student in students:
            time_now = datetime.now()
            # print(time_now)
            hour = time_now.hour
            minute = time_now.minute
            second = time_now.second
            start_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            # print(start_time)
            # print(student.roll_num)
            if str(student.roll_num) in roll_nums:
                # print('creating new attendance')
                
                new_attendance = Attendance(
                                            # Faculty_Name = request.user.faculty, 
                                            roll_num=str(student.roll_num), 
                                            course=details['course'], 
                                            branch=details['branch'],
                                            date=str(date.today()),
                                            start_time = start_time,
                                            end_time = None,
                                            year=details['year'], 
                                            status='Present'
                                            )
                new_attendance.save()
                student_record = Student.objects.get(roll_num=student.roll_num)
                student_record.ta = 1
                student_record.save()
            else:
                new_attendance = Attendance(
                                            # Faculty_Name = request.user.faculty, 
                                            roll_num=str(student.roll_num), 
                                            course=details['course'], 
                                            branch=details['branch'],
                                            start_time=None,
                                            end_time=None,
                                            date=str(date.today()),
                                            year=details['year'],
                                            )   # default Status is Absent
                new_attendance.save()
                student_record = Student.objects.get(roll_num=student.roll_num)
                student_record.ta = 0
                student_record.save()
        attendances = Attendance.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], course = details['course'])
        course_start_time, course_end_time = '', ''
        for course in course_qs:
            course_start_time = course.start_time
            course_end_time = course.end_time
        context = {"attendances":attendances, 
                    "ta":True, 
                    'course_start_time':course_start_time, 
                    'course_end_time':course_end_time,
                    'course_code':details['course']
                    }
        messages.success(request, "Initial Attendance Recorded")
        return render(request, 'attendance_sys/faculty_attendance.html', context)        
    context = {}
    return render(request, 'attendance_sys/faculty_home.html', context)

@login_required(login_url = 'login')
def endAttendance(request, branch, year, course):
    if request.method == 'GET':
        details = {
            'branch':branch,
            'year': year,
            'course':course,
            # 'faculty':request.user.faculty
            }
        students = Student.objects.filter(branch=details['branch'], year=details['year'], course=details['course'], ta=1)
        # only those students whose attendance has been captured before
        course_qs = Course.objects.filter(code=details['course'])
        roll_nums = Recognizer(details)
        print('if 1')
        for student in students:
            time_now = datetime.now()
            # print(time_now)
            hour = time_now.hour
            minute = time_now.minute
            second = time_now.second
            end_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            if str(student.roll_num) in roll_nums:
                print(student.roll_num)
                student_record = Student.objects.get(roll_num=student.roll_num)
                student_record.ta = 0
                student_record.save()
                attendance_record = Attendance.objects.get(roll_num=student.roll_num, date=str(date.today()))
                
                attendance_record.end_time = end_time
                attendance_record.save()
            else:
                new_attendance = Attendance(
                                            # Faculty_Name = request.user.faculty, 
                                            roll_num = str(student.roll_num), 
                                            course = details['course'],
                                            branch = details['branch'], 
                                            year = details['year'],
                                            endtime = None,
                                            status = 'Proxy'
                                            )
                new_attendance.save()
                student_record = Student.objects.get(roll_num=student.roll_num)
                student_record.ta = 0
                student_record.save()
        attendances = Attendance.objects.filter(date = str(date.today()),branch = details['branch'], year = details['year'], course = details['course'])
        # print(attendances.all().values())
        course_start_time, course_end_time = '', ''
        for course in course_qs:
            course_start_time = course.start_time
            course_end_time = course.end_time
        context = {"attendances":attendances, 
                    "ta":True, 
                    'course_start_time':course_start_time, 
                    'course_end_time':course_end_time,
                    'course_code':details['course']
                    }
        messages.success(request, "Final Attendance Recorded")
        return render(request, 'attendance_sys/faculty_attendance.html', context)        
    context = {}
    return render(request, 'attendance_sys/faculty_home.html', context)

@login_required(login_url='login')
def takeAttendance(request):
    if request.method == 'POST':
        if 'attendance_action' in request.POST:
            action = request.POST['attendance_action']
            details = {
                'branch':request.POST['branch'],
                'year': request.POST['year'],
                'course':request.POST['course'],
                # 'faculty':request.user.faculty
                }
            course_qs = Course.objects.filter(code=details['course'])
            course_start_time, course_end_time = '', ''
            for course in course_qs:
                course_start_time = course.start_time
                course_end_time = course.end_time
            # print(type(course_end_time), type(course_start_time))
            hour = course_start_time.hour
            minute = course_start_time.minute
            second = course_start_time.second
            course_start_time = int(f"{hour:02d}{minute:02d}{second:02d}")

            hour = course_end_time.hour
            minute = course_end_time.minute
            second = course_end_time.second
            course_end_time = int(f"{hour:02d}{minute:02d}{second:02d}")

            current_time = datetime.now()
            hour = current_time.hour
            minute = current_time.minute
            second = current_time.second
            curr_time = int(f"{hour:02d}{minute:02d}{second:02d}")

            # print(course_start_time, course_end_time, curr_time)

            if action == 'start':
                if curr_time > course_start_time + 500:
                    messages.error(request, "Can't take attendance now as start time exceeded. Contact admin for help")
                    return render(request, 'attendance_sys/faculty_home.html', {})
                elif curr_time < course_start_time - 1000:
                    messages.error(request, "Can't take attendance now. Please wait until 10 minutes before the class starts. Contact admin for help")
                    return render(request, 'attendance_sys/faculty_home.html', {})
                else:
                    return redirect('start_attendance', **details)
            elif action == 'end':
                if curr_time > course_end_time + 500:
                    messages.error(request, "Can't take attendance now as end time exceeded. Contact admin for help")
                    return render(request, 'attendance_sys/faculty_home.html', {})
                elif curr_time < course_end_time - 1000:
                    messages.error(request, "Can't take attendance now. Please wait until 10 minutes before class ends. Contact admin for help")
                    return render(request, 'attendance_sys/faculty_home.html', {})
                else:
                    return redirect('end_attendance', **details)
            else:
                messages.error(request, 'Invalid action')
                return render(request, 'attendance_sys/faculty_home.html', {})
        else:
            messages.error(request, 'Attendance action not specified')
            return render(request, 'attendance_sys/faculty_home.html', {})
    else:
        messages.error(request, 'Invalid request method')
        return render(request, 'attendance_sys/faculty_home.html', {})


def student_searchattendance(request):
    if request.method == 'GET':
        # roll_num = request.GET.get('roll_num')
        roll_num = str(request.user)[:-11].upper()
        print(roll_num)
        course = request.GET.get('course')
        attendances = Attendance.objects.filter(roll_num=roll_num, course=course)
        myFilter = studentAttendanceFilter(request.GET, queryset=attendances)
        attendances = myFilter.qs
        courses = Course.objects.filter(code=course)
        course_start_time, course_end_time = '', ''
        for course in courses:
            course_start_time = course.start_time
            course_end_time = course.end_time
        context = {'attendances': attendances, 
                   'ta':False, 
                   'myFilter': myFilter, 
                   'course_start_time':course.start_time, 
                   'course_end_time':course.end_time,
                   'course':course,
                   'roll_num':'roll_num'
                   }
        return render(request, 'attendance_sys/student_attendance.html', context)

def faculty_searchattendance(request):
    if request.method == 'GET':
        course_code = request.GET.get('course')
        attendances = Attendance.objects.filter(course=course_code)
        myFilter = facultyAttendanceFilter(request.GET, queryset=attendances)
        attendances = myFilter.qs
        courses = Course.objects.filter(code=course_code)
        course_start_time, course_end_time = '', ''
        for course in courses:
            course_start_time = course.start_time
            course_end_time = course.end_time
        context = {'attendances': attendances, 
                   'ta': False, 
                   'myFilter': myFilter, 
                   'course_start_time':course_start_time, 
                   'course_end_time':course_end_time,
                   'course_code':course_code
                   }
        return render(request, 'attendance_sys/faculty_attendance.html', context)


def download_csv(request, course):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{course}_attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Branch', 'Entry Time','Exit Time', 'Status', 'Course'])

    attendances = Attendance.objects.filter(course=course)  # Adjust this queryset as per your requirement

    for attendance in attendances:
        writer.writerow([attendance.roll_num, attendance.branch, attendance.start_time,
                         attendance.end_time, attendance.status, attendance.course])

    return response

def download_excel(request, course):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{course}_attendance.xlsx"'
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(['Roll Number', 'Branch','Entry Time','Exit Time', 'Status','Course'])

    attendances = Attendance.objects.filter(course=course)  # Adjust this queryset as per your requirement

    for attendance in attendances:
        worksheet.append([attendance.roll_num, attendance.branch, attendance.start_time,
                           attendance.end_time, attendance.status, attendance.course])

    workbook.save(response)
    return response

def download_student_csv(request, course, roll_num):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{course}_{roll_num}_attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Roll Number', 'Branch', 'Your Entry Time', 'Your Exit Time', 'Attendance', 'Course'])

    attendances = Attendance.objects.filter(course=course, roll_num=roll_num)

    for attendance in attendances:
        writer.writerow([attendance.roll_num, attendance.branch, attendance.start_time,
                         attendance.end_time, attendance.status, attendance.course])

    return response

def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance = faculty)
    context = {'form':form}
    return render(request, 'attendance_sys/facultyForm.html', context)

def studentProfile(request):
    form = StudentForm()
    context = {'form':form}
    return render(request, 'attendance_sys/student_update.html', context)

def download_student_excel(request, course, roll_num):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{course}_{roll_num}_attendance.xlsx"'
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(['Roll Number', 'Branch','Your Entry Time','Your Exit Time', 'Attendance','Course'])

    attendances = Attendance.objects.filter(course=course, roll_num=roll_num)

    for attendance in attendances:
        worksheet.append([attendance.roll_num, attendance.branch, attendance.start_time,
                           attendance.end_time, attendance.status, attendance.course])

    workbook.save(response)
    return response


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def videoFeed(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("aborted")

def getVideo(request):
    return render(request, 'attendance_sys/templates/videoFeed.html')