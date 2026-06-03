from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView ,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from persiantools.jdatetime import JalaliDate
from account.models import User
from .models import Task, Activity, Report, Course
from django.core.paginator import Paginator
from .forms import TaskForm ,ActivityForm, ReportForm
from django.db.models import Q

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by('-id')

    # گرفتن پارامترهای GET
    q = (request.GET.get('q') or '').strip()
    status = (request.GET.get('status') or '').strip()
    filter_type = (request.GET.get('filter_type') or 'all').strip()

    # سرچ
    if q:
        tasks = tasks.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(creator__username__icontains=q) |
            Q(creator__first_name__icontains=q) |
            Q(creator__last_name__icontains=q) |
            Q(main_responsible__username__icontains=q) |
            Q(main_responsible__first_name__icontains=q) |
            Q(main_responsible__last_name__icontains=q) |
            Q(review_by__username__icontains=q) |
            Q(review_by__first_name__icontains=q) |
            Q(review_by__last_name__icontains=q)
        ).distinct()

    # فیلتر وضعیت
    if status:
        tasks = tasks.filter(status=status)

    # فیلتر تسک‌های من
    if filter_type == 'mine':
        tasks = tasks.filter(
            Q(creator=request.user) |
            Q(main_responsible=request.user) |
            Q(review_by=request.user)
        ).distinct()
    
    paginator = Paginator(tasks, 5)  # هر صفحه 5 تسک
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "task": page_obj,
        "page_obj": page_obj,
        "q": q,
        "selected_status": status,
        "filter_type": filter_type,
    }

    return render(request, 'task/task_list.html', context)


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    queryset = Task.objects.all()
    context_object_name = 'task_view'
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = self.get_object().activities.all()  # related_name = 'activity'
        context['activity_form'] = ActivityForm()

        return context

    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.task = self.object
            activity.creator = request.user
            activity.save()

            if activity.review_by:
                self.object.review_by = activity.review_by
                self.object.save()
            
            if activity.status:
                self.object.status = activity.status
                self.object.save()

            return redirect(self.request.path_info)

            
        # اگر فرم نامعتبر بود، دوباره صفحه را با ارورها نمایش بده
        context = self.get_context_data()
        context['activity_form'] = form
        return self.render_to_response(context)
    
    # آپدیت فیلد review_by تسک با یوزری که توی این اکتیویتی انتخاب شده
        

# @login_required
# def task_view(request, pk):
#     question = Task.objects.get(pk=pk)
#     return render(request, 'task/task_view.html', {'task_view': question})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/create_form.html'
    success_url = reverse_lazy('home:list_task')

# اینجا اون دوتا فیلی که برای زمان هست به سمتش ارسال میشه و میگیره فرمتش میکنه و میفرسته سمت مدل
    def form_valid(self, form):

        form.instance.creator = self.request.user
        
        start_jalali = self.request.POST.get('start_date')
        end_jalali = self.request.POST.get('end_date')

        if start_jalali:
            y, m, d = map(int, start_jalali.split('/'))
            form.instance.start_date = JalaliDate(y, m, d).to_gregorian()

        if end_jalali:
            y, m, d = map(int, end_jalali.split('/'))
            form.instance.end_date = JalaliDate(y, m, d).to_gregorian()

        return super().form_valid(form)
    
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'task/report_form.html'
    success_url = reverse_lazy('home:list_task')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# اینجا اون دوتا فیلی که برای زمان هست به سمتش ارسال میشه و میگیره فرمتش میکنه و میفرسته سمت مدل
    def form_valid(self, form):

        form.instance.student = self.request.user
        form.instance.day = timezone.localdate()
        return super().form_valid(form)




class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "profile_view"
    template_name = "task/profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # ---------------------------------
        # GET Parameters
        # ---------------------------------
        status = self.request.GET.get("status")
        role = self.request.GET.get("role")
        course_id = self.request.GET.get("course")
        page_number = self.request.GET.get("page")

       

        # Base queryset (همیشه از این شروع می‌کنیم)
        tasks = Task.objects.filter(
            Q(main_responsible=user) |
            Q(creator=user) |
            Q(review_by=user)
        ).distinct()

        # ---- Role Filter (بدون overwrite)
        if role in ["creator", "responsible", "review"]:
            if role == "creator":
                tasks = tasks.filter(creator=user)

            elif role == "responsible":
                tasks = tasks.filter(main_responsible=user)

            elif role == "review":
                tasks = tasks.filter(review_by=user)

        # ---- Status Filter
        if status:
            tasks = tasks.filter(status=status)

        # ---- Order (خیلی مهم برای pagination پایدار)
        tasks = tasks.order_by("-id")

        # ---- Pagination
        paginator = Paginator(tasks, 5)
        page_obj = paginator.get_page(page_number)

    

        courses = Course.objects.filter(student=user)

        selected_course = None
        stats = {}

        if courses.exists():
            if course_id:
                selected_course = courses.filter(id=course_id).first()
            else:
                selected_course = courses.first()

            if selected_course:
                stats = user.get_course_stats(selected_course)

      
        context.update({
            "page_obj": page_obj,
            "tasks": page_obj.object_list,  # مهم 
            "selected_status": status,
            "selected_role": role,
            "courses": courses,
            "selected_course": selected_course,
        })

        context.update(stats)

        return context



def todolist(request):
    return render(request, 'task/todo_list.html')