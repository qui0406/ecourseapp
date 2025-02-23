from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse

from courses.models import Category, Course, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget # type: ignore
from django.urls import path
# type: ignore

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

class MyCourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'category', 'created_at']
    list_filter = ['id', 'created_at']
    search_fields = ['subject']
    list_editable = ['subject']
    readonly_fields= ['image_view']

    def image_view(self, course):
        return mark_safe(f'<img src="/static/{course.image.name}" alt="Hinh anh" width="100" height="100" />')


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }
        

class CourseAdminSite(admin.AdminSite):
    site_header = 'OU eCourse App'

    def get_urls(self):
        return [path('cate-stats/', self.cate_stats_view)] + super().get_urls()

    def cate_stats_view(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')).values('id', 'name', 'course_count')

        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = CourseAdminSite(name='ecourseapp')

admin_site.register(Course, MyCourseAdmin)
admin_site.register(Category)
admin_site.register(Lesson, LessonAdmin)
