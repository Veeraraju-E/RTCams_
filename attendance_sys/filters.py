import django_filters

from .models import Attendance, Faculty

class studentAttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['Faculty_Name', 'branch', 'student', 'start_time', 'end_time', 'year', 'course', 'roll_num']

class facultyAttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['Faculty_Name', 'branch', 'student', 'course', 'year', 'start_time', 'end_time']

# class facultyProfileFilter(django_filters.FilterSet):
#     class Meta:
#         model = Faculty
#         fields = '__all__'
#         exclude = ['faculty']