from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib import messages





class MyLoginViwe(auth_views.LoginView):

    def get_success_url(self):
        return reverse_lazy('home:list_task') 