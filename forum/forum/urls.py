from django.urls import path

from . import views


urlpatterns = [
    path('', views.SectionListView.as_view(), name="index"),
    path('section/<int:pk>', views.SectionDetailView.as_view(), name="section_details"),
    path('thread/<int:pk>', views.ThreadDetailView.as_view(), name="thread_details"),
    path('section_create/', views.SectionCreateView.as_view(), name='section_create')
]