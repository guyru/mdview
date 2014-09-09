import argparse
import os.path
import random
import time
import webbrowser
import markdown

from flask import Flask, Markup, render_template, Response

__version__ = '0.0.1'

#app = Flask(__name__)
app = Flask('mdview')

@app.route('/')
def index():
    mtime = int(os.path.getmtime(app.config['filename']) * 1000)
    # it would be better if we could query the mtime() of the FD itself.

    source = open(app.config['filename'], 'rb').read()
    if app.extensions:
        html = markdown.markdown(source, extensions=app.config['extensions'])
    else:
        html = markdown.markdown(source)

    return render_template('base.html', html=Markup(html),
                           title=app.config['filename'],
                           mtime=mtime
                           )

class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None

    def encode(self):
        if not self.data:
            return ""
        lines = []
        for prop in ['event', 'id', 'data']:
            value = getattr(self, prop)
            if value:
                lines.append('%s: %s' % (prop, value))

        return "\n".join(lines) + '\n\n'

@app.route('/updates/<int:mtime>')
def updates(mtime):
    def updates_event():
        while True:
            new_mtime = int(os.path.getmtime(app.config['filename']) * 1000)
            if mtime < new_mtime:
                # this means that there was an update
                yield ServerSentEvent(new_mtime).encode()
            time.sleep(0.2)

    return Response(updates_event(), mimetype="text/event-stream")


def run():
    description = "Simple markdown viewer."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("filename")
    parser.add_argument("-x", "--extensions", help=("markdown extensions"
                        " separated by commas"))
    parser.add_argument('--version', action="version",
                        version="%(prog)s " + __version__)
    args = parser.parse_args()
    app.config['filename'] = args.filename
    app.config['extensions'] = None
    if args.extensions:
        app.config['extensions'] = args.extensions.split(',')


    # HACK: There must be a better way select a random port
    port = random.randrange(1024, 2**16)
    # HACK: In debug mode it will launch the browser with each reload.
    # There is also a race condition on when the server is actually up.
    webbrowser.open('http://localhost:%d/' % port)
    app.run(port=port, threaded=True)

if __name__ == '__main__':
    run()
