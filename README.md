# PyErr - Python 纠错助手

`PyErr` 是一个面向 Python 初学者的报错分析与速查工具，采用前后端分离架构：

- `frontend/`：Vue 3 + TypeScript + Vite
- `backend/`：FastAPI + SQLAlchemy + SQLite

## 核心功能

- 报错分析：输入报错信息后返回解释、常见原因、排查步骤和建议方案
- 错误检索：支持关键字搜索（中英文/模糊）
- 热门错误：提供高频错误入口，便于快速查阅
- 反馈机制：用户可提交分析反馈，持续优化规则
- 管理后台：规则增删改查、统计信息查看、登录保护

## 项目结构

- `backend/`：API 服务与数据层
- `frontend/`：Web 前端应用
- `docker-compose.yml`：一键部署编排
- `DEPLOY.md`：Linux 服务器部署说明
- `.env.server.example`：服务端环境变量示例

## 主要 API

- `POST /api/analyze`
- `GET /api/search`
- `GET /api/highlights`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/feedback`
- `GET /api/admin/rules`
- `POST /api/admin/rules`
- `PUT /api/admin/rules/{id}`
- `DELETE /api/admin/rules/{id}`
- `GET /api/admin/stats`

## 本地开发

### 1. 启动后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

后端默认地址：`http://127.0.0.1:8000`

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

## 管理员默认账号

- 用户名：`admin`
- 密码：`admin123456`

可通过环境变量覆盖：

- `PYERR_ADMIN_USERNAME`
- `PYERR_ADMIN_PASSWORD`
- `PYERR_TOKEN_SECRET`
- `PYERR_TOKEN_EXPIRE_SECONDS`

## Docker 部署

参见 [DEPLOY.md](./DEPLOY.md)。

基本步骤：

1. 复制 `.env.server.example` 为 `.env`
2. 按服务器信息修改环境变量
3. 运行 `docker compose up -d --build`

