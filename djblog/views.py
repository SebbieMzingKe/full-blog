from django.shortcuts import get_object_or_404 ,render
from .models import Post
from django.http import  Http404


# Create your views here.


def post_list(request): # list all poosts
    posts = Post.published.all()
    return render(
        request,
        '/home/sebbie/Desktop/projects/full-blog/djblog/post/list.html',
        {'posts':posts}
    )

# return a single post
def post_detail(request, id):
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found")

    post = get_object_or_404(
        Post,
        id = id,
        status = Post.Status.PUBLISHED
    )

    return render(
        request,
        '/home/sebbie/Desktop/projects/full-blog/djblog/templates/post/detail.html',
        {'post':post}
    )