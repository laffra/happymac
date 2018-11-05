import os
import process
import sqlite3
import time
import utils

DB_FILE_NAME = "activity.db"
DORMANT_PROCESS_CPU = 0.1
INIT_QUERY = """CREATE TABLE IF NOT EXISTS activities (
    timestamp float,
    system float,
    cpu float,
    name text NOT NULL,
    title text NOT NULL
)"""

def get_activity_path():
    home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    return os.path.join(home_dir, DB_FILE_NAME)

def update():
    pid = utils.get_current_app_pid()
    cpu = process.family_cpu(pid)
    if cpu < DORMANT_PROCESS_CPU:
        return
    connection = sqlite3.connect(get_activity_path())
    cursor = connection.cursor()
    cursor.execute("INSERT INTO activities (timestamp,system,cpu,name,title) VALUES(?,?,?,?,?)", [
        int(time.time()),
        process.cpu(-1),
        cpu,
        utils.get_current_app_name(),
        utils.get_active_window_name()
    ])
    connection.commit()

def get_activities():
    cursor = sqlite3.connect(get_activity_path()).cursor()
    cursor.execute("SELECT * FROM activities")
    return cursor.fetchall()

sqlite3.connect(get_activity_path()).cursor().execute(INIT_QUERY)