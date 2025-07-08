import sqlite3
import csv

class DBManager:
    def __init__(self, db_name="user_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            if query.strip().lower().startswith("select"):
                rows = self.cursor.fetchall()
                columns = [desc[0] for desc in self.cursor.description]
                return {"status": "success", "columns": columns, "rows": rows}
            self.conn.commit()
            return {"status": "success", "message": "Query executed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def export_table_to_csv(self, table_name, file_path):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            columns = [description[0] for description in self.cursor.description]
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)
            return True, "Export successful."
        except Exception as e:
            return False, str(e)
