# Dentistry

前后端分离的内容与文件管理项目。前端可提交文字与文件（图片/音频/视频），后端持久化到数据库并对外提供 API；前端可拉取并展示这些内容。

2026-3-17/duanhuiwen:当前运行起来后可以发送文件和文字到后端储存起来，后端只会返回“医生组正在思考中”，并显示。暂时没有接入智能体！！！路漫漫其修远兮，口腔种植学的知识填充仍需继续进行！！！

## 运行方式

### 后端

```bash
cd dentistry
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 文档: http://127.0.0.1:8000/docs  
- 若前端在 `dentistry/frontend` 下，可直接访问: http://127.0.0.1:8000/app/

### 前端

- **方式一**：后端启动后访问 http://127.0.0.1:8000/app/  
- **方式二**：用任意静态服务器在 `frontend` 目录下起服务（如 `python -m http.server 3000`），页面中 API 请求会发往 `http://127.0.0.1:8000`（见 `frontend/static/js/app.js` 中的 `API_BASE`）

## 环境变量

复制 `.env.example` 为 `.env` 并按需修改。可选项：

- `DATABASE_URL`: 数据库连接（默认 SQLite）
- `CORS_ORIGINS`: CORS 允许来源列表

## 项目结构

- `backend/app/`: FastAPI 应用
  - `api/v1/`: 版本化 API 路由（contents、upload、health）
  - `core/`: 配置与数据库连接
  - `models/`: SQLAlchemy 模型
  - `schemas/`: Pydantic 请求/响应模型
  - `services/`: 业务逻辑
  - `repos/`: 数据访问层（便于扩展分析查询）
- `backend/uploads/`: 上传文件存储
- `frontend/`: 静态前端（可自行替换为 Vue/React 等）

## API 契约（便于扩展与替换前端）

- `POST /api/v1/contents` — 提交文字，body: `{ "type": "text", "text_content": "..." }`
- `POST /api/v1/upload` — 上传文件，multipart `file`
- `GET /api/v1/contents?since=&limit=` — 拉取内容列表
- 文件访问: `GET /api/v1/files/<path>`（返回的 `file_url` 即此形式）

列表与推送中的每项结构：`id`, `type`, `text_content?`, `file_url?`, `created_at`。

## 后续扩展

- **前端 UI**：可只改 `frontend/` 下的 HTML/CSS/JS 或整站替换为其他框架，保持上述 API 契约即可。
- **数据分析与处理**：在 `app/services/` 下新增模块（如 `analysis_service`），或单独脚本读取数据库与 `uploads/`；需要新接口时在 `app/api/v1/` 下增加路由（如 `/api/v1/analytics/`、`/api/v1/export/`）。
- **数据库变更**：建议使用 Alembic 做迁移，避免直接改表结构破坏兼容性。同时数据库中应该存储大量的口腔种植学的文字图片资料，用作一个知识库。但是对于这个知识库应该智能化管理还是使用字符检索的调用方法，暂时没有考虑清楚，可能需要后续和计算机系的共同讨论之后得到。
- **后续人工智能的接入**：做一个中间程序，调用db的存储数据，然后调用模型的API之后得到返回结果，大部分对话内容可以直接调用前端的展示窗口API展示到前端。
- **智能体训练建议**：建议使用成型智能体，理想情况是中间程序可以访问网页版的智能体，完成对话，但感觉只限于对话，其他的内容需要提前生成并存储起来以备不时之需。
