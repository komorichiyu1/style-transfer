import os
from init_dirs import create_directories
from app import app, init_db

if __name__ == '__main__':
    # 创建必要的目录
    create_directories()
    
    # 初始化数据库
    init_db()
    
    # 运行Flask应用
    print("启动Flask应用...")
    app.run(debug=True, host='0.0.0.0', port=5000)