import jdatetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class User(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)

    # def get_task_summary(self):
    #     all_tasks = self.main_responsible_tasks.all()
    #     today_m = timezone.localdate()
    #     # start_of_month_m = today.replace(day=1)
    #     today_jalali = jdatetime.date.today()
    #     start_of_month = today_jalali.replace(day=1).togregorian()
    #     today = today_jalali.togregorian()

    #     return {
    #         'total': all_tasks.count(),
    #         'this_month': all_tasks.filter(start_date__gte=start_of_month).count(),
    #         'done': all_tasks.filter(status='done').count(),
    #         'done_this_month': all_tasks.filter(
    #             status='done',
    #             completed_at__gte=start_of_month
    #         ).count(),
    #         'working': all_tasks.filter(status='working').count(),
    #         'delayed': all_tasks.filter(end_date__lt=today).exclude(status='done').count(),
    #     }

    def get_task_summary(self):
        all_tasks = self.main_responsible_tasks.all()
        all_tasks_review_by = self.main_responsible_tasks.all()

        today_jalali = jdatetime.date.today()
        start_of_month_jalali = today_jalali.replace(day=1)

        return {
            'total': all_tasks.count(),

            # چون start_date جلالی است → جلالی مقایسه می‌کنیم
            'this_month': all_tasks.filter(
                start_date__gte=start_of_month_jalali
            ).count(),

            'done': all_tasks.filter(
                status='done'
            ).count(),

            # completed_at میلادی است → باید میلادی مقایسه شود
            'done_this_month': all_tasks.filter(
                status='done',
                completed_at__gte=start_of_month_jalali.togregorian()
            ).count(),

            'working': all_tasks.filter(
                status='working'
            ).count(),

            # end_date جلالی است → باید با جلالی مقایسه شود
            'delayed': all_tasks.filter(
                end_date__lt=today_jalali
            ).exclude(status='done').count(),
        }
    


    def get_tasks(self):
        today = jdatetime.date.today()

        my_tasks = self.main_responsible_tasks.all()
        review_tasks = self.review_by_tasks.all()
        created_tasks = self.creator_tasks.all()

        return {

            # -----------------------
            # مسئول اصلی (کارهای من)
            # -----------------------

            'my_tasks_all': my_tasks.order_by('-id'),

            'my_tasks_done': my_tasks.filter(
                status='done'
            ).order_by('-completed_at'),

            'my_tasks_working': my_tasks.filter(
                status='working'
            ).order_by('end_date'),

            'my_tasks_in_progress': my_tasks.filter(
                status='in_progress'
            ).order_by('start_date'),

            'my_tasks_delayed': my_tasks.filter(
                end_date__lt=today
            ).exclude(status='done').order_by('end_date'),

            'my_tasks_error': my_tasks.filter(
                status='error'
            ).order_by('-id'),

            'my_tasks_rejected': my_tasks.filter(
                status='rejected'
            ).order_by('-id'),

            # -----------------------
            # کارهایی که باید بررسی کنم
            # -----------------------

            'review_tasks_all': review_tasks.order_by('-id'),

            'review_tasks_pending': review_tasks.filter(
                status='in_progress'
            ).order_by('end_date'),

            'review_tasks_done': review_tasks.filter(
                status='done'
            ).order_by('-completed_at'),

            # -----------------------
            # کارهایی که من ساختم
            # -----------------------

            'created_tasks_all': created_tasks.order_by('-id'),

            'created_tasks_active': created_tasks.exclude(
                status='done'
            ).order_by('end_date'),

            'created_tasks_done': created_tasks.filter(
                status='done'
            ).order_by('-completed_at'),
        }
            

