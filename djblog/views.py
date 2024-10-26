from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post

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
    