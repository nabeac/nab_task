import jdatetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)

    def get_task_summary(self):
        all_tasks = self.main_responsible_tasks.all()

        today_jalali = jdatetime.date.today()
        start_of_month = today_jalali.replace(day=1).togregorian()
        today = today_jalali.togregorian()

        return {
            'total': all_tasks.count(),
            'this_month': all_tasks.filter(start_date__gte=start_of_month).count(),
            'done': all_tasks.filter(status='done').count(),
            'done_this_month': all_tasks.filter(
                status='done',
                completed_at__gte=start_of_month
            ).count(),
            'working': all_tasks.filter(status='working').count(),
            'delayed': all_tasks.filter(end_date__lt=today).exclude(status='done').count(),
        }
