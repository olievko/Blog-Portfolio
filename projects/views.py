from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.requests import RequestSite
from .models import PersonalInfo, Education, Job, Skillset, Skill, LangSkill, Category, Project, Price, Post, Comment
from django.http import HttpResponse
# from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from taggit.models import Tag
from .forms import ContactForm, EmailPostForm, CommentForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def project_list(request, category_slug=None):
    template = "project/project_index.html"
    site_name = RequestSite(request).domain
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)
    prices = Price.objects.filter(is_active=True)
    common_tags = Post.tags.most_common()[:4]
    category = None
    categories = Category.objects.filter(is_active=True)
    object_list = Project.published.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category)
        skill_sets = skill_sets.filter(category=category)
        prices = prices.filter(category=category)
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_email = form.cleaned_data['contact_email']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['oleksii.v.ievtushenko@gmail.com']
            if cc_myself:
                recipients.append(contact_email)
            try:
                send_mail(subject,
                          message,
                          contact_email,
                          recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
        return redirect('message_sent')
    else:
        form = ContactForm()
    context = {
        'site_name': site_name,
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'category': category,
        'categories': categories,
        'projects': projects,
        'prices': prices,
        'common_tags': common_tags,
        'form': form,
    }
    return render(request, template, context)


def project_detail(request, pk, slug, category_slug=None):
    template = 'project/project_detail.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.all()
    skills = Skill.objects.all()
    language_skills = LangSkill.objects.filter(is_active=True)
    prices = Price.objects.filter(is_active=True)
    common_tags = Post.tags.most_common()[:4]
    projects = Project.published.all()
    category = None
    categories = Category.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        projects = projects.filter(category=category)
        skill_sets = skill_sets.filter(category=category)
        prices = prices.filter(category=category)
    project = get_object_or_404(Project, pk=pk, slug=slug)
    meta_keywords = project.meta_keywords
    meta_description = project.meta_description
    images = project.images.all()
    if request.method == 'POST' and 'send' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_email = form.cleaned_data['contact_email']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['oleksii.v.ievtushenko@gmail.com']
            if cc_myself:
                recipients.append(contact_email)
            try:
                send_mail(subject,
                          message,
                          contact_email,
                          recipients)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
        return redirect('message_sent')
    else:
        form = ContactForm()
    context = {
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'category': category,
        'categories': categories,
        'projects': projects,
        'project': project,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'prices': prices,
        'common_tags': common_tags,
        'images': images,
        'form': form,
    }
    return render(request, template, context)


def message_sent(request):
    template = "includes/message_success.html"
    personal_info = PersonalInfo.objects.all()
    skills = Skill.objects.all()
    projects = Project.published.all()
    message_success = 'message_success'
    context = {
        'personal_info': personal_info,
        'skills': skills,
        'projects': projects,
        'message_success': message_success,
    }
    return render(request, template, context)


def post_list(request, tag_slug=None):
    template = 'blog/post/list.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)
    common_tags = Post.tags.most_common()[:4]
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'page': page,
        'posts': posts,
        'tag': tag,
        'common_tags': common_tags,
    }
    return render(request, template, context)


@login_required
def post_detail(request, year, month, day, post):
    template = 'blog/post/detail.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)
    common_tags = Post.tags.most_common()[:4]
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    images = post.images.all()
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'common_tags': common_tags,
        'post': post,
        'images': images,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(request, template, context)


def post_share(request, post_id):
    template = 'blog/post/share.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'oleksii.v.ievtushenko@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, template, context)


def post_search(request):
    template = 'blog/post/search.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
    context = {
        'personal_info': personal_info,
        'job_list': job_list,
        'education': education,
        'skills': skills,
        'skill_sets': skill_sets,
        'language_skills': language_skills,
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, template, context)