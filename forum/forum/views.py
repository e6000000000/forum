from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from . import models


class SectionListView(ListView):
    model = models.Section
    context_object_name = 'sections'
    template_name = 'index.html'

class SectionDetailView(DetailView):
    model = models.Section
    context_object_name = 'section'
    template_name = 'section_details.html'

class ThreadDetailView(DetailView):
    model = models.Thread
    context_object_name = 'thread'
    template_name = 'thread_details.html'

class SectionCreateView(CreateView):
    model = models.Section
    template_name = 'section_create.html'
    fields = ['title', 'description']
    #success_url = reverse_lazy('index')

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('section_details', kwargs = {'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
