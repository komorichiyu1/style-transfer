import os
import sys
import sqlite3

def create_project_directories():
    """创建项目所需的所有目录"""
    directories = [
        'database',
        'static/css',
        'static/js',
        'static/img',
        'static/img/styles',
        'static/img/icons',
        'static/uploads',
        'static/uploads/originals',
        'static/uploads/results',
        'static/uploads/comparisons',
        'static/uploads/temp',
        'models',
        'models/pretrained',
        'templates',
        'templates/admin'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def create_simple_style_preview(style_name, output_path, size=(300, 300)):
    """创建简单的风格预览图像，不使用复杂的字体功能"""
    from PIL import Image, ImageDraw
    # 创建彩色背景
    import random
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    img = Image.new('RGB', size, color=(r, g, b))
    
    # 保存图像
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Created style preview for {style_name} at {output_path}")
    
    return output_path

def create_all_style_previews():
    """创建所有风格预览图像"""
    styles = {
        'vangogh': '梵高星空',
        'picasso': '毕加索立体派',
        'ink': '水墨画',
        'impression': '印象派',
        'pop': '波普艺术'
    }
    
    for style_id, style_name in styles.items():
        output_path = os.path.join('static', 'img', 'styles', f'{style_id}.jpg')
        create_simple_style_preview(style_name, output_path)

def init_db():
    """初始化数据库"""
    # 确保数据库目录存在
    os.makedirs('database', exist_ok=True)
    
    try:
        conn = sqlite3.connect('database/portrait.db')
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建上传历史表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_image TEXT NOT NULL,
            upload_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建处理结果表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_image TEXT NOT NULL,
            result_image TEXT NOT NULL,
            styles TEXT NOT NULL,
            parameters TEXT,
            create_date TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 创建风格模型表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS styles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            preview_image TEXT,
            model_path TEXT NOT NULL
        )
        ''')
        
        # 检查是否有管理员账户，如果没有则创建一个默认管理员
        admin = cursor.execute('SELECT * FROM users WHERE is_admin = 1').fetchone()
        if not admin:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123')
            cursor.execute('INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)',
                         ('admin', 'admin@example.com', hashed_password, 1))
        
        # 添加一些预设风格
        styles = [
            ('梵高星空', '梵高的星空风格，充满漩涡状的笔触和强烈的色彩对比', 'vangogh.jpg', 'vangogh.pth'),
            ('毕加索立体派', '毕加索的立体派风格，打破传统透视，呈现多角度视图', 'picasso.jpg', 'picasso.pth'),
            ('水墨画', '中国传统水墨画风格，强调线条和墨色变化', 'ink.jpg', 'ink.pth'),
            ('印象派', '印象派风格，注重光影效果和色彩表现', 'impression.jpg', 'impression.pth'),
            ('波普艺术', '波普艺术风格，融合流行文化元素和鲜艳色彩', 'pop.jpg', 'pop.pth'),
        ]
        
        for style in styles:
            existing = cursor.execute('SELECT * FROM styles WHERE name = ?', (style[0],)).fetchone()
            if not existing:
                cursor.execute('INSERT INTO styles (name, description, preview_image, model_path) VALUES (?, ?, ?, ?)', style)
        
        conn.commit()
        conn.close()
        print("数据库初始化完成")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        raise e

def create_model_placeholders():
    """创建模型占位文件"""
    pretrained_models = {
        'vangogh': 'models/pretrained/vangogh.pth',
        'picasso': 'models/pretrained/picasso.pth',
        'ink': 'models/pretrained/ink.pth',
        'impression': 'models/pretrained/impression.pth',
        'pop': 'models/pretrained/pop.pth'
    }
    
    # 创建预训练模型目录
    os.makedirs('models/pretrained', exist_ok=True)
    
    # 由于实际模型文件较大，这里仅作为演示，实际应用中需要下载预训练模型
    for model_name, model_path in pretrained_models.items():
        if not os.path.exists(model_path):
            # 创建空文件作为占位符
            with open(model_path, 'w') as f:
                f.write(f"Placeholder for {model_name} model")
            print(f"Created placeholder model file for {model_name}")

def initialize_project():
    """初始化项目，创建必要的目录和文件"""
    print("初始化项目...")
    
    try:
        # 创建目录结构
        create_project_directories()
        
        # 创建风格预览图像
        create_all_style_previews()
        
        # 初始化数据库
        init_db()
        
        # 创建模型占位文件
        create_model_placeholders()
        
        print("项目初始化完成")
    except Exception as e:
        print(f"项目初始化失败: {e}")
        sys.exit(1)

def run_app():
    """运行Flask应用"""
    try:
        from app import app
        app.run(debug=True)
    except ImportError:
        print("无法导入Flask应用，请确保app.py文件存在")
        sys.exit(1)
    except Exception as e:
        print(f"运行应用失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 初始化项目
    initialize_project()
    
    # 运行Flask应用
    run_app()
