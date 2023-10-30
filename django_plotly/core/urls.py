from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.chart, name='chart'),
    path("", views.use_template, name="usetemplate"),
    path("update_chart/", views.update_chart, name='update_chart')
] 
