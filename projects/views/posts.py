from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import PersonalInfo, Education, Job, Skillset, Skill, LangSkill, Post, Comment
from django.http import HttpResponseRedirect
# from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from projects.forms import EmailPostForm, CommentForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request, tag_slug=None):
    template = 'blog/post/list.html'
    personal_info = PersonalInfo.objects.all()
    education = Education.objects.all()
    job_list = Job.objects.all()
    skill_sets = Skillset.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    language_skills = LangSkill.objects.filter(is_active=True)

    object_list = Post.published.all()
    common_tags = Post.tags.most_common()[:4]
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    form = SearchForm()
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            object_list = Post.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )

    paginator = Paginator(object_list, 3)
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
        'form': form,
        'query': query,
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

    initial_data = {
        "content_type": post.get_content_type,
        "object_id": post.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        content_type = post.get_content_type
        obj_id = post.id
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = post.comments

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

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
        'comment_form': form,
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
    common_tags = Post.tags.most_common()[:4]
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
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
        'common_tags': common_tags,
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, template, context)


# class PostsSearch(ListView):
#     model = Post
#     context_object_name = 'posts'
#     template_name = 'blog/post/list.html'
#     paginate_by = 3
#
#     def get_queryset(self):
#         query = self.request.GET.get("q")
#         return Post.published.filter(
#             Q(title__icontains=query) | Q(body__icontains=query)
#         )
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context["q"] = f'q={self.request.GET.get("q")}&'
#         context["personal_info"] = PersonalInfo.objects.all()
#         context["education"] = Education.objects.all()
#         context["job_list"] = Job.objects.all()
#         context["skill_sets"] = Skillset.objects.filter(is_active=True)
#         context["skills"] = Skill.objects.filter(is_active=True)
#         context["language_skills"] = LangSkill.objects.filter(is_active=True)
#         context["common_tags"] = Post.tags.most_common()[:4]
#         return context
