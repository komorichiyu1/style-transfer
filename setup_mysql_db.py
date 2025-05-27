import pymysql
import os
import getpass


def setup_mysql_database():
    """设置MySQL数据库并创建所需的表"""
    print("==== MySQL数据库初始化 ====")

    # 获取数据库连接信息
    host = input("MySQL主机 (默认: localhost): ") or "localhost"
    port = int(input("MySQL端口 (默认: 3306): ") or "3306")
    user = input("MySQL用户名 (默认: root): ") or "root"
    password = getpass.getpass("MySQL密码: ")

    db_name = input("数据库名称 (默认: portrait_db): ") or "portrait_db"

    # 首先创建数据库
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"数据库 '{db_name}' 创建成功或已存在")

        # 切换到新创建的数据库
        cursor.execute(f"USE {db_name}")

        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_admin TINYINT DEFAULT 0,
            is_active TINYINT DEFAULT 1,
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            avatar VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # 创建上传历史表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_uploads (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            original_image VARCHAR(255) NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # 创建处理结果表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            original_image VARCHAR(255) NOT NULL,
            result_image VARCHAR(255) NOT NULL,
            styles VARCHAR(255) NOT NULL,
            parameters TEXT,
            create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # 创建风格模型表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS styles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            preview_image VARCHAR(255),
            model_path VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')

        # 检查是否有管理员账户，如果没有则创建一个默认管理员
        cursor.execute("SELECT * FROM users WHERE is_admin = 1")
        admin = cursor.fetchone()

        if not admin:
            # 创建默认管理员账户
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123', method='pbkdf2:sha256')
            cursor.execute('''
                INSERT INTO users (username, email, password, is_admin, is_active)
                VALUES (%s, %s, %s, %s, %s)
            ''', ('admin', 'admin@example.com', hashed_password, 1, 1))
            print("已创建默认管理员账户 (用户名: admin, 密码: admin123)")

        conn.commit()

        # 保存MySQL配置
        save_config(host, port, user, password, db_name)

        print("数据库表创建成功")
        print("MySQL配置已保存")

        return True

    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()


def save_config(host, port, user, password, db_name):
    """保存MySQL配置到配置文件"""
    config_dir = "config"
    os.makedirs(config_dir, exist_ok=True)

    config_path = os.path.join(config_dir, "db_config.py")
    with open(config_path, 'w') as f:
        f.write(f"""# MySQL数据库配置
DB_CONFIG = {{
    'host': '{host}',
    'port': {port},
    'user': '{user}',
    'password': '{password}',
    'db': '{db_name}',
    'charset': 'utf8mb4'
}}
""")


if __name__ == "__main__":
    setup_mysql_database()