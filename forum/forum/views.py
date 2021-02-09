from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from extra_views import CreateWithInlinesView

from core.exceptions import *
from .models import *
from .services import *
from core.views import BaseView


class SectionListView(BaseView, ListView):
    """
    Display a list of `forum.Section` model.
    """
    model = Section
    context_object_name = 'sections'
    template_name = 'forum/index.html'


class SectionDetailView(BaseView, DetailView):
    """
    Display a `forum.Section` model.
    """
    model = Section
    context_object_name = 'section'
    template_name = 'forum/section_details.html'


class ThreadDetailView(BaseView, DetailView):
    """
    Display a forum.Thread` model.
    """
    model = Thread
    context_object_name = 'thread'
    template_name = 'forum/thread_details.html'


@method_decorator(login_required, name='dispatch')
class SectionCreateView(BaseView, CreateView):
    """
    Display a creation form for `forum.Section` model
    """
    model = Section
    template_name = 'forum/section_create.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        self._before_form_validation(form)
        return super().form_valid(form)

    def _before_form_validation(self, form):
        form.instance.author = self.request.user


@method_decorator(login_required, name='dispatch')
class ThreadCreateView(BaseView, CreateWithInlinesView):
    """
    Display a creation form for `forum.Thread` model and 
    first `forum.Post` model to this Thread
    """
    model = Thread
    inlines = [PostInline]

    template_name = 'forum/thread_create.html'
    fields = ['title']

    def forms_valid(self, form, inlines):
        try:
            self._before_forms_validation(form, inlines)
        except Section.DoesNotExist:
            raise HttpError(
                404,
                f'section with pk={section_pk} does not exist'
            )

        return super().forms_valid(form, inlines)
    
    def _before_forms_validation(self, form, inlines):
        section_pk = self.kwargs['section_pk']

        form.instance.author = self.request.user
        form.instance.section = Section.objects.get(pk=section_pk)
    
        for formtype in inlines:
            for inline_form in formtype:
                inline_form.instance.author = self.request.user


@method_decorator(login_required, name='dispatch')
class PostReplyCreateView(BaseView, CreateView):
    """
    Display a creation form for `forum.Post` model 
    which is a reply to some `forum.Post` model in the same `forum.Thread` model
    """
    model = Post
    template_name = 'forum/postreply_create.html'
    fields = ['text']

    def get_context_data(self, **kwargs):
        post_pk = self.kwargs['post_pk']
        try:
            kwargs['post'] = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise HttpError(
                404,
                f'post with pk={post_pk} does not exist'
            )

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            self._before_form_validation(form)
        except Post.DoesNotExist:
            raise HttpError(
                404,
                f'post with pk={post_pk} does not exist'
            )
        except Thread.DoesNotExist:
            raise HttpError(
                404,
                f'thread with pk={thread_pk} does not exist'
            )
        except ThreadClosed:
            raise HttpError(
                403,
                f'thread with pk={thread_pk} is closed'
            )
        
        return super().form_valid(form)
    
    def _before_form_validation(self, form):
        post_pk = self.kwargs['post_pk']
        thread_pk = self.kwargs['thread_pk']

        form.instance.author = self.request.user
        form.instance.reply_to = Post.objects.get(
            pk=post_pk
        )
        form.instance.thread = Thread.objects.get(
            pk=thread_pk
        )

        if form.instance.thread.is_closed:
            raise ThreadClosed()


@method_decorator(login_required, name='dispatch')
class ThreadUpdateView(BaseView, View):
    """
    Toggle `is_closed` bool variable of `forum.Thread` model
    """
    def get(self, *args, **kwargs):
        thread_pk = kwargs['pk']

        try:
            self.thread = toggle_thread_is_closed(
                thread_pk,
                self.request.user
            )
        except PermissionsDenied:
            raise HttpError(
                403,
                f'only author can close or open their threads'
            )
        except Thread.DoesNotExist:
            raise HttpError(
                404,
                f'thread with pk={thread_pk} does not exist'
            )

        return HttpResponseRedirect(
            self.thread.get_absolute_url()
        )


class SearchResultsView(BaseView, TemplateView):
    """
    Display results of forum search
    """
    template_name = 'forum/search_result.html'

    def get_context_data(self, **kwargs):
        text = self.request.GET.get('text', '')
        kwargs.update(forum_search(text))
        return super().get_context_data(**kwargs)

