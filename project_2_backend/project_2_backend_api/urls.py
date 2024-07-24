from django.urls import path
from . import views
urlpatterns = [
    path('objects/<int:pk>', views.ObjectView.as_view(), name='object_detail'),
    path('objects', views.ObjectListView.as_view(), name='object_list')
]
