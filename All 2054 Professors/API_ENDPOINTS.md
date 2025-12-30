# De Anza College Professors API - 所有端点列表

## 基础信息
- **API 基础URL**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs` (Swagger UI)
- **替代文档**: `http://localhost:8000/redoc` (ReDoc)

---

## 端点列表

### 1. 首页 / Web界面
**GET** `/`

- **描述**: 返回美化的Web界面（HTML）或API信息（JSON）
- **浏览器访问**: 返回HTML页面
- **API调用**: 返回JSON格式的端点列表
- **示例**:
  - 浏览器: `http://localhost:8000/`
  - API: `http://localhost:8000/?format=json`

---

### 2. 获取所有教授
**GET** `/professors`

- **描述**: 获取所有教授列表，支持分页和筛选
- **查询参数**:
  - `page` (int, 可选): 页码，从1开始，默认=1
  - `limit` (int, 可选): 每页结果数，最大100，默认=20
  - `department` (string, 可选): 按部门筛选
  - `min_rating` (float, 可选): 最低平均评分 (0-5)
  - `max_difficulty` (float, 可选): 最高平均难度 (0-5)
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **示例**:
  - 浏览器: `http://localhost:8000/professors`
  - 浏览器（筛选）: `http://localhost:8000/professors?department=Mathematics&min_rating=4.0`
  - API: `http://localhost:8000/professors?format=json&page=1&limit=20`
  - API（筛选）: `http://localhost:8000/professors?format=json&department=History&min_rating=4.0&max_difficulty=3.0`

---

### 3. 按姓名搜索教授
**GET** `/professors/name/{name}`

- **描述**: 根据教授姓名搜索（支持部分匹配，不区分大小写）
- **路径参数**:
  - `name` (string, 必需): 教授姓名（可以是部分匹配）
- **查询参数**:
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **示例**:
  - 浏览器: `http://localhost:8000/professors/name/Smith`
  - 浏览器: `http://localhost:8000/professors/name/John`
  - API: `http://localhost:8000/professors/name/Smith?format=json`

---

### 4. 按部门获取教授
**GET** `/professors/department/{department}`

- **描述**: 获取指定部门的所有教授
- **路径参数**:
  - `department` (string, 必需): 部门名称
- **查询参数**:
  - `page` (int, 可选): 页码，从1开始，默认=1
  - `limit` (int, 可选): 每页结果数，最大100，默认=20
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **示例**:
  - 浏览器: `http://localhost:8000/professors/department/Mathematics`
  - 浏览器: `http://localhost:8000/professors/department/Computer%20Information%20Systems`
  - API: `http://localhost:8000/professors/department/History?format=json&page=1&limit=10`

---

### 5. 搜索教授
**GET** `/search`

- **描述**: 搜索教授（在姓名和部门中搜索）
- **查询参数**:
  - `q` (string, 必需): 搜索关键词
  - `page` (int, 可选): 页码，从1开始，默认=1
  - `limit` (int, 可选): 每页结果数，最大100，默认=20
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **示例**:
  - 浏览器: `http://localhost:8000/search?q=math`
  - 浏览器: `http://localhost:8000/search?q=Smith`
  - API: `http://localhost:8000/search?q=computer&format=json&page=1&limit=20`

---

### 6. 统计信息
**GET** `/stats`

- **描述**: 获取数据库统计信息
- **查询参数**:
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **返回数据**:
  - `total_professors`: 总教授数
  - `total_reviews`: 总评价数
  - `departments`: 部门统计（数量和列表）
  - `ratings`: 评分统计（平均、最低、最高）
  - `difficulty`: 难度统计（平均、最低、最高）
  - `top_departments`: 热门部门Top 10
- **示例**:
  - 浏览器: `http://localhost:8000/stats`
  - API: `http://localhost:8000/stats?format=json`

---

### 7. 获取所有部门列表
**GET** `/departments`

- **描述**: 获取所有部门的列表
- **查询参数**:
  - `format` (string, 可选): 响应格式，'json' 或 'html'，默认='html'
- **返回数据**:
  - `count`: 部门总数
  - `departments`: 部门名称列表（排序后）
- **示例**:
  - 浏览器: `http://localhost:8000/departments`
  - API: `http://localhost:8000/departments?format=json`

---

## 响应格式说明

### HTML格式（默认）
- 浏览器访问时自动返回美化的HTML页面
- 包含完整的UI界面、样式和交互功能
- 适合用户直接浏览

### JSON格式
- 添加 `?format=json` 参数获取JSON数据
- 适合API调用和程序集成
- 返回纯数据，无HTML标签

---

## 快速参考

### 常用端点（浏览器访问）
```
http://localhost:8000/                              # 首页
http://localhost:8000/professors                    # 所有教授
http://localhost:8000/professors/name/Smith        # 搜索姓名
http://localhost:8000/professors/department/Math   # 按部门
http://localhost:8000/search?q=computer           # 搜索
http://localhost:8000/stats                        # 统计信息
http://localhost:8000/departments                  # 部门列表
http://localhost:8000/docs                         # API文档
```

### 常用端点（API调用）
```
http://localhost:8000/professors?format=json
http://localhost:8000/professors/name/Smith?format=json
http://localhost:8000/professors/department/Math?format=json
http://localhost:8000/search?q=computer&format=json
http://localhost:8000/stats?format=json
http://localhost:8000/departments?format=json
```

---

## 注意事项

1. **URL编码**: 如果部门名称或姓名包含空格或特殊字符，需要进行URL编码
   - 例如: `Computer Information Systems` → `Computer%20Information%20Systems`

2. **分页**: 所有列表端点都支持分页，默认每页20条，最多100条

3. **筛选组合**: `/professors` 端点支持多个筛选条件组合使用

4. **搜索**: `/search` 端点会在姓名和部门中同时搜索

5. **格式切换**: 所有端点都支持通过 `format` 参数在HTML和JSON之间切换

