from django import forms
from .models import Task, Activity, Report, Course
import django_jalali.forms as jforms 

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude  = ['creator', 'start_date', 'end_date','completed_at']



class ReportForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['course'].queryset = Course.objects.filter(student=user)

    class Meta:
        model = Report
        exclude = ['student', 'day']




class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'activity_file', 'review_by','status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # این خط لیبل رو حذف می‌کنه