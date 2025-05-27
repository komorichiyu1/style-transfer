import os

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
        'models',
        'models/pretrained',
        'templates',
        'templates/admin'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

if __name__ == "__main__":
    create_project_directories()
