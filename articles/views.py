from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.urls import resolve
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from hitcount.views import HitCountDetailView
from .models import Post, Comment, Like, Dislike
from django.db.models import Q
from django.core.paginator import Paginator
import json

#-------------------------------------------------------------------------------
#The post list view (url='/')
class PostListView(ListView):
    model = Post
    ordering = ['-created_at']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:3]
        return context

#-------------------------------------------------------------------------------
#The posts of cetain user view (url='/user/<int:pk>/')
class UserPostListView(ListView):
    model = Post
    template_name = 'articles/user_posts.html'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user=user).order_by('-created_at')

#-------------------------------------------------------------------------------
#The post details view (url='/article/<int:pk>/')
class PostDetailView(HitCountDetailView):
    model = Post
    query_pk_and_slug = True
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-hit_count_generic__hits')[:3]
        return context

#-------------------------------------------------------------------------------
#The post create view (url='/article/new/')
class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_message = 'Article created'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = 'd-none invisible'
        context['edit_col'] = 'col-12'
        return context

#-------------------------------------------------------------------------------
#The post update view (url='/article/<int:pk>/update/')
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    query_pk_and_slug = True
    fields = ['title', 'content', 'image']
    success_message = 'Article updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = 'd-none invisible'
        context['edit_col'] = 'col-12'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

#-------------------------------------------------------------------------------
#The post delete view (url='/article/<int:pk>/delete/')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    query_pk_and_slug = True
    success_url = '/'
    success_message = 'Article deleted'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

#-------------------------------------------------------------------------------
#The about view (url='/about/')
def about(request):
    context = {
        "title": "About"
    }
    return render(request, 'articles/about.html', context)

#-------------------------------------------------------------------------------
#The user comment logic (url='/user/commment/' | ajax func)
def userComment(request):
    if request.method == 'POST' and request.is_ajax():
        data = f'''
            <script>
                top.location.href="/article/{request.POST.get('article_id')}"
            </script>
        '''
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')
        comment = Comment()
        comment.article = get_object_or_404(Post, id=article_id)
        comment.user = get_object_or_404(User, id=user_id)
        comment.comment = request.POST.get('comment')
        comment.save()
        messages.success(request, 'Comment posted')
        return HttpResponse(data)
    else:
        data = f'''
            <script>
                top.location.href="/article/{request.POST.get('article_id')}"
            </script>
        '''
        messages.success(request, 'Comment posted')
        return HttpResponse(data)

#-------------------------------------------------------------------------------
#The user like logic (url='/user/like/' | ajax func)
def userLike(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')

        count = Dislike.objects.filter(user=user_id, article=article_id).count()
        if count > 0:
            Dislike.objects.filter(user=user_id, article=article_id).delete()

        count = Like.objects.filter(user=user_id, article=article_id).count()
        if count < 1:
            like = Like()
            like.article = get_object_or_404(Post, id=article_id)
            like.user = get_object_or_404(User, id=user_id)
            like.save()

        data = {'success': '200'}
        print(json.dumps(data))
        return HttpResponse(json.dumps(data))

#-------------------------------------------------------------------------------
#The user dislike logic (url='/user/dislike/' | ajax func)
def userDislike(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        article_id = request.POST.get('article_id')

        count = Like.objects.filter(user=user_id, article=article_id).count()
        if count > 0:
            Like.objects.filter(user=user_id, article=article_id).delete()

        count = Dislike.objects.filter(user=user_id, article=article_id).count()
        if count < 1:
            dislike = Dislike()
            dislike.article = get_object_or_404(Post, id=article_id)
            dislike.user = get_object_or_404(User, id=user_id)
            dislike.save()

        data = {'success': '200'}
        print(json.dumps(data))
        return HttpResponse(json.dumps(data))


#-------------------------------------------------------------------------------
#The search logic (url='/search/?q=query')
def search(request):
    template_name = 'articles/post_list.html'
    if request.method == 'GET':
        query = request.GET.get('q')

        if not query == None:
            look_ups = Q(title__icontains=query) | Q(content__icontains=query)
            qs = Post.objects.filter(look_ups).order_by('-created_at')
        else:
            qs = Post.objects.all().order_by('-created_at')
        context = {
            'object_list': qs,
            'obj_list': qs,
            'content': 'search',
            'query': query
        }

    return render(request, template_name, context)

class SearchView(ListView):
    model = Post
    ordering = ['-created_at']
    paginate_by = 6

    def get_queryset(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('q')
            if not query == None:
                look_ups = Q(title__icontains=query) | Q(content__icontains=query)
                object_list = Post.objects.filter(look_ups).order_by('-created_at')
            else:
                object_list = Post.objects.all().order_by('-created_at')

            return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_list'] = Post.objects.filter(Q(title__icontains=self.request.GET.get('q')) | Q(content__icontains=self.request.GET.get('q')))
        context['content'] = 'search'
        context['query'] = self.request.GET.get('q')
        # context['popular_posts'] = Post.objects.order_by('-updated_at')[:3]
        return context
