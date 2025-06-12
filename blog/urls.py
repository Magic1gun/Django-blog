from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)

app_name = 'blog'

urlpatterns = [
    # 重定向和Cookie相关的URL
    path('redirect/', views.example_for_redirect, name='redirect_example'),
    path('inf1/', views.inf1, name='inf1'),
    path('inf2/', views.inf2, name='inf2'),
    path('setcookie/', views.setcookie, name='setcookie'),
    path('readcookie/', views.readcookie, name='readcookie'),
    path('getcookie/', views.readcookie, name='getcookie'),
    path('deletecookie/', views.deletecookie, name='deletecookie'),
    
    # Cookie和Session相关的URL
    path('testcookie/', views.cookie_session, name='cookie_session'),
    path('create/', views.create_session, name='create_session'),
    path('access/', views.access_session, name='access_session'),
    path('delete/', views.delete_session, name='delete_session'),
    
    # 缓存相关的URL
    path('cache/view/', views.cached_view, name='cached_view'),
    path('cache/api/', views.cache_api_view, name='cache_api'),
    path('cache/delete/', views.delete_cached_data, name='delete_cache'),
    path('cache/counter/', views.cache_counter, name='cache_counter'),
    path('cache/reset/', views.reset_counter, name='reset_counter'),
    path('cache/template/', views.template_cache_view, name='template_cache'),
    
    # 其他URL
    path('', views.PostList.as_view(), name='home'),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('delete-account/', views.delete_account, name="delete_account"),
    path('api/posts/', views.PostViewSet.as_view({'get': 'list'}), name='post-list'),
    path('api/posts/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve'}), name='post-detail'),
    
    # 通配符URL放在最后
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]