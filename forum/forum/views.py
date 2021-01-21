from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from extra_views import CreateWithInlinesView, InlineFormSet

from . import models


class SectionListView(ListView):
    """
    Display a list of :model:`forum.Section`.
    """
    model = models.Section
    context_object_name = 'sections'
    template_name = 'forum/index.html'

class SectionDetailView(DetailView):
    """
    Display a :model:`forum.Section`.
    """
    model = models.Section
    context_object_name = 'section'
    template_name = 'forum/section_details.html'

class ThreadDetailView(DetailView):
    """
    Display a :model:`forum.Thread`.
    """
    model = models.Thread
    context_object_name = 'thread'
    template_name = 'forum/thread_details.html'

class SectionCreateView(CreateView):
    """
    Display a creation form of :model:`forum.Section`
    """
    model = models.Section
    template_name = 'forum/section_create.html'
    fields = ['title', 'description']

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('section_details', kwargs = {
                'pk': self.object.pk
            })

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))

        form.instance.author = self.request.user
        
        return super().form_valid(form)

class PostInline(InlineFormSet):
    """
    InlineFormSet of :model:`forum.Post`
    """
    model = models.Post
    fields = ['text']

    factory_kwargs = {
        'can_delete': False,
        'can_order': False,
        'extra': 1,
    }

class ThreadCreateView(CreateWithInlinesView):
    """
    Display a creation form of :model:`forum.Thread` and 
    first :model:`forum.Post` to this Thread
    """
    model = models.Thread
    inlines = [PostInline]

    template_name = 'forum/thread_create.html'
    fields = ['title']

    def get_success_url(self, **kwargs):
        if  kwargs != None:
            return reverse_lazy('thread_details', kwargs = {
                'section_pk': self.object.section.pk,
                'pk': self.object.pk
            })

    def forms_valid(self, form, inlines):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))

        section_pk = self.kwargs['section_pk']

        form.instance.author = self.request.user
        try:
            form.instance.section = models.Section.objects.get(pk=section_pk)
        except models.Section.DoesNotExist:
            return HttpResponseBadRequest(f'section with pk={section_pk} does not exist')

        for formtype in inlines:
            for form in formtype:
                form.instance.author = self.request.user

        return super().forms_valid(form, inlines)

class PostReplyCreateView(CreateView):
    """
    Display a creation form of :model:`forum.Post` 
    which is a reply to some :model:`forum.Post` in the same :model:`forum.Thread`
    """
    model = models.Post
    template_name = 'forum/postreply_create.html'
    fields = ['text']

    def get_context_data(self, **kwargs):
        post_pk = self.kwargs['post_pk']
        try:
            kwargs['post'] = models.Post.objects.get(pk=post_pk)
        except models.Post.DoesNotExist:
            return HttpResponseBadRequest(f'post with pk={post_pk} does not exist')

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))

        post_pk = self.kwargs['post_pk']
        thread_pk = self.kwargs['thread_pk']

        form.instance.author = self.request.user
        try:
            form.instance.reply_to = models.Post.objects.get(pk=post_pk)
            form.instance.thread = models.Thread.objects.get(pk=thread_pk)
        except models.Post.DoesNotExist:
            return HttpResponseBadRequest(f'post with pk={post_pk} does not exist')
        except models.Thread.DoesNotExist:
            return HttpResponseBadRequest(f'thread with pk={thread_pk} does not exist')

        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('thread_details', kwargs = {
                'section_pk': self.object.thread.section.pk,
                'pk': self.object.thread.pk
            })

