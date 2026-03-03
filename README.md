# 介绍
这是一个收藏夹项目，以便 hjki156 便利的在任何地方访问网站、下载连接、磁力、图片、文字
（其实是给赴尘杯写的题库）

# 功能

- [x] 基础 crud based on SQLAlchemy ORM
> 再也不用 PHP 风格了

- [ ] 带鉴权的上传接口
> 不用担心被偷家了

- [ ] 前端示例页面
> 简陋但能跑

# 环境变量

1. 复制示例配置：将 `.env.example` 复制为 `.env`
2. 按需修改以下变量：
	- `SQLALCHEMY_DATABASE_URI`：数据库连接串
	- `SECRET_KEY`：JWT 签名密钥
	- `JWT_EXPIRATION_DAYS`：Token 过期天数

# 容器运行

1. 构建开发镜像（`python main.py`）

```bash
docker build -f dockerfile --target dev -t collation-api:dev .
```

2. 构建生产镜像（`gunicorn`）

```bash
docker build -f dockerfile --target production -t collation-api:prod .
```

3. 启动容器（从 `.env` 注入配置）

```bash
docker run --rm -p 2013:2013 --env-file .env collation-api:prod
```

# Docker Compose

默认按生产模式启动（`production`）：

```bash
docker compose up -d --build
```

切换开发模式（`dev`）后启动：

- PowerShell:

```powershell
$env:APP_TARGET="dev"; docker compose up -d --build
```

- Bash:

```bash
APP_TARGET=dev docker compose up -d --build
```

停止并清理：

```bash
docker compose down
```
