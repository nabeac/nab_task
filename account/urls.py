from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views 

app_name='accounts'
urlpatterns = [
    # ...
    path('login/', views.MyLoginViwe.as_view(), {'template_name': 'registration/login.html'}, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(),{'template_name': 'registration/logged_out.html'}, name = 'logout')
]