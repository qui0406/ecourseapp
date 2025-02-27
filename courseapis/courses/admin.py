from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Count
from .models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget # type: ignore
from django import forms
from django.urls import path
from courses import dao

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'OU eCourse App'

    def get_urls(self):
        return [path('cate-stats/', self.cate_stats_view)] + super().get_urls()
    
    def cate_stats_view(self, request):
        # stats = Category.objects.annotate(course_count=Count('courses__id')).values('id', 'name', 'course_count')

        return TemplateResponse(request, 'admin/stats.html', {
            'stats': dao.count_course_by_cate()
        })


admin_site = CourseAppAdminSite(name='myapp')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ['name']
    list_filter = ['id', 'name']


class CourseForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Course
        fields = '__all__'


class TagInlineAdmin(admin.StackedInline):
    model = Course.tags.through


class CourseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'subject', 'created_date', 'updated_date', 'category', 'active']
    readonly_fields = ['img']
    inlines = [TagInlineAdmin]
    form = CourseForm

    def img(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />'.format(url=course.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }


admin_site.register(Category, CategoryAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson)
admin_site.register(Tag)