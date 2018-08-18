from django.conf.urls import url
from django.urls import path

from .views import KeyWordSearch, ButtonSearch, ButtonPensionSearch

urlpatterns = [
    path('keyword_search/', KeyWordSearch.as_view()),
    path('button_search/', ButtonPensionSearch.as_view()),
    # path('button_search/', ButtonSearch.as_view()),

]