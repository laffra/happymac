import datetime
import os
import process
import sqlite3
import time
import utils
import webbrowser

DB_FILE_NAME = "activity.db"
DORMANT_PROCESS_CPU = 0.1
INIT_QUERY = """CREATE TABLE IF NOT EXISTS activities (
    timestamp float,
    system float,
    cpu float,
    name text NOT NULL,
    title text NOT NULL
)"""

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")

def get_activity_path():
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    return os.path.join(home_dir, DB_FILE_NAME)

def get_report_path():
    reports_dir = os.path.join(home_dir, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return os.path.join(home_dir, "report_%s.html" % datetime.datetime.utcnow())

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

def generate_report():
    filename = get_report_path()
    with open(filename, "w") as output:
        output.write("<table border=1>")
        output.write("<tr><th>When</th><th>CPU</th><th>APP CPU</th><th>APP NAME</th><th>Window/Tab Title</td></tr>")
        for timestamp, cpu, app_cpu, app_name, window_title in get_activities():
            output.write("""
              <tr>
              <td>%s</td>
              <td>%d%%</td>
              <td>%d%%</td>
              <td>%s</td>
              <td>%s</td>
              </tr>
            """ % (
                datetime.datetime.fromtimestamp(timestamp),
                int(cpu * 100),
                int(app_cpu * 100),
                app_name.encode('ascii','ignore'),
                window_title.encode('ascii','ignore'),
            ))
        output.write("</table>")
    webbrowser.open("file://%s" % filename)


sqlite3.connect(get_activity_path()).cursor().execute(INIT_QUERY)