import collections
import datetime
import error
import log
import os
import process
import re
import sqlite3
import time
import utils
import webbrowser

DB_FILE_NAME = "activities.db"
DORMANT_PROCESS_CPU = 0.1
INIT_QUERY = """CREATE TABLE IF NOT EXISTS activities (
    timestamp float,
    system float,
    cpu float,
    email text,
    location text,
    pid text,
    ppid text,
    name text,
    title text,
    url text,
    fav text
)"""
INDEX_EMAIL = 3
INDEX_TITLE = 8
HOUR_IN_MS = 3600 * 1000000

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")
title_details = {}

def get_activity_path():
    if not os.path.exists(home_dir):
        os.makedirs(home_dir)
    return os.path.join(home_dir, DB_FILE_NAME)

def get_report_path():
    reports_dir = os.path.join(home_dir, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    return os.path.join(reports_dir, "report_%s.html" % datetime.datetime.utcnow())

def update_tab(email, url, fav, title):
    connection = sqlite3.connect(get_activity_path())
    cursor = connection.cursor()
    cursor.execute('''
            UPDATE activities SET email = "%s", url = "%s", fav = "%s"
            WHERE  email = "no@email" AND title = "%s" AND name = "Google Chrome"
        ''' % (email, url, fav, title)
    )
    connection.commit()
    title_details[title] = (url, fav)
    log.log("New tab: %s %s %s" % (email, url, title))
    for row in cursor.execute('SELECT * FROM activities WHERE  title = "%s" AND name = "Google Chrome"' % title).fetchall():
        print row[INDEX_EMAIL], row[INDEX_TITLE]

def update_activities():
    pid = utils.get_current_app_pid()
    cpu = process.family_cpu_usage(pid)
    if cpu < DORMANT_PROCESS_CPU:
        return
    connection = sqlite3.connect(get_activity_path())
    cursor = connection.cursor()
    title = utils.get_active_window_name()
    app_name = utils.get_current_app_name()
    url = get_url('', app_name, title)
    cursor.execute("""
            INSERT INTO activities (timestamp,system,cpu,email,location,pid,ppid,name,title,url)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, [
        int(time.time()),
        process.cpu(-1),
        cpu,
        "no@email",
        process.location(pid),
        pid,
        process.parent_pid(pid),
        app_name,
        title,
        url
    ])
    connection.commit()

def get_activities():
    cursor = sqlite3.connect(get_activity_path()).cursor()
    return cursor.execute("SELECT * FROM activities").fetchall()

def generate_report():
    try:
        filename = get_report_path()
        activities = get_activities()
        log.log("Generate report with %d events in file %s" % (len(activities), filename))
        emails = list(set(row[INDEX_EMAIL] for row in activities))
        with open(filename, "w") as output:
            generate_header(output, emails)
            generate_summary_pie_chart(output, emails, activities)
            for email in reversed(sorted(emails)):
                generate_pie_chart(output, email, [activity for activity in activities if activity[INDEX_EMAIL] == email])
            generate_full_table(output, activities)
            generate_footer(output)
        webbrowser.open("file://%s" % filename)
    except:
        error.error("Cannot generate report")

def generate_header(output, emails):
    charts = """
        <div style="text-align: center; border: 2px solid grey; margin:20px; width:1100px;">
            <h2>Summary</h2>
            <canvas id="chart-area-summary"></canvas>
        </div>
        """ + "\n".join([
            """
            <div style="text-align: center; border: 2px solid grey; margin:20px; width:1100px">
                <h2 id="chart-header-%(email)s">%(email)s</h2>
                <canvas id="chart-area-%(email)s"></canvas>
            </div>
            """ % { "email": email or "no email" }
            for email in emails
        ])
    output.write("""
        <html>
            <head>
                <title>HappyMac Report</title>
                <script src="https://www.chartjs.org/dist/2.7.3/Chart.bundle.js"></script>
                <script src="https://www.chartjs.org/samples/latest/utils.js"></script>
            </head>
            <body>
                <div id="canvas-holder">
                    %s
                </div>
    """ % charts)

def generate_footer(output):
    output.write("""
            </body>
        </html>
    """)

def generate_summary_pie_chart(output, emails, activities):
    data = [
        len([row for row in activities if row[INDEX_EMAIL] == email])
        for email in emails
    ]
    emails = [email.encode('utf8') for email in emails]
    log.log("Generate summary pie chart %s, %s" % (data, emails))
    output.write("""
        <script>
        var colors = [
            window.chartColors.red,
            window.chartColors.blue,
            window.chartColors.green,
            window.chartColors.orange,
            window.chartColors.yellow,
        ];
        new Chart(document.getElementById('chart-area-summary').getContext('2d'), {
			type: 'pie',
			data: {
				datasets: [{
					data: %(data)s,
					backgroundColor: colors,
					label: 'Time Spent Well'
				}],
				labels: %(labels)s,
			},
			options: {
				responsive: true
			}
		});
        console.log("Generate summary pie chart", %(data)s, %(labels)s);
        </script>
    """ % {"data": data, "labels": emails})

def generate_pie_chart(output, pie_email, activities):
    log.log("Generate pie chart for %d rows for email '%s'" % (len(activities), pie_email))
    counts = collections.defaultdict(int)

    for timestamp, cpu, app_cpu, email, location, pid, ppid, app_name, title, url, fav in activities:
        counts[url or "%s + %s" % (app_name, title)] += 1

    labels = repr([title.encode("utf8")[:32] for title in counts.keys()])
    data = list(counts.values())
    id = (pie_email or "@no_email").split("@")[1].replace(".", "_")
    output.write("""
        <script>
        var colors = [
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
            window.chartColors.red, window.chartColors.orange, window.chartColors.yellow, window.chartColors.green, window.chartColors.blue,
        ];
		var config_%(id)s = {
			type: 'pie',
			data: {
				datasets: [{
					data: %(data)s,
					backgroundColor: colors,
					label: 'Time Spent Well'
				}],
				labels: %(labels)s,
			},
			options: {
				responsive: true
			}
		};
        setTimeout(function() {
            new Chart(document.getElementById('chart-area-%(email)s').getContext('2d'), config_%(id)s);
            document.getElementById('chart-header-%(email)s').textContent = "%(email)s - %(size)d samples recorded";
        }, 1500);
        </script>
    """ % {"data": repr(data), "size": len(data), "id": id, "email": pie_email or "no email", "labels": labels})

def get_fav(fav, app_name, title):
    if app_name != "Google Chrome":
        return fav
    title = title.encode('ascii', 'ignore')
    return (fav or title_details.get(title, ('',''))[1]).encode("ascii", "ignore")

def get_url(url, app_name, title):
    if app_name != "Google Chrome":
        return url
    title = title.encode('ascii', 'ignore')
    return (url or title_details.get(title, ('',''))[0]).encode("ascii", "ignore")

def generate_full_table(output, activities):
    output.write("<h1>All Events</h1><table border=1 width=\"1400px\">")
    output.write("""
        <tr>
            <th>When</th>
            <th>CPU</th>
            <th>APP CPU</th>
            <th>Email</th>
            <th>PID</th>
            <th>Parent PID</th>
            <th>Location</th>
            <th>APP NAME</th>
            <th>Window/Tab Title</td>
            <th>Url</th>
            <th>FavIcon</th>
        </tr>""")

    for timestamp, cpu, app_cpu, email, location, pid, ppid, app_name, title, url, fav in activities:
        output.write(u"""
        <tr>
        <td>%s</td>
        <td>%d%%</td>
        <td>%d%%</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        """ % (
            datetime.datetime.fromtimestamp(timestamp),
            int(cpu * 100),
            int(app_cpu * 100),
            email,
            pid,
            ppid,
            location,
            app_name,
            title.encode('ascii', 'ignore'),
            u'<a href=%s>%s</a>' % (
                get_url(url, app_name, title),
                get_url(url, app_name, title),
            ),
            u'<img src="%s" width=38>' % get_fav(fav, app_name, title),
        ))
    output.write("</table>")

def setup():
    sqlite3.connect(get_activity_path()).cursor().execute(INIT_QUERY)

try:
    setup()
except Exception as e:
    log.log("Cannot open activity database: %s. Retrying..." % e)
    path = get_activity_path()
    os.system("mv %s %s.%s" % (path, path, time.time()))
    try:
        setup()
    except:
        error.error("Cannot initialize activities.")
