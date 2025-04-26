from django.db import models
from extenstios . utils import django_jalali, jalalitime
import django_jalali.db.models as jmodels
from account.models import User


def task_image_path(Blog, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    # return 'product_{0}/{1}'.format(image.product.id, filename)
    return f'{Task.title}/{filename}'


def task_file_path(Task, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    # return 'product_{0}/{1}'.format(image.product.id, filename)
    return f'tasks/{Task.title}/{filename}'


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField()
    creator = models.ForeignKey(User, related_name='creator_tasks', on_delete=models.CASCADE)
    main_responsible = models.ForeignKey(User, related_name='main_responsible_tasks', on_delete=models.CASCADE)
    review_by =  models.ForeignKey(User, related_name='review_by_tasks', on_delete=models.CASCADE, null=True, blank=True)
    task_file = models.FileField(upload_to='task_file_path',null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    STATUS_CHOICES = [
        ('in_progress', 'درحال بررسی'),
        ('working', 'در حال انجام'),
        ('done', 'تکمیل شده'),
        ('error', ' به مشکل خورد'),
        ('rejected', 'رد شده'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def get_status_color(self):
        return {
            'in_progress': 'yellow-400',
            'done': 'green-800',
            'working':'green-400',
            'error':'red-600',
            'rejected': 'gray-600',
        }.get(self.status, 'gray-200')

    def __str__(self):
        return f'task : {self.title} __ for :{self.main_responsible}'

    def start_time(self):
        return django_jalali(self.start_date)
    
    def end_time(self):
        return django_jalali(self.end_date)
    

class Activity(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    time = models.DateField(auto_now_add=True)
    task = models.ForeignKey(Task, related_name='activities', on_delete=models.CASCADE)
    activity_file = models.FileField(upload_to='task_file_path',null=True, blank=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    review_by = models.ForeignKey(User, related_name='review_by', on_delete=models.CASCADE, null=True, blank=True)

    def timeset(self):
        return jalalitime(self.time)
    

    STATUS_CHOICES = [
        ('in_progress', 'درحال بررسی'),
        ('working', 'در حال انجام'),
        ('done', 'تکمیل شده'),
        ('error', ' به مشکل خورد'),
        ('rejected', 'رد شده'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    


# class Communication(models.Model):
#     comment = models.CharField(max_length=100)
#     user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, related_name='commentt', on_delete=models.CASCADE)
#     reply = models.ForeignKey("self", related_name='commentt', on_delete=models.CASCADE)
#     c_date = models.DateField(auto_now_add=True)
#     m_date = models.DateField(auto_now=True)

#     def __str__(self):
#         return f'{self.user}=={self.task}'

#     def start_date(self):
#         return self.c_date

# class Task(models.Model):
#     #موضوع
#     title = models.CharField(max_length=50)
#     #دستور عمل
#     description = models.TextField()
#     #تاریخ شروع
#     start_date = models.DateField()  
#     #تاریخ پایان
#     end_date = models.DateField() 
#     #فایل صوتی توضیحات بیشتر
#     # audio_file = None 
#     # #سرپرست
#     # supervisor = None 
#     # #ایجاد کننده
#     # creator = None 
#     # #مسئول اصلی تسک
#     # main_responsible = None 
#     # #درحال برسی توسط
#     # review_by = None 
#     #وضعیت
#     status = (
#         'درحال انجام',
#         'اتمام تسک',
#     )