import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database configuration
'''DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'task_management'
}'''

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Thanhdat1311!',
    'database': 'task_management',
    'auth_plugin': 'mysql_native_password'
}

DB_CONFIG_NEW = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Thanhdat1311!',
    'auth_plugin': 'mysql_native_password'
}

class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except (Error, Exception) as error:
            print(error)
            return None

    def create_database(self, db_name):
        try:
            config_copy = self.config.copy()
            config_copy.pop('database', None)  # Remove the 'database' key if it exists
            cnt = mysql.connector.connect(**config_copy)
            cur = cnt.cursor()
            cur.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')
            cnt.commit()
            print(f"Database '{db_name}' created or already exists.")
        except (Error, Exception) as error:
            print(error)
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

class TaskTable(Database):
    def __init__(self, config, table_name='task_mng'):
        super().__init__(config)
        self.table_name = table_name

    def create_table(self):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor()
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                            id INT NOT NULL AUTO_INCREMENT,
                            title VARCHAR(500) NOT NULL,
                            category VARCHAR(100),
                            description TEXT,
                            add_date DATE,
                            due_date DATE,
                            finished_date DATE,
                            completed BOOL,
                            PRIMARY KEY (id)
                            );""")
            cnt.commit()
            print(f"Table '{self.table_name}' created or already exists.")
        except (Error, Exception) as error:
            print(error)
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def add_task(self, title, category, description, due_date):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor()
            cur.execute(f"""
                        INSERT INTO {self.table_name}(title, category, description, due_date)
                        VALUES (%s, %s, %s, %s)
                        """,(title, category, description, due_date))
            task_id = cur.lastrowid
            cnt.commit()
            return task_id
        except (Error, Exception) as error:
            print(error)
            return None
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def get_task(self, task_id):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor(dictionary=True)
            cur.execute(f"""
                        SELECT * FROM {self.table_name}
                        WHERE id = %s
                        """,(task_id,))
            row = cur.fetchone()
            if row:
                for date_field in ['add_date', 'due_date', 'finished_date']:
                    if row[date_field]:
                        row[date_field] = row[date_field].strftime("%Y-%m-%d")
            else:
                print(f'Task ID {task_id} not found.')
            return row
        except (Error, Exception) as error:
            print(error)
            return None
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def update_task(self, task_id, updates):
        cnt = self.create_connection()
        
        values = []
        str_exe = ''
        i = 0
        for k, v in updates.items():
            if i>0:
                str_exe += ', ' 
            str_exe += k + ' = ' + '%s'
            values.append(v)
            i += 1

        values.append(task_id)
        sql = f'update {self.table_name} set {str_exe} where id = %s'
        
        try:
            cur = cnt.cursor()
            cur.execute(sql, tuple(values))
            cnt.commit()
        except (Error, Exception) as error:
            print(error)
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def delete_task(self, task_id):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor()
            cur.execute(f"""
                        SELECT * FROM {self.table_name}
                        WHERE id = %s
                        """,(task_id,))
            row = cur.fetchone()
            if row:
                cur.execute(f"""
                            DELETE FROM {self.table_name}
                            WHERE id = %s
                            """,(task_id,))
                cnt.commit()
                return task_id
            else:
                print(f'Task ID {task_id} not found.')
                return None
        except (Error, Exception) as error:
            print(error)
            return None
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def list_all_tasks(self):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor(dictionary=True)
            cur.execute(f"SELECT * FROM {self.table_name}")
            rows = cur.fetchall()
            for row in rows:
                for date_field in ['add_date', 'due_date', 'finished_date']:
                    if row[date_field]:
                        row[date_field] = row[date_field].strftime("%Y-%m-%d")
            return rows if rows else "There's no task in the management system."
        except (Error, Exception) as error:
            print(error)
            return None
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

    def search_tasks(self, keyword):
        cnt = self.create_connection()
        try:
            cur = cnt.cursor(dictionary=True)
            cur.execute(f"""
                        SELECT * FROM {self.table_name}
                        WHERE title REGEXP %s OR description REGEXP %s
                        """, (keyword, keyword))
            rows = cur.fetchall()
            for row in rows:
                for date_field in ['add_date', 'due_date', 'finished_date']:
                    if row[date_field]:
                        row[date_field] = row[date_field].strftime("%Y-%m-%d")
            return rows if rows else f'No tasks found with the keyword "{keyword}".'
        except (Error, Exception) as error:
            print(error)
            return None
        finally:
            if cur:
                cur.close()
            if cnt:
                cnt.close()

db = Database(DB_CONFIG)
db.create_database('task_management')

task_table = TaskTable(DB_CONFIG)
task_table.create_table()

# Example usage
if __name__ == "__main__":
    # Add a task
    task_id = task_table.add_task("Complete MySQL integration", "Work", "Integrate MySQL database into the task management system", "2023-08-15")
    print(f"Added task with ID: {task_id}")

    # Get a task
    task = task_table.get_task(task_id)
    print(f"Retrieved task: {task}")

    # Update a task
    task_table.update_task(task_id, {"completed": True, "finished_date": datetime.now().strftime("%Y-%m-%d")})
    print("Updated task")

    # List all tasks
    all_tasks = task_table.list_all_tasks()
    print(f"All tasks: {all_tasks}")

    # Search tasks
    search_results = task_table.search_tasks("MySQL")
    print(f"Search results: {search_results}")

    # Delete a task
    task_table.delete_task(task_id)
    print(f"Deleted task with ID: {task_id}")
