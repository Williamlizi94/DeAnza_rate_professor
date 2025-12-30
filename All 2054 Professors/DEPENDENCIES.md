# 项目依赖说明

## 📦 完整依赖列表

### 第三方库（需要安装）

| 包名 | 版本 | 用途 | 使用位置 |
|------|------|------|----------|
| `fastapi` | 0.104.1 | Web框架，构建RESTful API | api.py |
| `uvicorn[standard]` | 0.24.0 | ASGI服务器，运行FastAPI | api.py |
| `requests` | >=2.31.0 | HTTP库，数据抓取和API调用 | DeAnza_AllProfessors.py, update_data.py |

### Python标准库（内置，无需安装）

以下库是Python标准库，无需额外安装：

| 库名 | 用途 | 使用位置 |
|------|------|----------|
| `re` | 正则表达式 | DeAnza_AllProfessors.py |
| `json` | JSON数据处理 | 所有文件 |
| `time` | 时间处理 | DeAnza_AllProfessors.py, api.py, run_api_server.py |
| `csv` | CSV文件处理 | DeAnza_AllProfessors.py |
| `typing` | 类型提示 | DeAnza_AllProfessors.py, api.py |
| `subprocess` | 子进程管理 | update_data.py, run_api_server.py |
| `sys` | 系统相关 | update_data.py, run_api_server.py |
| `os` | 操作系统接口 | api.py, update_data.py, run_api_server.py |
| `datetime` | 日期时间 | update_data.py |
| `signal` | 信号处理 | run_api_server.py |

---

## 🚀 安装方法

### 方法1: 使用 requirements.txt（推荐）

```bash
# 安装所有依赖
pip install -r requirements.txt

# 使用国内镜像源（推荐，速度更快）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方法2: 使用 requirements_api.txt

```bash
pip install -r requirements_api.txt
```

### 方法3: 手动安装

```bash
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install requests>=2.31.0
```

---

## 📋 各文件依赖详情

### 1. api.py
**依赖**:
- `fastapi` - Web框架
- `uvicorn` - 服务器（通过运行脚本）
- 标准库: `json`, `os`, `time`, `typing`

### 2. DeAnza_AllProfessors.py
**依赖**:
- `requests` - HTTP请求和数据抓取
- 标准库: `re`, `json`, `time`, `csv`, `typing`

### 3. update_data.py
**依赖**:
- `requests` - API调用（可选，如果API不可用则跳过）
- 标准库: `subprocess`, `sys`, `os`, `json`, `datetime`

### 4. run_api_server.py
**依赖**:
- 标准库: `subprocess`, `sys`, `os`, `time`, `signal`
- 注: 此文件只负责运行api.py，本身不需要额外依赖

---

## 🔍 依赖版本说明

### FastAPI 0.104.1
- 稳定的Web框架版本
- 支持异步操作
- 自动生成API文档

### Uvicorn 0.24.0
- `[standard]` 包含高性能依赖：
  - `httptools` - HTTP解析器
  - `uvloop` - 事件循环（Linux/Mac）
  - `watchfiles` - 文件监控（开发模式）
  - `python-dotenv` - 环境变量支持

### Requests >=2.31.0
- HTTP请求库
- 用于数据抓取
- 兼容Python 3.8+

---

## ⚙️ Python版本要求

- **最低版本**: Python 3.8
- **推荐版本**: Python 3.10 或 3.12
- **已测试版本**: Python 3.12

---

## 🔄 更新依赖

### 更新到最新版本（谨慎）

```bash
# 更新所有包到最新兼容版本
pip install --upgrade fastapi uvicorn requests

# 查看当前版本
pip list | grep -E "fastapi|uvicorn|requests"
```

### 锁定版本（推荐）

建议使用 `requirements.txt` 中指定的版本，以确保稳定性。

---

## 🐛 常见问题

### 1. 安装失败

**问题**: `pip install` 失败

**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 版本冲突

**问题**: 与其他项目依赖冲突

**解决方案**:
```bash
# 使用虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 然后安装依赖
pip install -r requirements.txt
```

### 3. uvicorn[standard] 安装慢

**问题**: 某些系统上安装较慢

**解决方案**:
```bash
# 先安装基础版本
pip install uvicorn

# 或只安装必要依赖
pip install uvicorn httptools
```

---

## 📊 依赖大小估算

- `fastapi`: ~1MB
- `uvicorn[standard]`: ~5-10MB
- `requests`: ~1-2MB

**总计**: 约 10-15MB

---

## 🔒 安全建议

1. **定期更新**: 定期检查并更新依赖包以修复安全漏洞
2. **虚拟环境**: 使用虚拟环境隔离项目依赖
3. **版本锁定**: 在生产环境使用固定版本
4. **安全检查**: 使用工具检查已知漏洞
   ```bash
   pip install safety
   safety check -r requirements.txt
   ```

---

## 📝 文件说明

- **requirements.txt**: 完整依赖列表（包含详细说明）
- **requirements_api.txt**: 简化版依赖列表（仅包名和版本）
- **DEPENDENCIES.md**: 本文档（详细说明）

