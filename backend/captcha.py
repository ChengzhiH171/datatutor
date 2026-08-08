"""
DataTutor 验证码模块
自绘4位数字验证码，Pillow + Redis 存储
"""
import io
import base64
import random
import uuid
import redis_client
from PIL import Image, ImageDraw


def generate_captcha():
    """生成验证码图片，返回 (captcha_id, base64_image)"""
    # 4位随机数字
    code = ''.join(random.choices('0123456789', k=4))
    captcha_id = str(uuid.uuid4())

    # 存入 Redis，5分钟过期
    r = redis_client.get_redis()
    if r:
        r.setex(f'captcha:{captcha_id}', 300, code)

    # 绘制图片
    width, height = 120, 44
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 随机背景颜色块
    for i in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(4, 12)
        y2 = y1 + random.randint(4, 12)
        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        draw.rectangle([x1, y1, x2, y2], fill=color)

    # 干扰线
    for _ in range(3):
        x1 = random.randint(0, width // 3)
        y1 = random.randint(0, height)
        x2 = random.randint(width * 2 // 3, width)
        y2 = random.randint(0, height)
        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        draw.line([x1, y1, x2, y2], fill=color, width=1)

    # 噪点
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
        draw.point((x, y), fill=color)

    # 绘制数字
    for i, ch in enumerate(code):
        x = 15 + i * 24 + random.randint(-3, 3)
        y = random.randint(4, 12)
        color = (
            random.randint(0, 80),
            random.randint(80, 160),
            random.randint(160, 220)
        )
        draw.text((x, y), ch, fill=color)

    # 输出 base64
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return captcha_id, f'data:image/png;base64,{b64}'


def verify_captcha(captcha_id, captcha_code):
    """校验验证码，成功返回 True 并删除 Redis key，失败返回 False"""
    if not captcha_id or not captcha_code:
        return False
    r = redis_client.get_redis()
    if not r:
        return False
    key = f'captcha:{captcha_id}'
    stored = r.get(key)
    if stored is None:
        return False
    stored_str = stored.decode('utf-8') if isinstance(stored, bytes) else stored
    if stored_str.lower() == captcha_code.strip().lower():
        r.delete(key)  # 一次性验证码
        return True
    return False
