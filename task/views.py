from django.shortcuts import render, redirect
from django.views.generic import CreateView ,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from persiantools.jdatetime import JalaliDate
from account.models import User
from .models import Task, Activity
from .forms import TaskForm ,ActivityForm


@login_required
def task_list(request):
    question = Task.objects.all().order_by('-id')  # آخرین تسک‌ها براساس ID

    return render(request, 'task/task_list.html', {'task': question})

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
        start_jalali = self.request.POST.get('start_date')
        end_jalali = self.request.POST.get('end_date')

        if start_jalali:
            y, m, d = map(int, start_jalali.split('/'))
            form.instance.start_date = JalaliDate(y, m, d).to_gregorian()

        if end_jalali:
            y, m, d = map(int, end_jalali.split('/'))
            form.instance.end_date = JalaliDate(y, m, d).to_gregorian()

        return super().form_valid(form)




        
        




