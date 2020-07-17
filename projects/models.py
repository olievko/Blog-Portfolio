from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from taggit.managers import TaggableManager
import time


class PersonalInfo(models.Model):
    TITLE_CHOICES = (
        ('Dr', 'Doctor'),
        ('PhD', 'Doctor of Philosophy'),
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    title = models.CharField(
        max_length=50,
        default=False,
        choices=TITLE_CHOICES, blank=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True)
    overview = models.TextField(blank=True)
    locality = models.CharField(
        max_length=255,
        help_text="e.g., city such as Kyiv",
        blank=True)
    country = models.CharField(
        max_length=64,
        help_text="e.g., Ukraine",
        blank=True)
    years_experience = models.IntegerField(
        default=False,
        blank=True)
    partners = models.IntegerField(
        default=False,
        blank=True)
    completed_projects = models.IntegerField(
        default=False,
        blank=True)
    clients = models.IntegerField(
        default=False,
        help_text="e.g., amount of clients",
        blank=True)
    email = models.EmailField(blank=True)
    phone =models.IntegerField(
        default=False,
        blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    skype = models.CharField(
        max_length=255,
        help_text="skype: user_name",
        blank=True)
    linkedin = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    resume_file = models.FileField(
        upload_to='resume/%Y/%m/%d/',
        blank=True)
    meta_keywords = models.CharField(
        "Meta Keywords",
        max_length=255,
        null=True,
        blank=True,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.TextField(
        "Meta Description",
        max_length=255,
        null=True,
        blank=True,
        help_text='Content for description meta tag, maximum are 200 characters')

    class Meta:
        verbose_name_plural = "Personal Info"

    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    def __str__(self):
        return self.full_name()


class Education(models.Model):
    DEGREE_CHOICES = (
        ('Ph.D.', 'Doctor of Philosophy'),
        ('M.Sc.', 'Masters'),
        ('B.Sc.', 'Bachelor'),
        ('12th', 'High School')
    )
    school_name = models.CharField(
        max_length=250,
        help_text="e.g., Tbilisi State University")
    institute_or_faculty = models.CharField(
        max_length=250,
        help_text="e.g., Institute of Economics",
        blank=True)
    department = models.CharField(
        max_length=250,
        help_text="e.g., Department of Economics",
        blank=True)
    degree = models.CharField(
        max_length=50,
        choices=DEGREE_CHOICES)
    qualification = models.CharField(
        max_length=250,
        help_text="e.g., Economist")
    location = models.CharField(
        max_length=250,
        help_text="e.g., Kyiv, Ukraine",
        blank=True)
    school_url = models.URLField(
        'School URL',
        blank=True)
    start_date = models.DateField()
    completion_date = models.DateField()
    summary = models.TextField(
        blank=True,
        help_text="e.g., Diploma with honors")
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-completion_date']
        verbose_name_plural = "Education"

    def edu_date_range(self):
        return ''.join(['(', self.formatted_start_date(),
                        '-', self.formatted_end_date(), ')'])

    def full_start_date(self):
        return self.start_date.strftime("%Y-%m-%d")

    def full_end_date(self):
        if (self.is_current == True):
            return time.strftime("%Y-%m-%d", time.localtime())
        else:
            return self.completion_date.strftime("%Y-%m-%d")

    def formatted_start_date(self):
        return self.start_date.strftime("%b %Y")

    def formatted_end_date(self):
        if (self.is_current == True):
            return "Current"
        else:
            return self.completion_date.strftime("%b %Y")

    def __str__(self):
        return ' '.join([self.school_name, self.edu_date_range()])


def job_image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "job/{0}/{1}".format(instance.slug, filename)


class Job(models.Model):
    company = models.CharField(
        max_length=250)
    slug = models.SlugField(
        max_length=250,
        db_index=True,
        blank=True)
    image = models.ImageField(
        upload_to=job_image_folder,
        blank=True)
    location = models.CharField(
        max_length=250,
        help_text="e.g., Kyiv, Ukraine",
        blank=True)
    title = models.CharField(
        max_length=250)
    company_url = models.URLField(
        'Company URL',
        blank=True)
    description = models.TextField()
    start_date = models.DateField()
    completion_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-completion_date', '-start_date']

    def job_date_range(self):
        return ''.join(['(', self.formatted_start_date(), '-',
                        self.formatted_end_date(), ')'])

    def full_start_date(self):
        return self.start_date.strftime("%Y-%m-%d")

    def full_end_date(self):
        if (self.is_current == True):
            return time.strftime("%Y-%m-%d", time.localtime())
        else:
            return self.completion_date.strftime("%Y-%m-%d")

    def formatted_start_date(self):
        return self.start_date.strftime("%b %Y")

    def formatted_end_date(self):
        if (self.is_current == True):
            return "Current"
        else:
            return self.completion_date.strftime("%b %Y")

    def __str__(self):
        return ' '.join([self.company, self.job_date_range()])

    def get_absolute_url(self):
        return reverse('profile_detail',
                       kwargs={'job_slug': self.slug})


class ActiveCategoryManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCategoryManager, self).get_query_set().filter(is_active=True)


class ProjectCategory(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique=True,
        help_text='Unique value for product page URL, created automatically from name.')
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        max_length=250,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag',
        blank=True)
    meta_description = models.CharField(
        max_length=250,
        help_text='Content for description meta tag',
        blank=True)
    objects = models.Manager()
    active = ActiveCategoryManager()

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_list_by_category',
                       args=[self.slug])


