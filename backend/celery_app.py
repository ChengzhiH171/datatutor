"""Celery 异步任务配置（成员D）

Redis 数据库分配：
  DB 0 —— Celery broker（任务队列）
  DB 1 —— Celery backend（结果存储）
  DB 2 —— SocketIO 消息队列（Worker → Flask-SocketIO 服务端跨进程 emit）
"""
from celery import Celery
import os

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

celery_app = Celery(
    'datatutor',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
    # Worker 启动时自动加载任务模块，确保任务被注册
    include=['tasks.report_task'],
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    # 结果保留 1 小时，足够前端轮询兜底
    result_expires=3600,
)
