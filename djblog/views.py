from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post
from .forms import EmailPostForm
from django.http import  Http404
from django.views.generic import ListView
from django.core.mail import send_mail


# Create your views here.

def post_list(request): # display all posts
    posts = Post.published.all()
    
    return render(
        request,
        'djblog/post/list.html',
        {'posts':posts}
    )

def post_detail(request, id): # display a single post
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found")
    post = get_object_or_404(
        Post,
        id = id,
        status = Post.Status.PUBLISHED
    )
    return render(
        request,
        'djblog/post/detail.html',
        {'post':post}
    )

def post_share(request, post_id):
# Retrieve post by id
    post = get_object_or_404(
    Post,
    id=post_id,
    status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
            post.get_absolute_url()
            )
            subject = (
            f"{cd['name']} ({cd['email']}) "
            f"recommends you read {post.title}"
            )
            message = (
            f"Read {post.title} at {post_url}\n\n"
            f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
    request,
    'post/share.html',
    {
    'post': post,
    'form': form,
    'sent': sent
    }
    )
