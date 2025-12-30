# API部署方案说明

## 运行方式选择

API需要在**某个地方持续运行**才能24小时提供服务。有以下几种选择：

---

## 方案一：本地电脑运行（最简单）

### 适用场景
- 个人项目
- 内网使用
- 测试环境

### 要求
- 电脑需要**24小时开机**
- 网络需要**持续连接**
- 需要设置**电源管理**（防止休眠）

### 优缺点
✅ **优点**:
- 免费（无需额外服务器费用）
- 配置简单
- 直接访问

❌ **缺点**:
- 需要电脑一直开机（耗电）
- 本地IP可能变化（DDNS或固定IP）
- 电脑故障会影响服务
- 重启电脑需要重新启动服务

### 配置步骤
```powershell
# 1. 设置电源管理（禁用休眠）
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0

# 2. 启动API服务器（后台运行）
Start-Process python -ArgumentList "run_api_server.py" -WindowStyle Hidden

# 3. 设置定时更新（任务计划程序）
```

---

## 方案二：云服务器/VPS（推荐）

### 适用场景
- 正式项目
- 公网访问
- 需要稳定性

### 推荐云服务商
- **阿里云** (https://www.aliyun.com)
- **腾讯云** (https://cloud.tencent.com)
- **AWS** (https://aws.amazon.com)
- **DigitalOcean** (https://www.digitalocean.com)
- **Vultr** (https://www.vultr.com)

### 服务器要求
- **最低配置**: 1核CPU, 1GB内存, 20GB硬盘
- **推荐配置**: 2核CPU, 2GB内存, 40GB硬盘
- **系统**: Ubuntu 20.04/22.04 或 CentOS 7/8

### 价格参考
- 国内: ¥30-100/月（入门级）
- 国外: $5-10/月（入门级）

### 部署步骤
```bash
# 1. SSH连接到服务器
ssh user@your-server-ip

# 2. 上传项目文件（使用scp或git）
scp -r project/ user@server:/home/user/

# 3. 安装Python和依赖
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements_api.txt

# 4. 使用systemd创建服务（参考 deploy_24h.md）

# 5. 设置防火墙
sudo ufw allow 8000/tcp
```

### 优缺点
✅ **优点**:
- 24小时稳定运行
- 公网IP，可全球访问
- 专业运维支持
- 相对稳定

❌ **缺点**:
- 需要付费（但价格不高）
- 需要服务器管理知识
- 需要配置防火墙和安全

---

## 方案三：本地服务器/NAS

### 适用场景
- 有闲置服务器
- 内网使用
- 数据安全要求高

### 要求
- 服务器硬件
- 稳定的网络和电源
- 基本的Linux知识

### 优缺点
✅ **优点**:
- 数据完全掌控
- 无月租费用
- 可自定义配置

❌ **缺点**:
- 需要硬件投资
- 需要维护
- 需要稳定的网络和电力

---

## 方案四：容器云/Serverless（高级）

### 适用场景
- 大规模部署
- 需要弹性伸缩
- 不想管理服务器

### 平台选择
- **Heroku** (简单但较贵)
- **Railway** (价格适中)
- **Fly.io** (免费额度)
- **Google Cloud Run**
- **AWS Lambda** (Serverless)

### 优缺点
✅ **优点**:
- 无需管理服务器
- 自动扩缩容
- 高可用性

❌ **缺点**:
- 配置复杂
- 可能有额外费用
- 冷启动问题

---

## 方案对比表

| 方案 | 成本 | 稳定性 | 难度 | 适用场景 |
|------|------|--------|------|----------|
| 本地电脑 | 免费 | ⭐⭐ | ⭐ | 个人/测试 |
| 云服务器 | ¥30-100/月 | ⭐⭐⭐⭐ | ⭐⭐ | 正式项目 |
| 本地服务器 | 一次性 | ⭐⭐⭐ | ⭐⭐⭐ | 企业内网 |
| 容器云 | 按使用 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 大规模 |

---

## 我的推荐

### 对于个人项目/学习
**选择：本地电脑运行**
- 最简单，无需额外费用
- 设置电源不休眠
- 使用 `run_api_server.py` 后台运行

### 对于正式项目/公网使用
**选择：云服务器（VPS）**
- 阿里云/腾讯云入门级服务器
- 使用systemd管理服务
- 配置定时更新任务

---

## 快速决策指南

### 选择本地电脑，如果：
- ✅ 预算有限
- ✅ 只是个人使用
- ✅ 电脑可以24小时开机
- ✅ 能接受偶尔的服务中断

### 选择云服务器，如果：
- ✅ 需要公网访问
- ✅ 需要稳定性
- ✅ 有预算（每月几十元）
- ✅ 愿意学习服务器管理

---

## 本地电脑运行详细配置

### Windows配置

1. **禁用休眠和睡眠**
```powershell
# 管理员PowerShell运行
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 0
```

2. **设置API自动启动**
```powershell
# 创建启动脚本 start_api.bat
# 添加到启动文件夹
# Win+R -> shell:startup
# 复制 start_api.bat 到启动文件夹
```

3. **配置防火墙**
```powershell
# 允许8000端口（如果需要外部访问）
New-NetFirewallRule -DisplayName "DeAnza API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### 本地IP固定（可选）

如果需要从外部访问：

1. **使用DDNS服务**（如花生壳、No-IP）
2. **路由器端口转发**（8000端口）
3. **使用ngrok**（临时访问）
```bash
ngrok http 8000
```

---

## 云服务器部署快速指南

### 1. 购买服务器
- 选择Ubuntu 20.04系统
- 最低配置：1核1GB即可

### 2. 上传项目
```bash
# 方式1: 使用git
git clone your-repo
cd project

# 方式2: 使用scp
scp -r project/ user@server:/home/user/
```

### 3. 安装依赖
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements_api.txt
```

### 4. 创建系统服务
```bash
# 参考 deploy_24h.md 中的systemd配置
sudo nano /etc/systemd/system/deanza-api.service
sudo systemctl start deanza-api
sudo systemctl enable deanza-api
```

### 5. 配置防火墙
```bash
sudo ufw allow 8000/tcp
sudo ufw enable
```

---

## 总结

**不一定需要专门的服务器**，但需要：
- ✅ 某个设备**持续运行**
- ✅ 可以是本地电脑（24小时开机）
- ✅ 可以是云服务器（推荐）
- ✅ 可以是本地服务器/NAS

根据你的**使用场景**和**预算**选择合适的方案即可！


