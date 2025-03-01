from django.urls import path, include
from . import views
from rest_framework import routers # type: ignore

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('lessons', views.LessonViewSet, basename='lessons')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]