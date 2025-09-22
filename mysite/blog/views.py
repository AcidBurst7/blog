from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.db.models import Count

from decouple import config
from taggit.models import Tag

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


def post_list(request, tag_slug=None):
    posts_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tags__in=[tag])

    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts, 'tag': tag}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]


    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post, 
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    post = get_object_or_404(
        Post, 
        id=post_id, 
        status=Post.Status.PUBLISHED
    )

    recipient = ""
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} рекомендует к прочтению"
               f"{post.title}" 
            )
            message = (
                f"Прочесть {post.title} at {post_url}\n\n"
                f"{cd['name']}\ прокомментировал: {cd['comments']}"
            )
            recipient = [cd['to']]
            send_mail(subject, message, config('EMAIL_HOST_USER'), recipient)
            sent = True
        else:
            print(form.errors)
    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post, 
            'form': form, 
            'sent': sent,
            'recipient': recipient
        }
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )
