# DataTutor —— 大数据技术学科垂类智能教学助手

面向一流学科建设的学科垂类大模型与创新应用开发平台，基座模型为**讯飞星火认知大模型 V4.0**。

## 已实现功能

| 功能 | 说明 |
|------|------|
| AI 实训副驾 | 终端内实时对话辅导，对话自动保存供报告生成 |
| AI 课程生成 | Teacher Agent 自动生成实训课程和子任务，支持文件上传辅助 |
| Docker 隔离实训 | 每个学生独立容器，所有安装包本地预置免下载 |
| 多角色管理 | 学生/教师/管理员三端，课程班级子任务全生命周期 |
| 学情分析 | 进度追踪、任务完成率统计 |
| 实训报告生成 | 基于对话记录和完成情况自动生成个性化报告 |
| 知识库问答 | 大数据领域知识 RAG 问答 |

## 技术栈

- 后端: Python 3.8 / Flask / Flask-SocketIO / SQLAlchemy / Celery
- 数据库: MySQL 8.0 / Redis 7
- AI 引擎: 讯飞星火认知大模型 V4.0 → 星辰 MaaS 工作流 Agent API
- 容器化: Docker / Docker Compose
- 前端: HTML5 / Tailwind CSS / Iconify

## 讯飞星火 Agent

| Agent | 输入 | 用途 |
|-------|------|------|
| 实训副驾 | 系统提示 + 终端上下文 + 文件预览 + 学生消息 | 终端内实时辅导，对话自动存储 |
| 知识问答 | 系统提示 + 终端上下文 + 学生问题 | 大数据领域知识检索 |
| 课程生成 | 课程主题 + 文件预览 | AI 自动生成实训课程和子任务 |
| 报告生成 | 课程信息 + 完成情况 + 对话摘要 | 自动生成学生个人实训报告 |

## 学生容器环境

学生登录后自动分配独立 Docker 实训环境：

| 配置 | 值 |
|------|-----|
| 容器名 | dts-student{ID} |
| SSH 端口 | 2200+ID |
| 账号 | learner / 123456 |
| 课程数据 | /home/learner/course-data/ (只读挂载) |
| 安装包 | /home/learner/packages/ (只读挂载) |

11 门课程预置安装包: Hadoop, Spark, Hive, Kafka, Flink, ZooKeeper, HBase, Flume, Sqoop, Storm

## 快速启动

环境要求: Docker & Docker Compose, Python 3.8+

配置: 复制 backend/.env.example 为 backend/.env，填入讯飞星火 API 密钥

启动: docker-compose up -d mysql && cd backend && python3 app.py

默认: http://localhost/login.html

## 项目结构

```
/opt/datatutor/
├── backend/
│   ├── routes/      ai.py / auth.py / courses.py / chat.py
│   ├── terminal_ws/  SSH WebSocket 终端
│   └── tasks/        异步报告生成
├── frontend/
│   ├── login.html    登录/注册
│   ├── teacher.html  教师工作台
│   ├── hub.html      学生实训台
│   └── admin.html    管理员面板
├── docker-compose.yml
└── .env.example
```
