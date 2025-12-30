# 24小时运行快速开始指南

## 🚀 快速部署（3步）

### 步骤1: 启动API服务器

#### Windows:
```powershell
# 方式1: 后台运行（推荐）
Start-Process python -ArgumentList "run_api_server.py" -WindowStyle Hidden

# 方式2: 双击运行
start_api.bat
```

#### Linux/Mac:
```bash
# 后台运行
chmod +x start_api.sh
./start_api.sh

# 或手动运行
nohup python3 run_api_server.py > logs/server.log 2>&1 &
```

### 步骤2: 设置定时更新

#### Windows (任务计划程序):
1. 打开"任务计划程序"
2. 创建基本任务
3. 名称: "DeAnza数据更新"
4. 触发器: 每天，凌晨2点
5. 操作: 启动程序
   - 程序: `python.exe`
   - 参数: `update_data.py`
   - 起始于: `E:\小元芳\总2054个教授`

#### Linux (Crontab):
```bash
# 编辑crontab
crontab -e

# 添加（每天凌晨2点更新）
0 2 * * * cd /path/to/project && python3 update_data.py >> logs/update.log 2>&1
```

### 步骤3: 验证运行

```bash
# 检查API是否运行
curl http://localhost:8000/stats?format=json

# 手动触发数据更新
python update_data.py

# 手动重新加载数据（无需重启服务器）
curl -X POST http://localhost:8000/reload
```

---

## 📋 核心文件说明

### 1. `run_api_server.py`
- **功能**: 运行API服务器，支持自动重启
- **用途**: 确保服务器24小时运行

### 2. `update_data.py`
- **功能**: 自动抓取最新数据并更新API
- **用途**: 定时运行，保持数据最新

### 3. `api.py`
- **功能**: API服务器
- **新端点**: `POST /reload` - 重新加载数据（无需重启）

---

## 🔄 工作流程

```
定时任务 (每天2点)
    ↓
运行 update_data.py
    ↓
执行 DeAnza_AllProfessors.py (抓取数据)
    ↓
保存到 rmp_deanza_all_professors.json
    ↓
调用 POST /reload (重新加载数据)
    ↓
API数据更新完成 ✓
```

---

## ⚙️ 配置选项

### 更新频率
- **推荐**: 每天1-2次（凌晨2-3点）
- **最多**: 每小时1次（避免被封IP）

### 服务器端口
- **默认**: 8000
- **修改**: 编辑 `api.py` 最后一行

### 日志位置
- **API日志**: `logs/server.log`
- **更新日志**: `logs/update.log`

---

## 🔍 监控命令

### Windows:
```powershell
# 查看API进程
Get-Process python | Where-Object {$_.CommandLine -like "*api.py*"}

# 查看端口占用
netstat -ano | findstr :8000

# 测试API
Invoke-WebRequest http://localhost:8000/stats?format=json
```

### Linux:
```bash
# 查看API进程
ps aux | grep api.py

# 查看端口占用
netstat -tlnp | grep 8000

# 测试API
curl http://localhost:8000/stats?format=json

# 查看日志
tail -f logs/server.log
```

---

## 🛠️ 故障排除

### API无法启动
1. 检查端口8000是否被占用
2. 检查Python环境是否正确
3. 查看错误日志

### 数据更新失败
1. 检查网络连接
2. 检查RateMyProfessors网站是否可访问
3. 查看 `logs/update.log` 日志

### 数据没有更新
1. 手动运行 `python update_data.py`
2. 手动调用 `POST /reload`
3. 重启API服务器

---

## 📝 完整部署方案

详细部署方案请查看 `deploy_24h.md` 文件，包含：
- Windows服务（NSSM）
- Linux系统服务（systemd）
- Docker容器化
- 其他高级配置

---

## ✅ 验证清单

- [ ] API服务器正在运行
- [ ] 可以访问 http://localhost:8000
- [ ] 定时任务已设置
- [ ] 日志文件正常生成
- [ ] 数据更新脚本可正常运行
- [ ] `/reload` 端点正常工作

---

## 🎯 推荐配置

- **服务器**: 最低2GB内存，稳定网络
- **更新频率**: 每天1次（凌晨2点）
- **监控**: 每天检查一次日志
- **备份**: 每周备份一次数据文件


