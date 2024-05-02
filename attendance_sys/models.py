from django.db import models

from django.contrib.auth.models import User, AbstractUser


def user_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.firstname + instance.lastname
    filename = name +'.'+ ext 
    return 'Faculty_Images/{}'.format(filename)

    
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)


class Faculty(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    # email = models.EmailField(max_length=200, null=True, blank=True)
    # faculty = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return str(self.firstname + " " + self.lastname)


def student_directory_path(instance, filename): 
    name, ext = filename.split(".")
    name = instance.roll_num
    filename = name +'.'+ ext 
    return 'Student_Images/{}/{}/{}'.format(instance.branch,instance.year,filename)

class Student(models.Model):

    BRANCH = (
        ('CSE','CSE'),
        ('AIDE','AIDE'),
        ('BSBE', 'BSBE'),
        ('Chemical Engg','Chemical Engg'),
        ('Chemistry', 'Chemistry'),
        ('Physics', 'Physics'),
        ('CI', 'CI'),
        ('MECH','MECH'),
        ('EE','EE'),
        ('MT', 'MT')
    )
    YEAR = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    # email = models.EmailField(max_length=200, null=True, blank=True)
    firstname = models.CharField(max_length=200, null=True, blank=True)
    lastname = models.CharField(max_length=200, null=True, blank=True)
    roll_num = models.CharField(max_length=15, null=True)
    branch = models.CharField(max_length=25, null=True, choices=BRANCH)
    ta = models.IntegerField(null=True, blank=True)  # 0 represents attendance not taken
    year = models.CharField(max_length=10, null=True, choices=YEAR)
    course = models.CharField(max_length=75, null=True)
    profile_pic = models.ImageField(upload_to=student_directory_path, null=True, blank=True)


    def __str__(self):
        return str(self.roll_num)

class Attendance(models.Model):
    # faculty = models.ForeignKey(Faculty, null = True, on_delete= models.SET_NULL)
    student = models.ForeignKey(Student, null = True, on_delete= models.SET_NULL)
    Faculty_Name = models.CharField(max_length=200, null=True, blank=True)
    roll_num = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField(auto_now_add = True, null = True)
    start_time = models.TimeField(null = True)
    end_time = models.TimeField(null = True)
    branch = models.CharField(max_length=10, null = True)
    year = models.CharField(max_length=10, null = True)
    course = models.CharField(max_length=75, null = True)
    status = models.CharField(max_length=10, null = True, default='Absent')

    def __str__(self):
        return str(self.roll_num + "_" + str(self.date)+ "_" + str(self.course))
    
class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    faculty = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} : {self.code}"
    
class Branch(models.Model):
    abbr = models.CharField(max_length=10)
    branch = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.branch}"
