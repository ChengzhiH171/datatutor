"""Docker 初始化 — MySQL 用户 + Doris 表"""
import pymysql, os, time
from werkzeug.security import generate_password_hash

print('Waiting for MySQL...')
for i in range(30):
    try:
        conn = pymysql.connect(host='mysql', user='root', password='datatutor123', port=3306, connect_timeout=2)
        conn.close()
        break
    except:
        time.sleep(2)

# 1. MySQL 种子用户
conn = pymysql.connect(host='mysql', user='root', password='datatutor123', port=3306, database='datatutor')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM users')
if cur.fetchone()[0] == 0:
    users = [
        ('tanwei', generate_password_hash('tanwei'), 'teacher', 'TW'),
        ('student1', generate_password_hash('123456'), 'student', 'student1'),
        ('stu001', generate_password_hash('123456'), 'student', 'stu001'),
        ('student2', generate_password_hash('123456'), 'student', 'student2'),
    ]
    for u in users:
        cur.execute('INSERT INTO users (username, password_hash, role, display_name) VALUES (%s,%s,%s,%s)', u)
    conn.commit()
    print('MySQL users created')
cur.close(); conn.close()

# 2. Doris 表
print('Waiting for Doris...')
for i in range(30):
    try:
        conn = pymysql.connect(host='doris', user='root', password='', port=9030, connect_timeout=2)
        cur = conn.cursor()
        cur.execute('SHOW DATABASES')
        cur.close(); conn.close()
        break
    except:
        time.sleep(3)

conn = pymysql.connect(host='doris', user='root', password='', port=9030)
cur = conn.cursor()
cur.execute('CREATE DATABASE IF NOT EXISTS datatutor_analytics')
cur.execute('USE datatutor_analytics')

tables = [
    'CREATE TABLE IF NOT EXISTS terminal_events (student_id INT, event_time DATETIME DEFAULT CURRENT_TIMESTAMP, course_id INT, subtask_id INT, vm_name VARCHAR(50), data STRING, direction VARCHAR(10)) DUPLICATE KEY(student_id, event_time) DISTRIBUTED BY HASH(student_id) BUCKETS 2 PROPERTIES("replication_num"="1")',
    'CREATE TABLE IF NOT EXISTS chat_events (student_id INT, event_time DATETIME DEFAULT CURRENT_TIMESTAMP, course_id INT, subtask_id INT, msg_role VARCHAR(10), msg_length INT) DUPLICATE KEY(student_id, event_time) DISTRIBUTED BY HASH(student_id) BUCKETS 2 PROPERTIES("replication_num"="1")',
    'CREATE TABLE IF NOT EXISTS task_completions (student_id INT, event_time DATETIME DEFAULT CURRENT_TIMESTAMP, course_id INT, subtask_id INT, duration_seconds INT, grade_level VARCHAR(2)) DUPLICATE KEY(student_id, event_time) DISTRIBUTED BY HASH(student_id) BUCKETS 2 PROPERTIES("replication_num"="1")',
    'CREATE TABLE IF NOT EXISTS page_views (student_id INT, event_time DATETIME DEFAULT CURRENT_TIMESTAMP, page VARCHAR(100), duration_seconds INT) DUPLICATE KEY(student_id, event_time) DISTRIBUTED BY HASH(student_id) BUCKETS 2 PROPERTIES("replication_num"="1")',
]
for sql in tables:
    try:
        cur.execute(sql)
    except Exception as e:
        print(f'Doris warn: {str(e)[:60]}')
conn.commit()
cur.close(); conn.close()
print('Doris tables created')
print('Init complete')
