from django import forms
from .models import Task, Activity
import django_jalali.forms as jforms 

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        exclude  = ['start_date', 'end_date']



class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'activity_file', 'review_by','status']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # این خط لیبل رو حذف می‌کنه