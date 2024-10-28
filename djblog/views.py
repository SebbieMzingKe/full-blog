from django.shortcuts import get_object_or_404 ,render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.http import  Http404


# Create your views here.


def post_list(request): # list all poosts
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3) # paginator with 3 posts per page
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1) # if page number is out of range return to page 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # if last page is out of range
    return render(
        request,
        'post/list.html',
        {'posts':posts}
    )

# return a single post
def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found")

    post = get_object_or_404(
        Post,
        # id = id,
        status = Post.Status.PUBLISHED,
        slug = post,
        publish__year = year,
        publish__month = month,
        publish__day = day

    )

    return render(
        request,
        'post/detail.html',
        {'post':post}
    )