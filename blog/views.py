from django.views.generic import ListView, DetailView

from django.shortcuts import render

from blog.models import Blog


class BlogListView(ListView):

    model = Blog


class BlogDetailView(DetailView):

    model = Blog
