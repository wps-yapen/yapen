from django.conf.urls import url
from django.urls import path

from .views import KeyWordButtonSearch

urlpatterns = [
    path('keyword_search/', KeyWordButtonSearch.as_view()),

]