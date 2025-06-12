from django.db import migrations
from django.utils.text import slugify

def create_test_posts(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    User = apps.get_model('auth', 'User')
    
    # 获取或创建测试用户
    test_user = User.objects.filter(username='testuser').first()
    if not test_user:
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )

    # 创建测试文章
    test_posts = [
        {
            'title': 'Post 3',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sed imperdiet justo.',
            'status': 1
        },
        {
            'title': 'Post 4',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sed imperdiet justo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Pellentesque in faucibus q',
            'status': 1
        }
    ]

    for post_data in test_posts:
        slug = slugify(post_data['title'])
        Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'slug': slug,
                'author': test_user,
                'content': post_data['content'],
                'status': post_data['status']
            }
        )

def remove_test_posts(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Post.objects.filter(title__in=['Post 3', 'Post 4']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_posts, remove_test_posts),
    ] 