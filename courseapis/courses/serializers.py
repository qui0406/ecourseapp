from courses.models import Category, Course, Tag, Lesson
from rest_framework import serializers # type: ignore

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    def get_image(self, course):
        if course.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % course.image.name)
            return '/static/%s' % course.image.name
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'