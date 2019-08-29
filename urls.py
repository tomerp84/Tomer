from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/?$', views.Netwrok.as_view()),
    url(r'^connect/', views.Connect.as_view()),
    url(r'^report/', views.Report.as_view()),
    ]

