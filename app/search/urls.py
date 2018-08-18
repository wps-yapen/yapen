from django.conf.urls import url
from django.urls import path

from .views import KeyWordSearch, ButtonSearch

urlpatterns = [
    path('keyword_search/', KeyWordSearch.as_view()),
    path('button_search/', ButtonSearch.as_view()),

]