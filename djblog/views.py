from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from .models import Post
from .forms import EmailPostForm, CommentForm
from django.http import  Http404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.core.mail import send_mail, BadHeaderError


# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


def post_list(request): # display all posts
    posts = Post.published.all()
    
    return render(
        request,
        'post/list.html',
        {'posts':posts}
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


    return render(
        request,
        'post/detail.html',
        {
            'post':post,
            'comments': comments,
            'form': form
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