# 24小时运行和实时更新部署指南

## 方案概述

本指南提供了让API服务器24小时运行并自动更新数据的几种方案。

---

## 方案一：Windows服务（推荐用于Windows服务器）

### 1. 使用NSSM（Non-Sucking Service Manager）

#### 安装NSSM
1. 下载NSSM: https://nssm.cc/download
2. 解压到项目目录或系统PATH

#### 创建API服务
```powershell
# 安装API服务
nssm install DeAnzaAPI "C:\Python312\python.exe" "E:\小元芳\总2054个教授\api.py"

# 配置服务
nssm set DeAnzaAPI AppDirectory "E:\小元芳\总2054个教授"
nssm set DeAnzaAPI AppStdout "E:\小元芳\总2054个教授\logs\api.log"
nssm set DeAnzaAPI AppStderr "E:\小元芳\总2054个教授\logs\api_error.log"

# 启动服务
nssm start DeAnzaAPI

# 查看服务状态
nssm status DeAnzaAPI
```

#### 创建数据更新服务（定时任务）
使用Windows任务计划程序：
1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（例如：每天凌晨2点）
4. 操作：启动程序
   - 程序：`python.exe`
   - 参数：`E:\小元芳\总2054个教授\update_data.py`
   - 起始于：`E:\小元芳\总2054个教授`

---

## 方案二：使用Python脚本后台运行（简单方案）

### 1. 运行API服务器

#### Windows PowerShell（后台运行）
```powershell
# 后台运行API服务器
Start-Process python -ArgumentList "api.py" -WindowStyle Hidden

# 或使用run_api_server.py（支持自动重启）
Start-Process python -ArgumentList "run_api_server.py" -WindowStyle Hidden
```

#### Linux/Mac（使用nohup）
```bash
# 后台运行API服务器
nohup python api.py > logs/api.log 2>&1 &

# 或使用run_api_server.py（支持自动重启）
nohup python run_api_server.py > logs/server.log 2>&1 &

# 查看进程
ps aux | grep api.py
```

### 2. 定时更新数据

#### Windows任务计划程序
1. 创建定时任务运行 `update_data.py`
2. 建议频率：每天1-2次（避免过于频繁）

#### Linux Crontab
```bash
# 编辑crontab
crontab -e

# 添加以下行（每天凌晨2点更新）
0 2 * * * cd /path/to/project && /usr/bin/python3 update_data.py >> logs/update.log 2>&1

# 查看crontab
crontab -l
```

---

## 方案三：使用systemd（Linux系统，推荐）

### 1. 创建API服务文件

创建 `/etc/systemd/system/deanza-api.service`:

```ini
[Unit]
Description=De Anza College Professors API
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/project/api.py
Restart=always
RestartSec=10
StandardOutput=append:/path/to/project/logs/api.log
StandardError=append:/path/to/project/logs/api_error.log

[Install]
WantedBy=multi-user.target
```

### 2. 创建数据更新服务

创建 `/etc/systemd/system/deanza-update.service`:

```ini
[Unit]
Description=De Anza College Data Update
After=network.target

[Service]
Type=oneshot
User=your_user
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python3 /path/to/project/update_data.py
StandardOutput=append:/path/to/project/logs/update.log
StandardError=append:/path/to/project/logs/update_error.log
```

### 3. 创建定时器

创建 `/etc/systemd/system/deanza-update.timer`:

```ini
[Unit]
Description=De Anza College Data Update Timer
Requires=deanza-update.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

### 4. 启动服务

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启动API服务
sudo systemctl start deanza-api
sudo systemctl enable deanza-api

# 启动数据更新定时器
sudo systemctl start deanza-update.timer
sudo systemctl enable deanza-update.timer

# 查看服务状态
sudo systemctl status deanza-api
sudo systemctl status deanza-update.timer

# 查看日志
sudo journalctl -u deanza-api -f
sudo journalctl -u deanza-update -f
```

---

## 方案四：使用Docker（容器化部署）

### 1. 创建Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./rmp_deanza_all_professors.json:/app/rmp_deanza_all_professors.json
      - ./logs:/app/logs
    restart: always
    environment:
      - PYTHONUNBUFFERED=1

  updater:
    build: .
    command: python update_data.py
    volumes:
      - ./rmp_deanza_all_professors.json:/app/rmp_deanza_all_professors.json
      - ./logs:/app/logs
    restart: "no"
    depends_on:
      - api
```

### 3. 运行Docker容器

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f api

# 设置定时更新（使用cron或外部调度）
```

---

## 自动更新配置

### update_data.py 使用说明

```python
# 运行一次更新
python update_data.py

# 这将：
# 1. 运行 DeAnza_AllProfessors.py 抓取最新数据
# 2. 自动调用 API 的 /reload 端点重新加载数据
# 3. 无需重启API服务器
```

### API重新加载端点

```
POST http://localhost:8000/reload
```

这个端点会重新加载JSON文件中的数据，无需重启服务器。

---

## 监控和维护

### 1. 日志管理

创建logs目录：
```bash
mkdir logs
```

建议日志轮转（防止日志文件过大）：
- Windows: 使用日志轮转工具
- Linux: 使用logrotate

### 2. 健康检查

可以添加健康检查端点：
```
GET http://localhost:8000/health
```

### 3. 监控脚本

创建监控脚本检查API是否运行：
```bash
#!/bin/bash
# check_api.sh
if ! curl -f http://localhost:8000/stats?format=json > /dev/null 2>&1; then
    echo "API is down, restarting..."
    systemctl restart deanza-api
fi
```

---

## 推荐配置

### 更新频率建议
- **数据更新**: 每天1-2次（建议凌晨2-3点，流量低）
- **API检查**: 每5分钟检查一次服务状态

### 资源要求
- **CPU**: 低（API服务器），中等（数据抓取时）
- **内存**: 建议至少2GB
- **磁盘**: 根据数据大小（当前约几十MB）
- **网络**: 稳定的互联网连接

---

## 故障处理

### API服务器崩溃
- 使用 `run_api_server.py` 自动重启
- 或使用systemd/NSSM自动重启功能

### 数据更新失败
- 检查网络连接
- 检查RateMyProfessors网站是否可访问
- 查看更新日志

### 数据不同步
- 手动调用 `/reload` 端点
- 或重启API服务器

---

## 安全建议

1. **防火墙**: 只开放必要端口（8000）
2. **认证**: 考虑为 `/reload` 端点添加认证
3. **HTTPS**: 生产环境建议使用HTTPS
4. **访问限制**: 考虑添加访问频率限制

---

## 快速开始（最简单方案）

### Windows
```powershell
# 1. 后台运行API
Start-Process python -ArgumentList "run_api_server.py" -WindowStyle Hidden

# 2. 设置定时任务运行 update_data.py（使用任务计划程序）
```

### Linux
```bash
# 1. 后台运行API
nohup python run_api_server.py > logs/server.log 2>&1 &

# 2. 添加到crontab（每天凌晨2点更新）
(crontab -l 2>/dev/null; echo "0 2 * * * cd $(pwd) && python update_data.py >> logs/update.log 2>&1") | crontab -
```


