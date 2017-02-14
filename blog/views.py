from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
import os.path
from django.conf import settings
# Create your views here.
def generate_upload_path(instance, filename):
    return os.path.join(settings.STATIC_ROOT, 'blog/img/')



def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject ='{} ({}) recommends you reading "{}" '.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'saman.esmailpour@gmail.com',[cd['to']])
            sent = True
    else:
        form= EmailPostForm()

    return render(request, 'blog/post/share.html',{'post':post,'form':form,
                                                    'sent': sent})



def post_list(request,tag_slug=None):
    objects_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objects_list = objects_list.filter(tags__in =[tag])
    paginator = Paginator(objects_list, 5) # Show 25 posts per page
    page = request.GET.get('page') # geting curent page
    try:
        posts = paginator.page(page) # a page object that have a 5 post!
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts':posts,
                                                    'page':page,
                                                    'tag':tag})#<! This is the method you can use to reuse your pagination template in paginated views of different models.

#class PostListView(ListView):
    #queryset = Post.published.all()
    #context_object_name = 'posts'
    #paginate_by = 2
    #template_name ='blog/post/list.html'


def post_detail(request,year, month, day,post):
    post = get_object_or_404(Post, slug=post,
                                    status='published',
                                    publish__year = year,
                                    publish__month = month,
                                    publish__day= day )

    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data= request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id',flat= True)
    similar_posts = Post.published.filter(tags__in = post_tags_ids).exclude(id= post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags',"-publish")[:4]


    return render(request, 'blog/post/detail.html', {'post':post,
                                                    'comments': comments,
                                                    'comment_form':comment_form,
                                                    'similar_posts':similar_posts})
