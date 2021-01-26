from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.SectionListView.as_view(),
        name="index"
    ),
    path(
        'section/<int:pk>/',
        views.SectionDetailView.as_view(),
        name="section_details"
    ),
    path(
        'section/<int:section_pk>/thread/<int:pk>/',
        views.ThreadDetailView.as_view(),
        name="thread_details"
    ),
    path(
        'section/<int:section_pk>/thread/<int:thread_pk>/create_reply/<int:post_pk>/',
        views.PostReplyCreateView.as_view(),
        name="postreply_create"
    ),
    path(
        'section/<int:section_pk>/thread_create/',
        views.ThreadCreateView.as_view(),
        name="thread_create"
    ),
    path(
        'section_create/',
        views.SectionCreateView.as_view(),
        name='section_create'
    ),
    path(
        'section/<int:section_pk>/thread_update/<int:pk>/',
        views.ThreadUpdateView.as_view(),
        name='thread_update'
    ),
    path(
        'search/',
        views.SearchResultsView.as_view(),
        name='search'
    ),
]