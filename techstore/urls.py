from django.contrib import admin
from django.urls import path, include
urlpatterns=[path('admin-django/',admin.site.urls), path('',include('loja.urls'))]
