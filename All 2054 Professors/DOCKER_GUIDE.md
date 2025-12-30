# Docker 部署指南

## 🐳 使用Docker运行API

### 前置要求

- 安装 Docker Desktop (Windows/Mac) 或 Docker Engine (Linux)
- 下载地址: https://www.docker.com/get-started

---

## 🚀 快速开始

### 方式1: 使用 Docker Compose（推荐）

```bash
# 1. 构建并启动容器
docker-compose up -d

# 2. 查看日志
docker-compose logs -f

# 3. 停止服务
docker-compose down

# 4. 重启服务
docker-compose restart
```

### 方式2: 使用 Docker 命令

```bash
# 1. 构建镜像
docker build -t deanza-api .

# 2. 运行容器
docker run -d \
  --name deanza-api \
  -p 8000:8000 \
  -v $(pwd)/rmp_deanza_all_professors.json:/app/rmp_deanza_all_professors.json \
  -v $(pwd)/logs:/app/logs \
  deanza-api

# 3. 查看日志
docker logs -f deanza-api

# 4. 停止容器
docker stop deanza-api

# 5. 删除容器
docker rm deanza-api
```

---

## 📋 常用命令

### Docker Compose

```bash
# 启动服务（后台运行）
docker-compose up -d

# 启动服务（前台运行，查看日志）
docker-compose up

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 查看日志
docker-compose logs -f api

# 查看服务状态
docker-compose ps

# 重启服务
docker-compose restart

# 重新构建镜像
docker-compose build

# 重新构建并启动
docker-compose up -d --build
```

### Docker 命令

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止）
docker ps -a

# 查看容器日志
docker logs deanza-api
docker logs -f deanza-api  # 实时查看

# 进入容器
docker exec -it deanza-api bash

# 查看容器资源使用
docker stats deanza-api

# 停止容器
docker stop deanza-api

# 启动已停止的容器
docker start deanza-api

# 删除容器
docker rm deanza-api

# 删除镜像
docker rmi deanza-api
```

---

## 🔧 配置说明

### 端口映射

- 容器端口: 8000
- 主机端口: 8000
- 修改: 编辑 `docker-compose.yml` 中的 `8000:8000` 为 `主机端口:8000`

### 数据持久化

以下文件/目录会被挂载到容器中：

- `rmp_deanza_all_professors.json` - 数据文件
- `logs/` - 日志目录
- `static/` - 静态文件目录

### 环境变量

可以在 `docker-compose.yml` 中添加环境变量：

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - API_HOST=0.0.0.0
  - API_PORT=8000
```

---

## 🔄 更新数据

### 方式1: 在容器外更新

```bash
# 1. 停止容器（可选，不停止也可以）
docker-compose stop

# 2. 运行数据更新脚本（在宿主机）
python update_data.py

# 3. 启动容器（如果之前停止了）
docker-compose start

# 4. 重新加载数据（通过API）
curl -X POST http://localhost:8000/reload
```

### 方式2: 在容器内更新

```bash
# 进入容器
docker exec -it deanza-api bash

# 运行更新脚本
python update_data.py

# 或手动调用重新加载
curl -X POST http://localhost:8000/reload

# 退出容器
exit
```

---

## 🐛 故障排除

### 1. 容器无法启动

```bash
# 查看日志
docker-compose logs api

# 检查端口是否被占用
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac
```

### 2. 数据文件找不到

确保数据文件存在：
```bash
# 检查文件
ls -la rmp_deanza_all_professors.json

# 如果不存在，先运行数据抓取
python DeAnza_AllProfessors.py
```

### 3. 权限问题（Linux/Mac）

```bash
# 确保日志目录可写
mkdir -p logs
chmod 777 logs
```

### 4. 重新构建镜像

```bash
# 强制重新构建
docker-compose build --no-cache

# 重新启动
docker-compose up -d
```

---

## 📊 监控和管理

### 查看资源使用

```bash
# Docker Compose
docker-compose stats

# Docker
docker stats deanza-api
```

### 健康检查

容器包含健康检查，可以查看状态：

```bash
docker inspect deanza-api | grep -A 10 Health
```

---

## 🚢 生产环境部署

### 使用环境变量文件

创建 `.env` 文件：

```env
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=info
```

在 `docker-compose.yml` 中使用：

```yaml
environment:
  - API_PORT=${API_PORT}
  - API_HOST=${API_HOST}
```

### 使用Docker网络

```yaml
networks:
  app-network:
    driver: bridge

services:
  api:
    networks:
      - app-network
```

### 添加反向代理（Nginx）

可以添加Nginx服务作为反向代理，提供HTTPS和负载均衡。

---

## 📝 注意事项

1. **数据文件**: 确保 `rmp_deanza_all_professors.json` 文件存在，否则API将无法正常工作

2. **日志目录**: 容器会自动创建logs目录，但建议在宿主机上预先创建

3. **端口冲突**: 如果8000端口被占用，修改 `docker-compose.yml` 中的端口映射

4. **数据更新**: 更新数据后记得调用 `/reload` 端点或重启容器

5. **资源限制**: 可以在 `docker-compose.yml` 中添加资源限制：

```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

---

## 🔗 访问地址

容器启动后，可以通过以下地址访问：

- API首页: http://localhost:8000
- API文档: http://localhost:8000/docs
- 统计信息: http://localhost:8000/stats
- 部门列表: http://localhost:8000/departments

如果在远程服务器上，将 `localhost` 替换为服务器IP地址。

