"""example_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from example_project import views
from admin_templates import admin_views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('admin/templates/', admin_views.templates_list, name='admin-template-list'),
    path('admin/templates/<key>/', admin_views.template_view, name='admin-template-detail'),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
