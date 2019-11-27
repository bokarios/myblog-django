from django.urls import path, include
from .views import about, userComment, userLike, userDislike, search, SearchView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/comment/', userComment, name='user-comment'),
    path('user/like/', userLike, name='user-like'),
    path('user/dislike/', userDislike, name='user-dislike'),
    path('search/', SearchView.as_view(), name='search'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('article/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', about, name="blog-about"),
    path('article/<int:pk>-<str:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('article/<int:pk>-<str:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('article/<int:pk>-<str:slug>/', PostDetailView.as_view(), name='post-detail'),
]
