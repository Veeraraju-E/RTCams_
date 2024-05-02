from django.contrib import admin
from .models import *

# Register your models here.    

class FacultyAdmin(admin.ModelAdmin):
    # Define fields or fieldsets as needed
    pass

class StudentAdmin(admin.ModelAdmin):
    # Define fields or fieldsets as needed
    pass



admin.site.register(User)

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance)