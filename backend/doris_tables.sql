-- ============================================================
-- DataTutor 学情分析 — Doris 建表 SQL（成员E）
-- 在 Doris 中执行此脚本创建数据库和 4 张行为日志表
-- ============================================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS datatutor_analytics;

USE datatutor_analytics;

-- 1. 终端事件表
DROP TABLE IF EXISTS terminal_events;
CREATE TABLE terminal_events (
    event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    student_id INT NOT NULL DEFAULT '0',
    course_id INT NOT NULL DEFAULT '0',
    subtask_id INT NOT NULL DEFAULT '0',
    vm_name VARCHAR(100) DEFAULT '',
    data VARCHAR(500) DEFAULT '',
    direction VARCHAR(10) DEFAULT ''
) DUPLICATE KEY(event_time, student_id, course_id)
DISTRIBUTED BY HASH(student_id) BUCKETS 3
PROPERTIES ("replication_num" = "1");

-- 2. AI 对话事件表
DROP TABLE IF EXISTS chat_events;
CREATE TABLE chat_events (
    event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    student_id INT NOT NULL DEFAULT '0',
    course_id INT NOT NULL DEFAULT '0',
    subtask_id INT NOT NULL DEFAULT '0',
    msg_role VARCHAR(20) DEFAULT '',
    msg_length INT NOT NULL DEFAULT '0'
) DUPLICATE KEY(event_time, student_id, course_id)
DISTRIBUTED BY HASH(student_id) BUCKETS 3
PROPERTIES ("replication_num" = "1");

-- 3. 任务完成事件表
DROP TABLE IF EXISTS task_completions;
CREATE TABLE task_completions (
    event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    student_id INT NOT NULL DEFAULT '0',
    course_id INT NOT NULL DEFAULT '0',
    subtask_id INT NOT NULL DEFAULT '0',
    duration_seconds INT NOT NULL DEFAULT '0',
    grade_level VARCHAR(10) DEFAULT ''
) DUPLICATE KEY(event_time, student_id, course_id)
DISTRIBUTED BY HASH(student_id) BUCKETS 3
PROPERTIES ("replication_num" = "1");

-- 4. 页面访问表
DROP TABLE IF EXISTS page_views;
CREATE TABLE page_views (
    event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    student_id INT NOT NULL DEFAULT '0',
    page VARCHAR(100) DEFAULT '',
    duration_seconds INT NOT NULL DEFAULT '0'
) DUPLICATE KEY(event_time, student_id)
DISTRIBUTED BY HASH(student_id) BUCKETS 2
PROPERTIES ("replication_num" = "1");

-- 验证
SHOW TABLES;
