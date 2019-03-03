from django.urls import path, include
from .views import post_list, post_detail, PostList, PostaList, PostoList
from . import views
app_name = 'blog'

urlpatterns = [path('posts/', views.PostaList.as_view(), name='blog_post_list'),
               path('post/create', views.PostCreate.as_view(), name='blog_post_create'),
               path('post/<str:year>/<str:month>/<str:slug>', views.PostDetail.as_view(), name='blog_post_detail'),
               path('', PostoList.as_view(), name='blog_post-list'),
               path('post/<int:year>/<int:month>/<str:slug>/update', views.PostUpdate.as_view(), name='blog_post_update'),
               path('post/<int:year>/<int:month>/<str:slug>/delete', views.PostDelete.as_view(), name='blog_post_delete'),
               path('<int:year>', views.PostArchiveView.as_view(), name='blog_post_archive_year'),
               path('<int:year>/<int:month>', views.PostArchiveMonth.as_view(), name='blog_post_archive_month'),
               path('<int:year>/<int:month>/<int:day>/<str:slug>', views.PostaDetail.as_view(),name='blog_posta_detail')]