from courses.models import Category, Course, Tag, Lesson, User
from rest_framework import serializers # type: ignore

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BaseSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    # def get_image(self, course):
    #     if course.image:
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri('/static/%s' % course.image.name)
    #         return '/static/%s' % course.image.name
    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)
        if instance.image:
            image_url = '/static/%s' % instance.image.name
            if request:
                data['image'] = request.build_absolute_uri(image_url)
        return data

    

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
        fields = ['id', 'subject', 'image', 'tags']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        data= validated_data.copy()
        user = User(**data)
        user.set_password(data.get('password'))
        user.save()
        return user
    