import os
import sqlite3
import pymysql
from datetime import datetime
try:
    from config.db_config import DB_CONFIG
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

def migrate_sqlite_to_mysql():
    """将SQLite数据库中的数据迁移到MySQL数据库"""
    print("==== 开始从SQLite到MySQL的数据迁移 ====")
    
    # 检查SQLite数据库文件是否存在
    sqlite_db_path = 'database/portrait.db'
    if not os.path.exists(sqlite_db_path):
        print(f"SQLite数据库文件 {sqlite_db_path} 不存在，无法进行迁移")
        return False
    
    try:
        # 连接SQLite数据库
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_conn.row_factory = sqlite3.Row
        
        # 获取表结构信息 - 在迁移前检查
        print("检查SQLite数据库表结构...")
        tables = sqlite_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print(f"找到 {len(tables)} 个表:", [t[0] for t in tables])
        
        # 检查users表结构
        if 'users' in [t[0] for t in tables]:
            columns = sqlite_conn.execute("PRAGMA table_info(users)").fetchall()
            print("Users表的列名:", [col[1] for col in columns])
        
        # 检查用户记录
        user_count = sqlite_conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        print(f"用户表记录数: {user_count}")
        
        if not HAS_CONFIG:
            print("找不到MySQL配置，请先运行setup_mysql_db.py")
            return False
        
        # 连接MySQL数据库
        mysql_conn = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            db=DB_CONFIG['db'],
            charset=DB_CONFIG['charset']
        )
        mysql_cursor = mysql_conn.cursor()
        
        # 迁移users表
        print("迁移users表...")
        sqlite_users = sqlite_conn.execute("SELECT * FROM users").fetchall()
        for user in sqlite_users:
            # 将SQLite行转换为字典
            user_dict = dict(user)
            print(f"正在处理用户: {user_dict}")
            
            # 确定注册日期字段 - 适应不同的字段名
            register_date = None
            for date_field in ['register_date', 'created_at', 'date_joined', 'created']:
                if date_field in user_dict and user_dict[date_field]:
                    register_date = user_dict[date_field]
                    break
            
            if not register_date:
                register_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 插入到MySQL
            mysql_cursor.execute('''
                INSERT INTO users 
                (id, username, email, password, is_admin, is_active, register_date, avatar)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                username=VALUES(username), 
                email=VALUES(email),
                password=VALUES(password),
                is_admin=VALUES(is_admin),
                is_active=VALUES(is_active),
                register_date=VALUES(register_date),
                avatar=VALUES(avatar)
            ''', (
                user_dict['id'],
                user_dict['username'],
                user_dict['email'],
                user_dict['password'],
                user_dict['is_admin'],
                user_dict['is_active'],
                register_date,
                user_dict.get('avatar')
            ))
        print(f"已迁移 {len(sqlite_users)} 个用户记录")
        
        # 迁移user_uploads表
        print("迁移user_uploads表...")
        try:
            sqlite_uploads = sqlite_conn.execute("SELECT * FROM user_uploads").fetchall()
            for upload in sqlite_uploads:
                upload_dict = dict(upload)
                
                # 确定上传日期字段
                upload_date = None
                for date_field in ['upload_date', 'created_at', 'date']:
                    if date_field in upload_dict and upload_dict[date_field]:
                        upload_date = upload_dict[date_field]
                        break
                
                if not upload_date:
                    upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                mysql_cursor.execute('''
                    INSERT INTO user_uploads
                    (id, user_id, original_image, upload_date)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    user_id=VALUES(user_id),
                    original_image=VALUES(original_image),
                    upload_date=VALUES(upload_date)
                ''', (
                    upload_dict['id'],
                    upload_dict['user_id'],
                    upload_dict['original_image'],
                    upload_date
                ))
            print(f"已迁移 {len(sqlite_uploads)} 个上传记录")
        except Exception as e:
            print(f"迁移user_uploads表时出错: {e}")
        
        # 迁移user_results表
        print("迁移user_results表...")
        try:
            sqlite_results = sqlite_conn.execute("SELECT * FROM user_results").fetchall()
            for result in sqlite_results:
                result_dict = dict(result)
                
                # 确定创建日期字段
                create_date = None
                for date_field in ['create_date', 'created_at', 'date']:
                    if date_field in result_dict and result_dict[date_field]:
                        create_date = result_dict[date_field]
                        break
                
                if not create_date:
                    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                mysql_cursor.execute('''
                    INSERT INTO user_results
                    (id, user_id, original_image, result_image, styles, parameters, create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    user_id=VALUES(user_id),
                    original_image=VALUES(original_image),
                    result_image=VALUES(result_image),
                    styles=VALUES(styles),
                    parameters=VALUES(parameters),
                    create_date=VALUES(create_date)
                ''', (
                    result_dict['id'],
                    result_dict['user_id'],
                    result_dict['original_image'],
                    result_dict['result_image'],
                    result_dict['styles'],
                    result_dict.get('parameters', ''),
                    create_date
                ))
            print(f"已迁移 {len(sqlite_results)} 条处理结果记录")
        except Exception as e:
            print(f"迁移user_results表时出错: {e}")
        
        # 迁移styles表
        print("迁移styles表...")
        try:
            sqlite_styles = sqlite_conn.execute("SELECT * FROM styles").fetchall()
            for style in sqlite_styles:
                style_dict = dict(style)
                
                # 确定创建日期字段
                created_at = None
                for date_field in ['created_at', 'create_date', 'date']:
                    if date_field in style_dict and style_dict[date_field]:
                        created_at = style_dict[date_field]
                        break
                
                if not created_at:
                    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                mysql_cursor.execute('''
                    INSERT INTO styles
                    (id, name, description, preview_image, model_path, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    description=VALUES(description),
                    preview_image=VALUES(preview_image),
                    model_path=VALUES(model_path),
                    created_at=VALUES(created_at)
                ''', (
                    style_dict['id'],
                    style_dict['name'],
                    style_dict.get('description', ''),
                    style_dict.get('preview_image', ''),
                    style_dict.get('model_path', ''),
                    created_at
                ))
            print(f"已迁移 {len(sqlite_styles)} 个风格模型记录")
        except Exception as e:
            print(f"迁移styles表时出错: {e}")
        
        # 提交所有更改
        mysql_conn.commit()
        
        print("数据迁移完成!")
        return True
        
    except Exception as e:
        print(f"数据迁移失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 关闭连接
        if 'sqlite_conn' in locals():
            sqlite_conn.close()
        
        if 'mysql_conn' in locals() and 'mysql_cursor' in locals():
            mysql_cursor.close()
            mysql_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_mysql()