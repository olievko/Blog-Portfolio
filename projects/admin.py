# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Images, Project, Category, PersonalInfo, Job, Education, Skillset, Skill, LangSkill, Price, PostImages, Post, Comment

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PersonalInfoAdminForm(forms.ModelForm):
    overview = forms.CharField(label="Overview", widget=CKEditorUploadingWidget())

    class Meta:
        model = PersonalInfo
        fields = '__all__'


class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(label="Description", widget=CKEditorUploadingWidget())

    class Meta:
        model = Project
        fields = '__all__'


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(label="Body", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    form = PersonalInfoAdminForm


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(Skillset)
class SkillsetAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(LangSkill)
class LangSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', )
    list_display_links = ('name',)
    ordering = ['name']
    search_fields = ['name', 'meta_keywords', 'meta_description']
    prepopulated_fields = {'slug': ('name',)}


class ImagesInline(admin.TabularInline):
    list_display = ('caption', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('caption',)}
    model = Images
    exta = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('status', 'added', 'publish')
    search_fields = ('title', 'technology', 'meta_keywords', 'meta_description')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [ImagesInline, ]
    form = ProjectAdminForm


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('type', 'category', 'price', 'is_active')


class PostImagesInline(admin.TabularInline):
    list_display = ('caption', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('caption',)}
    model = PostImages
    exta = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [PostImagesInline, ]
    form = PostAdminForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')