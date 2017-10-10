from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(View):
    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post, status='published',
                                 publish__year=year, publish__month=month, publish__day=day)
        return render(request, 'blog/post/detail.html', {'post': post})
