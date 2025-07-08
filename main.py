from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import csv
import io
from utils.ai_helper import get_query_suggestion

app = Flask(__name__)
DB_PATH = 'database.db'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/execute", methods=["POST"])
def execute():
    query = request.json.get("query", "")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description] if cursor.description else []
        return jsonify({"status": "success", "columns": col_names, "rows": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/suggest", methods=["POST"])
def suggest():
    query = request.json.get("query", "")
    suggestion = get_query_suggestion(query)
    return jsonify({"suggestion": suggestion})

@app.route("/export_csv", methods=["POST"])
def export_csv():
    data = request.json
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(data["columns"])
    writer.writerows(data["rows"])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="result.csv")

if __name__ == "__main__":
    app.run(debug=True)