class Skillset(models.Model):
    name = models.CharField(
        max_length=250,
        blank=True)
    slug = models.SlugField(
        max_length=250,
        blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'ProjectCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    meta_keywords = models.CharField(
        max_length=250,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag',
        blank=True)
    meta_description = models.CharField(
        max_length=250,
        help_text='Content for description meta tag',
        blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(
        max_length=250,
        help_text="e.g., C++, Python")
    slug = models.SlugField(
        max_length=250)
    level = models.IntegerField(
        default=False,
        help_text="Indicate your level skill in percentage")
    is_active = models.BooleanField(default=True)
    skillset = models.ForeignKey(
        'Skillset',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    meta_keywords = models.CharField(
        max_length=250,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag',
        blank=True)
    meta_description = models.CharField(
        max_length=250,
        help_text='Content for description meta tag',
        blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return ''.join([self.skillset.name, '-', self.name])


class LangSkill(models.Model):
    name = models.CharField(
        max_length=250,
        help_text="Ukrainian, English")
    slug = models.SlugField(
        max_length=250)
    level = models.IntegerField(
        default=False,
        help_text="Indicate your level skill in percentage")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


def project_image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "project/{0}/{1}".format(instance.slug, filename)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True)
    image = models.ImageField(
        upload_to=project_image_folder,
        blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(850, 550)],
        format='JPEG',
        options={'quality': 90})
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(600, 600)],
        format='JPEG',
        options={'quality': 90})
    project_url = models.URLField(
        'Project URL',
        null=True,
        blank=True)
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=255)
    report_file = models.FileField(
        upload_to='report/%Y/%m/%d/',
        null=True,
        blank=True)
    meta_keywords = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Content for description meta tag, maximum are 200 characters')
    publish = models.DateTimeField(default=timezone.now)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        'ProjectCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    object = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-added',)
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail',
                       args=[self.pk, self.slug])


class Images(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.ImageField(
        upload_to=project_image_folder,
        blank=True)
    caption = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=70,
        null=True)
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('images_detail', args=[self.id, self.slug])


class Price(models.Model):
    TYPE_CHOICES = (
        ('Simple', 'Simple'),
        ('Middle', 'Middle'),
        ('Complex', 'Complex'))

    SUPPORT_CHOICES = (
        ('Mail Support', 'Mail Support'),
        ('Endless Support', 'Endless Support'))
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='Simple')
    support = models.CharField(
        max_length=250,
        blank=True,
        choices=SUPPORT_CHOICES,
        default='Mail Support')
    name = models.CharField(
        max_length=250,
        help_text="Project name")
    instrument = models.CharField(
        max_length=250,
        default="Django")
    description = models.TextField(
        blank=True,
        help_text="Portfolio, Blog, Ecommerce,...")
    time_delivery = models.IntegerField(
        null=True,
        blank=True)
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'ProjectCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    meta_keywords = models.CharField(
        max_length=250,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag',
        blank=True)
    meta_description = models.CharField(
        max_length=250,
        help_text='Content for description meta tag',
        blank=True)

    class Meta:
        ordering = ['price']
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

    def __str__(self):
        return self.name


def blog_image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "blog/{0}/{1}".format(instance.slug, filename)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    body = models.TextField()

    image = models.ImageField(
        upload_to=blog_image_folder,
        blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(50, 50)],
        format='JPEG',
        options={'quality': 90})
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 90})
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    meta_keywords = models.CharField(
        max_length=250,
        help_text='Comma-delimited set of SEO keywords for keywords meta tag',
        blank=True)
    meta_description = models.CharField(
        max_length=250,
        help_text='Content for description meta tag',
        blank=True)
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


class PostImages(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.ImageField(
        upload_to=blog_image_folder,
        blank=True)
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90})
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 90})
    caption = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=70,
        null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Post Image'
        verbose_name_plural = 'Post Images'

    def __str__(self):
        return self.caption


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True