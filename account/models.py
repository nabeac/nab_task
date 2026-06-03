import jdatetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from statistics import mean



class User(AbstractUser):
    phone = models.CharField(max_length=100, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    body = models.CharField(max_length=50, default='n')
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
            





    def get_course_stats(user, course):
        reports = course.course_re.filter(student=user).order_by("day")

        aggregates = reports.aggregate(
            total_videos_watched=Sum("videos_number"),
            total_hours_watched=Sum("hours_number"),
        )

        watched_videos = aggregates["total_videos_watched"] or 0
        total_hours_watched = aggregates["total_hours_watched"] or 0

        total_videos = course.videos or 0
        total_course_hours = course.hours or 0

        # جلوگیری از بیشتر شدن از سقف
        if total_videos:
            watched_videos = min(watched_videos, total_videos)

        remaining_videos = total_videos - watched_videos

        progress_percent = 0
        if total_videos:
            progress_percent = round((watched_videos / total_videos) * 100, 1)
            circumference = 289
            progress_offset = circumference * (1 - progress_percent / 100)

            

        # -----------------------------
    
        if reports.exists():
            first_day = reports.first().day
            today = timezone.now().date()
            total_days = (today - first_day).days + 1
            average_daily_hours = round(total_hours_watched / total_days, 2) if total_days > 0 else 0
        else:
            average_daily_hours = 0


        gaps = []
        report_days = list(reports.values_list("day", flat=True))

        for i in range(1, len(report_days)):
            gap = (report_days[i] - report_days[i - 1]).days
            gaps.append(gap)

        if gaps:
            max_gap = max(gaps)
            min_gap = min(gaps)
            avg_gap = round(mean(gaps), 2)
        else:
            max_gap = min_gap = avg_gap = 0

        # فاصله از آخرین مطالعه تا امروز
        if report_days:
            current_gap = (timezone.now().date() - report_days[-1]).days
        else:
            current_gap = 0

        
        today = jdatetime.date.today()
        last_7_days_data = []

        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_hours = reports.filter(day=day).aggregate(
                total=Sum("hours_number")
            )["total"] or 0

            last_7_days_data.append({
                "day": day,
                "hours": float(day_hours),
            })

      
        return {
            "total_videos": total_videos,
            "watched_videos": watched_videos,
            "remaining_videos": remaining_videos,
            "progress_percent": progress_percent,
            "progress_offset": progress_offset,
            
            "total_hours_watched": total_hours_watched,
            "average_daily_hours": average_daily_hours,

            "max_gap": max_gap,
            "min_gap": min_gap,
            "avg_gap": avg_gap,
            "current_gap": current_gap,

            "gaps_list": gaps,
            "last_7_days": last_7_days_data,
        }


