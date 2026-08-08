"""学习进度路由 — 完整实现"""
from flask import Blueprint, request, jsonify
from database import db
from models import TaskProgress
from datetime import datetime
from routes.auth import token_required

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/<int:course_id>', methods=['GET'])
@token_required
def get_progress(current_user, course_id):
    """获取当前学生在某课程的进度"""
    from models import Subtask
    subtasks = Subtask.query.filter_by(course_id=course_id).order_by(Subtask.order_index).all()
    total = len(subtasks)

    # 查询所有子任务的状态
    all_progress = TaskProgress.query.filter(
        TaskProgress.student_id == current_user.id,
        TaskProgress.subtask_id.in_([s.id for s in subtasks])
    ).all()
    progress_map = {p.subtask_id: p.status for p in all_progress}

    # 构建 subtask_statuses: {id: 'pending'|'in_progress'|'completed'}
    subtask_statuses = {}
    completed = 0
    current_idx = 0
    for i, st in enumerate(subtasks):
        status = progress_map.get(st.id, 'pending')
        subtask_statuses[str(st.id)] = status
        if status == 'completed':
            completed += 1
        elif status == 'in_progress' and current_idx == 0:
            current_idx = i

    # 如果没有进行中的，指向第一个未完成的
    if current_idx == 0:
        for i, st in enumerate(subtasks):
            if progress_map.get(st.id, 'pending') != 'completed':
                current_idx = i
                break

    return jsonify({
        'completed': completed,
        'total': total,
        'subtask_statuses': subtask_statuses,
        'current_subtask_index': current_idx
    })


@progress_bp.route('/start', methods=['POST'])
@token_required
def start_subtask(current_user):
    """开始一个子任务"""
    data = request.get_json()
    existing = TaskProgress.query.filter_by(
        student_id=current_user.id,
        subtask_id=data['subtask_id']
    ).first()
    if existing:
        existing.started_at = datetime.utcnow()
        existing.status = 'in_progress'
    else:
        tp = TaskProgress(
            student_id=current_user.id,
            subtask_id=data['subtask_id'],
            status='in_progress',
            started_at=datetime.utcnow(),
        )
        db.session.add(tp)
    db.session.commit()
    return jsonify({'message': '已开始'})


@progress_bp.route('/complete', methods=['POST'])
@token_required
def complete_subtask(current_user):
    """完成一个子任务"""
    data = request.get_json()
    tp = TaskProgress.query.filter_by(
        student_id=current_user.id,
        subtask_id=data['subtask_id']
    ).first()
    if tp:
        tp.status = 'completed'
        tp.completed_at = datetime.utcnow()
    else:
        tp = TaskProgress(
            student_id=current_user.id,
            subtask_id=data['subtask_id'],
            status='completed',
            completed_at=datetime.utcnow(),
        )
        db.session.add(tp)
    db.session.commit()
    return jsonify({'message': '已完成'})


@progress_bp.route('/training_time', methods=['GET'])
@token_required
def get_training_time(current_user):
    """获取学生的总实训时长（秒）和当前会话起始时间"""
    from models import Subtask
    records = TaskProgress.query.filter_by(student_id=current_user.id).all()
    total_seconds = 0
    current_started_at = None
    for r in records:
        if r.started_at and r.completed_at:
            delta = (r.completed_at - r.started_at).total_seconds()
            total_seconds += max(0, int(delta))
        if r.status == 'in_progress' and r.started_at:
            current_started_at = r.started_at.isoformat()
            elapsed = (datetime.utcnow() - r.started_at).total_seconds()
            total_seconds += max(0, int(elapsed))
    return jsonify({
        'total_seconds': total_seconds,
        'current_started_at': current_started_at
    })


@progress_bp.route('/terminal_context', methods=['GET'])
@token_required
def get_terminal_context_route(current_user):
    """获取学生终端上下文（供工作流代码节点调用）"""
    from terminal_ws.terminal import get_terminal_context
    ctx = get_terminal_context(current_user.id)
    return jsonify({'context': ctx})
