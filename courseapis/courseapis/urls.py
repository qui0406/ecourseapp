from django.contrib import admin
from django.urls import path, include, re_path
from courses.admin import admin_site
from debug_toolbar.toolbar import debug_toolbar_urls # type: ignore

from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

from django.contrib import admin
from django.urls import path
from courses.swagger import schema_view # type: ignore


urlpatterns = [
    path('', include('courses.urls')),
    path('admin/', admin_site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('swagger/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
] + debug_toolbar_urls()
