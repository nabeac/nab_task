from django.contrib import admin
from .models import Task, Activity, Course, Report


admin.site.register(Task)

admin.site.register(Activity)
admin.site.register(Course)
admin.site.register(Report)


