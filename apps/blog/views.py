from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post, Comment
from BlogbyDjango.settings import EMAIL_FROM


# Create your views here.

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


class PostDetailView(View):
    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post, status='published',
                                 publish__year=year, publish__month=month, publish__day=day)
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        new_comment = None

        # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

        return render(request, 'blog/post/detail.html',
                      {'post': post, 'comments': comments, 'comment_form': comment_form, 'new_comment': new_comment,
                       'similar_posts': similar_posts})

    def post(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post, status='published',
                                 publish__year=year, publish__month=month, publish__day=day)
        comment_form = CommentForm(request.POST)
        new_comment = None
        comments = post.comments.filter(active=True)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return render(request, 'blog/post/detail.html',
                          {'post': post, 'comments': comments, 'comment_form': comment_form,
                           'new_comment': new_comment, })
        else:
            return render(request, 'blog/post/detail.html',
                          {'post': post, 'comments': comments, 'comment_form': comment_form,
                           'new_comment': new_comment, })


class PostShareView(View):
    def get(self, request, post_id):
        form = EmailPostForm()
        post = get_object_or_404(Post, id=post_id, status='published')
        return render(request, 'blog/post/share.html', {"form": form, 'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status='published')
        sent = False
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = '{} ({}) recommend you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'],
                                                                    cd['comments'])
            send_mail(subject, message, EMAIL_FROM, [cd['to']])
            sent = True

            return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

        else:
            return render(request, 'blog/post/share.html', {"form": form, 'sent': sent})


# 搜索引擎视图
def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
            return render(request, 'blog/post/search.html', {'form': form,
                                                             'cd': cd,
                                                             'results': results,
                                                             'total_results': total_results})
    else:
        return render(request, 'blog/post/search.html', {'form': form})
