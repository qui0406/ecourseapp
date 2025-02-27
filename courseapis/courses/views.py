from courses.paginators import CoursePaginator
from rest_framework import viewsets, generics # type: ignore
from courses.models import Category, Course, Lesson
from courses import serializers, paginators
from .serializers import CategorySerializer , CourseSerializer
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore



class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True).all()
    serializer_class = CourseSerializer 
    pagination_class = CoursePaginator

    def get_query(self):
        queries = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(subject__icontains=q)
        return queries

    @action(detail=True, methods=['get'])
    def lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True).all()

        return Response(serializers.LessonSerializer(lessons, many=True, context= {"request": request}).data, status= status.HTTP_200_OK)
