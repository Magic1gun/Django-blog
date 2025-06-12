# Django 博客项目

## 项目简介
本项目是一个基于 Django 框架的博客系统，支持 RESTful API，适合学习和二次开发。

## 环境要求
- Python 3.9 及以上
- pip
- （可选）Docker 及 Docker Compose
- Windows 10 19044 或更高版本（如需使用 Docker Desktop）

## 安装与运行

### 1. 克隆项目
```bash
# 克隆代码仓库
# git clone <your-repo-url>
cd <项目目录>
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 数据库迁移
```bash
python manage.py migrate
```

### 4. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 5. 启动开发服务器
```bash
python manage.py runserver
```

访问：http://127.0.0.1:8000/

---

## 使用 Docker 部署

### 1. 构建镜像
```bash
docker build -t mysite .
```

### 2. 运行容器
```bash
docker run -p 8000:8000 mysite
```

---

## 目录结构说明
```
mysite/           # 项目主目录
├── blog/         # 博客应用
├── mysite/       # 配置目录
├── static/       # 静态文件
├── templates/    # 模板文件
├── manage.py     # 管理脚本
├── requirements.txt # 依赖文件
├── Dockerfile    # Docker 配置
├── .dockerignore # Docker 忽略文件
└── README.md     # 项目说明
```

---

## 常用命令
- 迁移数据库：`python manage.py migrate`
- 创建超级用户：`python manage.py createsuperuser`
- 启动开发服务器：`python manage.py runserver`

---

## 其他说明
- 默认数据库为 SQLite（db.sqlite3），如需生产环境建议更换为 MySQL/PostgreSQL。
- 静态文件和媒体文件未做特殊配置，生产环境请使用专业存储方案。
- 如需 API 文档或前端对接，请参考 `blog` 应用下的接口实现。

---

## 联系方式
如有问题或建议，请提交 issue 或联系开发者。 