from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.requests import RequestSite
from projects.models import PersonalInfo, Education, Job, Skillset, Skill, LangSkill, ProjectCategory, Project, Price, Post
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from projects.forms import ContactForm
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
    categories = ProjectCategory.objects.filter(is_active=True)
    object_list = Project.published.all()
    if category_slug:
        category = get_object_or_404(ProjectCategory, slug=category_slug)
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
        'page': page,
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
    categories = ProjectCategory.objects.filter(is_active=True)
    if category_slug:
        category = get_object_or_404(ProjectCategory, slug=category_slug)
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
