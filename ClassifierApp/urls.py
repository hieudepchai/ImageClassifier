from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('collect_image', views.collect_image, name='collect_image')
]