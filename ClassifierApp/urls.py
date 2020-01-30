from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('collect_image', views.collect_image, name='collect_image'),
    path('clear_session', views.clear_session, name='clear_session'),
    path('display_image', views.display_image, name='display_image')
]