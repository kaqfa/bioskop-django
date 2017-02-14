from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Movie

class IndexView(ListView):
    model = Movie
    template_name = 'dashboard.html'
