import os
import shutil

def create_directories():
    """创建项目所需的所有目录"""
    dirs = [
        'static',
        'static/css',
        'static/js',
        'static/img',
        'static/img/styles',
        'static/img/avatars',  # 添加头像目录
        'static/uploads',
        'static/uploads/originals',
        'static/uploads/results',
        'static/uploads/temp',
        'database',
        'models',
        'models/pretrained',
        'templates',
        'templates/admin'
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"确保目录存在: {directory}")
    
    # 创建默认头像
    create_default_avatar()

def create_default_avatar():
    """创建默认用户头像"""
    from PIL import Image, ImageDraw
    
    # 检查默认头像是否已存在
    default_avatar_path = os.path.join('static', 'img', 'avatars', 'default.png')
    if os.path.exists(default_avatar_path):
        print(f"默认头像已存在: {default_avatar_path}")
        return
    
    # 创建简单的默认头像
    size = (200, 200)
    img = Image.new('RGB', size, color=(100, 150, 200))
    draw = ImageDraw.Draw(img)
    
    # 绘制简单的用户图标
    draw.ellipse((50, 30, 150, 130), fill=(240, 240, 240))
    draw.rectangle((75, 140, 125, 170), fill=(240, 240, 240))
    
    # 保存图像
    img.save(default_avatar_path)
    print(f"创建默认头像: {default_avatar_path}")

if __name__ == "__main__":
    create_directories()
    print("目录结构初始化完成")
