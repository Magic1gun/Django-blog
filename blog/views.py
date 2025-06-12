from django.views import generic
from .models import Post, Counter
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .serializers import PostSerializer
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import NewUserForm
from django.db.models import Q, F
import logging
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from datetime import datetime
from django.db import transaction

logger = logging.getLogger(__name__)

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(status=1).order_by('-created_on')
        return context

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        queryset = Post.objects.filter(status=1)
        logger.debug(f"Available posts: {list(queryset.values('title', 'slug', 'status'))}")
        return queryset

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        logger.debug(f"Looking for post with slug: {slug}")
        
        # 尝试直接通过slug查找
        try:
            post = Post.objects.get(slug=slug, status=1)
            logger.debug(f"Found post by slug: {post.title}")
            return post
        except Post.DoesNotExist:
            logger.debug(f"No post found with slug: {slug}")
        
        # 尝试通过标题查找
        try:
            post = Post.objects.get(title=slug, status=1)
            logger.debug(f"Found post by title: {post.title}")
            return post
        except Post.DoesNotExist:
            logger.debug(f"No post found with title: {slug}")
        
        # 如果都找不到，返回404
        logger.error(f"No post found with slug or title: {slug}")
        raise Http404(f"No post found with slug or title: {slug}")

def index(request):
    return render(request, 'index.html')

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "注册成功！")
            return redirect("blog:home")
        messages.error(request, "注册失败。请检查输入信息。")
    form = NewUserForm()
    return render(request=request, template_name="blog/register.html", context={"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"您已成功登录为 {username}。")
                return redirect("blog:home")
            else:
                messages.error(request, "用户名或密码无效。")
        else:
            messages.error(request, "用户名或密码无效。")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "您已成功退出登录。")
    return redirect("blog:home")

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # 先退出登录
        user.delete()    # 删除用户账户
        messages.success(request, "您的账户已成功注销。")
        return redirect('blog:home')
    return render(request, 'blog/delete_account.html')

def cookie_session(request):
    request.session.set_test_cookie()
    return HttpResponse("<h1>Cookie测试</h1>")

def cookie_delete(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        response = HttpResponse("Cookie创建成功")
    else:
        response = HttpResponse("您的浏览器不支持Cookie")
    return response

def create_session(request):
    request.session['name'] = 'username'
    request.session['password'] = 'password123'
    return HttpResponse("<h1>Session已设置</h1>")

def access_session(request):
    response = "<h1>欢迎访问Session</h1><br>"
    if request.session.get('name'):
        response += "用户名: {0} <br>".format(request.session.get('name'))
    if request.session.get('password'):
        response += "密码: {0} <br>".format(request.session.get('password'))
        return HttpResponse(response)
    else:
        return redirect('blog:create_session')

def delete_session(request):
    try:
        del request.session['name']
        del request.session['password']
    except KeyError:
        pass
    return HttpResponse("<h1>Session数据已清除</h1>")

# 重定向示例
def example_for_redirect(request):
    '''重定向请求到首页'''
    return redirect('blog:home')

# Cookies相关视图
def setcookie(request):
    response = HttpResponse("Cookie Created")
    response.set_cookie('dataflair', 'xyzxyzxyzxyz')
    return response

def readcookie(request):
    cookie_value = request.COOKIES.get('dataflair', 'Cookie not found')
    return HttpResponse(f"Cookie value: {cookie_value}")

def deletecookie(request):
    response = HttpResponse("Cookie Deleted")
    response.delete_cookie('dataflair')
    return response

# 无限重定向示例（仅用于演示，实际使用中应避免）
def inf1(request):
    return redirect('/inf2')

def inf2(request):
    return redirect('/inf1')

# 使用装饰器缓存视图
@cache_page(60 * 15)  # 缓存15分钟
def cached_view(request):
    """一个使用缓存的示例视图"""
    return HttpResponse("这个页面被缓存了15分钟")

# 使用缓存API的视图
def cache_api_view(request):
    """演示如何使用缓存API"""
    # 尝试从缓存获取数据
    cached_data = cache.get('my_cached_data')
    
    if cached_data is None:
        # 如果缓存中没有数据，生成新数据
        cached_data = "这是新生成的数据"
        # 将数据存入缓存，设置过期时间为300秒
        cache.set('my_cached_data', cached_data, 300)
    
    return HttpResponse(f"数据: {cached_data}")

# 使用缓存API删除数据
def delete_cached_data(request):
    """删除缓存中的数据"""
    cache.delete('my_cached_data')
    return HttpResponse("缓存数据已删除")

# 使用数据库的计数器示例
def cache_counter(request):
    """演示如何使用数据库实现计数器"""
    try:
        with transaction.atomic():
            counter, created = Counter.objects.select_for_update().get_or_create(
                name='page_views',
                defaults={'value': 0}
            )
            old_value = counter.value
            old_updated_at = counter.updated_at
            logger.debug(f"[计数器] 更新前 value: {old_value}, updated_at: {old_updated_at}")
            counter.value += 1
            counter.save()
            counter.refresh_from_db()
            logger.debug(f"[计数器] 更新后 value: {counter.value}, updated_at: {counter.updated_at}")
            logger.debug(f"[计数器] 创建状态: {created}")
            return HttpResponse(f"""
                <div style="text-align: center; margin-top: 50px;">
                    <h1>页面访问计数器</h1>
                    <div style="font-size: 24px; margin: 20px 0;">
                        当前计数: <span style="color: #007bff;">{counter.value}</span>
                    </div>
                    <div style="color: #666; margin-bottom: 20px;">
                        最后更新时间: {counter.updated_at.strftime('%Y-%m-%d %H:%M:%S')}
                    </div>
                    <a href="/blog/cache/reset/" 
                       style="display: inline-block; 
                              padding: 10px 20px; 
                              background-color: #dc3545; 
                              color: white; 
                              text-decoration: none; 
                              border-radius: 5px;">
                        重置计数器
                    </a>
                </div>
            """)
    except Exception as e:
        logger.error(f"计数器错误: {str(e)}")
        return HttpResponse(f"""
            <div style="text-align: center; margin-top: 50px;">
                <h1 style="color: #dc3545;">计数器暂时不可用</h1>
                <p style="color: #666;">错误信息: {str(e)}</p>
                <p>请稍后再试或联系管理员</p>
            </div>
        """)

def reset_counter(request):
    """重置计数器"""
    try:
        with transaction.atomic():
            counter = Counter.objects.get(name='page_views')
            counter.value = 0
            counter.save()
            messages.success(request, "计数器已重置")
            return redirect('blog:cache_counter')
    except Counter.DoesNotExist:
        messages.warning(request, "计数器不存在")
        return redirect('blog:cache_counter')
    except Exception as e:
        logger.error(f"重置计数器错误: {str(e)}")
        messages.error(request, f"重置计数器失败: {str(e)}")
        return redirect('blog:cache_counter')

# 使用缓存API的模板片段缓存示例
def template_cache_view(request):
    """演示如何在视图中使用模板片段缓存"""
    context = {
        'current_time': datetime.now(),
        'cached_data': cache.get('template_data', '默认数据')
    }
    return render(request, 'blog/cache_example.html', context)