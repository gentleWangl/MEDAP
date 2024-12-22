import mysql.connector
from hashlib import sha256  # 用于密码加密
import mysql.connector
from mysql.connector import Error
from hashlib import sha256  # 用于密码加密

def get_db_connection():
    """创建数据库连接"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='1234',
            database='medap'
        )
        if conn.is_connected():
            print("连接到数据库成功")
            return conn
    except Error as e:
        print(f"无法连接到数据库: {e}")
        return None



def register_user(username, password,email, identity):
    """注册用户，并插入数据库（身份：军事迷为0，管理员为1）"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 检查用户名是否已存在
    cursor.execute("SELECT * FROM User WHERE Username = %s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False  # 用户名已存在

    # 使用sha256对密码进行加密
    password_hash = sha256(password.encode('utf-8')).hexdigest()

    # 设置身份：军事迷is_admin=0，管理员is_admin=1
    is_admin = 1 if identity == "admin" else 0

    # 插入新用户
    cursor.execute("INSERT INTO User (Username, PasswordHash,Email,is_admin) VALUES (%s, %s, %s,%s)",
                   (username, password_hash, email,is_admin))
    conn.commit()

    cursor.close()
    conn.close()
    return True  # 注册成功





def execute_query(query, params=None):
    """执行单条SQL查询"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            print("查询执行成功")
        except Error as e:
            print(f"查询执行失败: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("数据库连接失败")

def fetch_all(query, params=None):
    """查询所有结果"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"查询失败: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    else:
        print("数据库连接失败")
        return []

def delete_record(table_name, record_id):
    """删除指定表中的记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (record_id,))
    conn.commit()
    cursor.close()
    conn.close()

def update_record(table_name, record_id, new_value):
    """更新指定表中的记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET column_name = %s WHERE id = %s", (new_value, record_id))
    conn.commit()
    cursor.close()
    conn.close()

def insert_record(table_name, values):
    """向指定表插入新记录"""
    conn = get_db_connection()
    cursor = conn.cursor()
    placeholders = ", ".join(["%s"] * len(values))
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    conn.commit()
    cursor.close()
    conn.close()

def login_user(username, password, identity):
    """根据用户名和密码验证用户，并检查身份是否一致"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 使用sha256对密码进行加密
    password_hash = sha256(password.encode('utf-8')).hexdigest()

    # 查询数据库中是否有该用户
    cursor.execute("SELECT * FROM User WHERE Username = %s AND PasswordHash = %s", (username, password_hash))
    user = cursor.fetchone()

    if user:
        # 获取用户的身份 (is_admin字段)
        is_admin = user[4]  # 假设is_admin是查询结果的第五个字段（索引从0开始）

        # 根据选择的身份检查是否允许登录
        if identity == "admin" and is_admin == 1:
            cursor.close()
            conn.close()
            return 1  # 管理员可以登录
        elif identity == "military" and is_admin == 0:
            cursor.close()
            conn.close()
            return 1  # 军事迷只能以军事迷身份登录
        elif identity == "military" and is_admin == 1:
            cursor.close()
            conn.close()
            return 1  # 管理员也可以以军事迷身份登录
        else:
            cursor.close()
            conn.close()
            return -2  # 身份不匹配，不能登录
    else:
        cursor.close()
        conn.close()
        return -1  # 用户名或密码错误