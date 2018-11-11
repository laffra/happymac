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
    x number,
    y number,
    width number,
    height number,
    pixel text,
    location text,
    pid text,
    ppid text,
    name text,
    title text,
    url text,
    fav text
)"""
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

def update_tab(url, fav, title):
    since_when = int(time.time()) - HOUR_IN_MS
    connection = sqlite3.connect(get_activity_path())
    cursor = connection.cursor()
    cursor.execute('''
            UPDATE activities SET url = "%s", fav = "%s"
            WHERE TITLE = "%s" AND name = "Google Chrome" AND timestamp > ?
        ''' % (url, fav, title),
        (since_when,)
    )
    connection.commit()
    title_details[title] = (url, fav)
    log.log("New tab: %s" % repr(title))

def update():
    pid = utils.get_current_app_pid()
    cpu = process.family_cpu_usage(pid)
    if cpu < DORMANT_PROCESS_CPU:
        return
    connection = sqlite3.connect(get_activity_path())
    cursor = connection.cursor()
    x, y, w, h = utils.get_active_window_dimensions()
    title = utils.get_active_window_name()
    app_name = utils.get_current_app_name()
    url = get_url('', app_name, title)
    cursor.execute("""
            INSERT INTO activities (timestamp,system,cpu,x,y,width,height,pixel,location,pid,ppid,name,title,url)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, [
        int(time.time()),
        process.cpu(-1),
        cpu,
        x,
        y,
        w,
        h,
        repr(utils.get_screen_pixel(x + 4, y + 4)),
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
        log.log("Generate report with %d event in file %s" % (len(activities), filename))
        with open(filename, "w") as output:
            generate_header(output)
            generate_pie_chart(output, activities)
            generate_full_table(output, activities)
            generate_footer(output)
        webbrowser.open("file://%s" % filename)
    except:
        error.error("Cannot generate report")

def generate_header(output):
    output.write("""
        <html>
            <head>
                <title>HappyMac Report</title>
                <script src="https://www.chartjs.org/dist/2.7.3/Chart.bundle.js"></script>
                <script src="https://www.chartjs.org/samples/latest/utils.js"></script>
            </head>
            <body>
                <div id="canvas-holder">
                    <canvas id="chart-area"></canvas>
                </div>
    """)

def generate_footer(output):
    output.write("""
            </body>
        </html>
    """)

def generate_pie_chart(output, activities):
    html_template = """
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
		var config = {
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

		window.onload = function() {
			var ctx = document.getElementById('chart-area').getContext('2d');
			window.myPie = new Chart(ctx, config);
		};
        </script>
    """
    counts = collections.defaultdict(int)

    for timestamp, cpu, app_cpu, x, y, w, h, pixel, location, pid, ppid, app_name, window_title, url, fav in get_activities():
        counts[(pixel, url or app_name)] += 1

    for k, v in counts.items():
        print k, ":", v

    def format(title):
        return title.encode("utf8")[:32]

    labels = repr([format(title) for _,title  in counts.keys()])
    data = repr(list(counts.values()))
    html = html_template % {"data": data, "labels": labels}
    output.write(html)

def pixelToColor(pixel):
    return "rgba(%d,%d,%d,%d)" % eval(pixel) if pixel else "white"

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
            <th>Dimensions</th>
            <th>Pixel</th>
            <th>PID</th>
            <th>Parent PID</th>
            <th>Location</th>
            <th>APP NAME</th>
            <th>Window/Tab Title</td>
            <th>Url</th>
            <th>FavIcon</th>
        </tr>""")

    for timestamp, cpu, app_cpu, x, y, w, h, pixel, location, pid, ppid, app_name, window_title, url, fav in activities:
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
        <td>%s</td>
        </tr>
        """ % (
            datetime.datetime.fromtimestamp(timestamp),
            int(cpu * 100),
            int(app_cpu * 100),
            (x, y, w, h),
            u'<div style="width:40px; height:40px; background:%s"/>' % pixelToColor(pixel),
            pid,
            ppid,
            location,
            app_name,
            window_title.encode('ascii', 'ignore'),
            u'<a href=%s>%s</a>' % (
                get_url(url, app_name, window_title),
                get_url(url, app_name, window_title),
            ),
            u'<img src="%s" width=38>' % get_fav(fav, app_name, window_title),
        ))
    output.write("</table>")


sqlite3.connect(get_activity_path()).cursor().execute(INIT_QUERY)