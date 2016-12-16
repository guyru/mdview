import argparse
import os.path
import logging
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
    """The view that actually serves the markdown file
    """
    mtime = int(os.path.getmtime(app.config['filename']) * 1000)
    # it would be better if we could query the mtime() of the FD itself.

    source = open(app.config['filename'], 'rb').read().decode("utf-8")
    if app.config['extensions']:
        html = markdown.markdown(source, extensions=app.config['extensions'])
    else:
        html = markdown.markdown(source)

    return render_template('base.html', html=Markup(html),
                           title=app.config['filename'].decode('utf-8'),
                           mtime=mtime
                           )

class ServerSentEvent(object):
    """Helper class for Server-Sent Events
    """
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None

    def encode(self):
        """Encode the event data for sending.
        """
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
    """Endpoint for server-sent events about file changes.

    Periodically checks the served file for changes. If changes are
    detected it sents a server-sent event with the timestamp of the
    last change.
    """
    def updates_event():
        last_response = time.time()
        while True:
            new_mtime = int(os.path.getmtime(app.config['filename']) * 1000)
            if getattr(app, '_shutdown', False):
                return
            if mtime < new_mtime or time.time() - last_response > 1:
                # We periodically send "gratuitous" updates. It allows
                # us to detect if a client closed the connection, which
                # will trigger "Broken pipe" error and thus terminate
                # thread, however we don't have to do it very often.
                last_response = time.time()

                # This means that there was an update to the file we're
                # serving.
                yield ServerSentEvent(new_mtime).encode()
            time.sleep(0.2)

    return Response(updates_event(), mimetype="text/event-stream")

def run():
    description = "Simple markdown viewer."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("filename")
    parser.add_argument("-x", "--extensions", help=("markdown extensions"
                        " separated by commas. Default: %(default)s"),
                        default="extra,codehilite")
    parser.add_argument('--version', action="version",
                        version="%(prog)s " + __version__)
    parser.add_argument('--debug', action='store_true', default=False,
                        help='run server in debug mode')

    args = parser.parse_args()
    app.config['filename'] = args.filename
    app.config['extensions'] = None
    if args.extensions:
        app.config['extensions'] = args.extensions.split(',')
    app.config['DEBUG'] = args.debug


    # HACK: There must be a better way select a random port
    port = random.randrange(1024, 2**16)
    # HACK: In debug mode it will launch the browser with each reload.
    # There is also a race condition on when the server is actually up.
    webbrowser.open('http://localhost:%d/' % port)

    # we explicitly turn of the reloader, as it currently causes multiple
    # browser windows to be opened.
    app.run(port=port, threaded=True, use_reloader=False)
    app._shutdown = True

if __name__ == '__main__':
    run()
