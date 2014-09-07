import argparse
import random
import webbrowser
import markdown

from flask import Flask, Markup, render_template

__version__ = '0.0.1'

#app = Flask(__name__)
app = Flask('mdview')

@app.route('/')
def index():
    source = open(app.config['filename'], 'rb').read()
    if app.extensions:
        html = markdown.markdown(source, extensions=app.config['extensions'])
    else:
        html = markdown.markdown(source)
    return render_template('base.html', html=Markup(html), title=app.config['filename'])
    return Markup(html)

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
    port = 5000
    # HACK: In debug mode it will launch the browser with each reload.
    # There is also a race condition on when the server is actually up.
    webbrowser.open('http://localhost:%d/' % port)
    app.run(port=port)

if __name__ == '__main__':
    run()
