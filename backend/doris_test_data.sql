-- ============================================================
-- DataTutor 学情分析 — 测试数据（成员E）
-- 在 Doris 中执行此脚本插入测试数据
-- ============================================================

USE datatutor_analytics;

-- terminal_events: 模拟 5 个学生的终端操作
INSERT INTO terminal_events (student_id, course_id, subtask_id, vm_name, data, direction) VALUES
(1, 101, 1, 'vm-python-01', 'ls -la', 'input'),
(1, 101, 1, 'vm-python-01', 'total 24\ndrwxr-xr-x 3 hadoop hadoop 4096 Aug 4 16:30 .', 'output'),
(1, 101, 2, 'vm-python-01', 'python hello.py', 'input'),
(1, 101, 2, 'vm-python-01', 'Hello, World!', 'output'),
(1, 101, 3, 'vm-python-01', 'pip install pandas', 'input'),
(1, 101, 3, 'vm-python-01', 'Successfully installed pandas', 'output'),
(2, 101, 1, 'vm-python-02', 'mkdir project', 'input'),
(2, 101, 1, 'vm-python-02', '', 'output'),
(2, 101, 2, 'vm-python-02', 'cat data.csv', 'input'),
(2, 101, 2, 'vm-python-02', 'id,name,score', 'output'),
(2, 101, 3, 'vm-python-02', 'python analyze.py', 'input'),
(3, 101, 1, 'vm-python-03', 'git clone repo', 'input'),
(3, 101, 1, 'vm-python-03', 'Cloning into repo...', 'output'),
(3, 101, 2, 'vm-python-03', 'cd repo && ls', 'input'),
(3, 101, 2, 'vm-python-03', 'README.md src/', 'output'),
(3, 101, 3, 'vm-python-03', 'python main.py', 'input'),
(3, 101, 3, 'vm-python-03', 'Training complete', 'output'),
(3, 101, 4, 'vm-python-03', 'python test.py', 'input'),
(4, 101, 1, 'vm-python-04', 'echo hello', 'input'),
(4, 101, 1, 'vm-python-04', 'hello', 'output'),
(4, 101, 2, 'vm-python-04', 'python train.py', 'input'),
(5, 101, 1, 'vm-python-05', 'jupyter notebook', 'input'),
(5, 101, 1, 'vm-python-05', 'Serving notebooks from local directory', 'output'),
(5, 101, 2, 'vm-python-05', 'import pandas as pd', 'input'),
(5, 101, 3, 'vm-python-05', 'df = pd.read_csv("data.csv")', 'input'),
(5, 101, 3, 'vm-python-05', 'DataFrame with 100 rows', 'output');

-- chat_events: 模拟 AI 对话
INSERT INTO chat_events (student_id, course_id, subtask_id, msg_role, msg_length) VALUES
(1, 101, 1, 'user', 45),
(1, 101, 1, 'assistant', 320),
(1, 101, 2, 'user', 80),
(1, 101, 2, 'assistant', 500),
(1, 101, 3, 'user', 30),
(2, 101, 1, 'user', 60),
(2, 101, 1, 'assistant', 280),
(2, 101, 2, 'user', 100),
(2, 101, 2, 'assistant', 450),
(3, 101, 1, 'user', 55),
(3, 101, 1, 'assistant', 300),
(3, 101, 2, 'user', 70),
(3, 101, 2, 'assistant', 400),
(3, 101, 3, 'user', 90),
(3, 101, 3, 'assistant', 600),
(3, 101, 4, 'user', 40),
(4, 101, 1, 'user', 50),
(4, 101, 1, 'assistant', 200),
(4, 101, 2, 'user', 65),
(5, 101, 1, 'user', 75),
(5, 101, 1, 'assistant', 350),
(5, 101, 2, 'user', 85),
(5, 101, 3, 'user', 95),
(5, 101, 3, 'assistant', 550);

-- task_completions: 模拟任务完成
INSERT INTO task_completions (student_id, course_id, subtask_id, duration_seconds, grade_level) VALUES
(1, 101, 1, 600, 'A'),
(1, 101, 2, 900, 'A'),
(1, 101, 3, 1200, 'B'),
(2, 101, 1, 450, 'B'),
(2, 101, 2, 720, 'A'),
(2, 101, 3, 1500, 'C'),
(3, 101, 1, 300, 'A'),
(3, 101, 2, 600, 'A'),
(3, 101, 3, 800, 'B'),
(3, 101, 4, 1000, 'A'),
(4, 101, 1, 1800, 'C'),
(4, 101, 2, 2400, 'B'),
(5, 101, 1, 500, 'B'),
(5, 101, 2, 700, 'A'),
(5, 101, 3, 1100, 'B');

-- page_views: 模拟页面访问
INSERT INTO page_views (student_id, page, duration_seconds) VALUES
(1, 'hub.html', 300),
(1, 'terminal.html', 600),
(1, 'chat.html', 400),
(2, 'hub.html', 200),
(2, 'terminal.html', 450),
(3, 'hub.html', 150),
(3, 'terminal.html', 800),
(3, 'chat.html', 500),
(4, 'hub.html', 100),
(5, 'hub.html', 250),
(5, 'terminal.html', 700);

-- 验证
SELECT 'terminal_events' AS tbl, COUNT(*) AS cnt FROM terminal_events
UNION ALL SELECT 'chat_events', COUNT(*) FROM chat_events
UNION ALL SELECT 'task_completions', COUNT(*) FROM task_completions
UNION ALL SELECT 'page_views', COUNT(*) FROM page_views;
