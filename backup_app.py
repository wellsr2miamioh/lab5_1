from flask import Flask, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
SOURCE_DB = '/nfs/demo.db'
BACKUP_DIR = '/nfs/backups'

os.makedirs(BACKUP_DIR, exist_ok=True)

@app.route('/backup', methods=['POST'])
def create_backup():
    if not os.path.exists(SOURCE_DB):
        return jsonify({"status": "error", "message": "Source DB not found"}), 404

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"demo_backup_{timestamp}.db")
        
        src = sqlite3.connect(SOURCE_DB)
        dst = sqlite3.connect(backup_path)
        with dst:
            src.backup(dst)
        src.close()
        dst.close()
        return jsonify({"status": "success", "backup": backup_path}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6000)
