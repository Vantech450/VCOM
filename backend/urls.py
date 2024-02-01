from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('Vatrent/', admin.site.urls),
    path('', include('base.urls')),
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
