import requests
import json

# API 基础 URL
BASE_URL = 'http://127.0.0.1:8000/api/v1'

# 替换为您的 token
TOKEN = 'b411ef3b3f0857dbd11bdef282702c04425141ee'

def test_get_posts():
    """测试获取所有文章"""
    print("\n1. 获取所有文章:")
    response = requests.get(f'{BASE_URL}/posts/')
    print(f"状态码: {response.status_code}")
    print("文章列表:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_get_single_post(post_id=1):
    """测试获取单个文章"""
    print(f"\n2. 获取文章 ID={post_id}:")
    response = requests.get(f'{BASE_URL}/posts/{post_id}/')
    print(f"状态码: {response.status_code}")
    print("文章详情:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_create_post():
    """测试创建新文章"""
    print("\n3. 创建新文章:")
    new_post = {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "status": 1,
        "author": 1  # 确保这个用户ID存在
    }
    headers = {
        'Authorization': f'Token {TOKEN}'
    }
    response = requests.post(f'{BASE_URL}/posts/', json=new_post, headers=headers)
    print(f"状态码: {response.status_code}")
    print("创建结果:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == '__main__':
    # 运行测试
    test_get_posts()
    test_get_single_post()
    test_create_post() 