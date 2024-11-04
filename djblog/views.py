from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from taggit.models import Tag


from .models import Post
from .forms import EmailPostForm, CommentForm

# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_list(request, tag_slug = None): # display all posts
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        post_list = post_list.filter(tags__in = [tag])


    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'post/list.html',
        {
            'posts':posts,
            'tag': tag
        }
    )

def post_detail(request, year, month, day, post): # display a single post
    # try:
    #     post = Post.published.get(id = id)
    # except Post.DoesNotExist:
    #     raise Http404("No post found")
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = post,
        publish__year=year,
        publish__month=month,
        publish__day=day,

    )

    # list active comments for this/a post
    comments = post.comments.filter(active = True)

    # form for users to comment
    form = CommentForm()

    # list of similar posts
    post_tags_ids = post.tags.values_list('id', flat = True)
    similar_posts = Post.published.filter(
        tags__in = post_tags_ids
    ).exclude(id = post.id)
    similar_posts = similar_posts.annotate(
        same_tags = Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return render(
        request,
        'post/detail.html',
        {
            'post':post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
         }
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
            try:
                send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
                )
            except BadHeaderError:  
                return HttpResponse('Invalid header found.')  
            except Exception as e:
                return HttpResponse(f'Error sending email: {str(e)}')
            
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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )

    comment = False

    form = CommentForm(data = request.POST)
    if form.is_valid():
        # create comment object without saving it to the database
        comment = form.save(commit = False)
        # assign the post to the comment
        comment.post = post
        # save comment to the database
        comment.save()

        return render(
            request,
            'post/comment.html',
            {
                'post': post,
                'form': form,
                'comment': comment
            }
        )