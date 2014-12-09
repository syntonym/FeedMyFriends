from flask import Flask, request, render_template, abort
import scraper
import json
import time
import database
from database import User, Feed, Keyword, session

app = Flask(__name__)


#Controller
def new_post_controller(new_url):

    post = {}

    try:
        post = scraper.ScrapeSite(new_url).get_site_dict()
        post['timestamp'] = time.time()
        post['status'] = "OK"
        #TODO: start worker to write results to database, should also add date parameter to record
    except:
        #TODO: need to predefine certain Exceptions or fail for "unknown"
        post['status'] = "Exception"

    return post



#View

@app.route("/init_db", methods=["POST"])
def init_db():
    database.init_db()
    abort(404)

@app.route("/feeds_get", methods=["GET"])
def get_feeds():
    feeds = session.query(Feed).limit(30)
    sdeef = [feed.rep() for feed in feeds]
    return(json.dumps(sdeef))

@app.route("/feeds", methods=["POST"])
def feeds():
    session = database.session
    session.add(Feed(request.form["link"]))
    session.commit()
    abort(405)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.session.remove()

@app.route("/scraper_api", methods=['GET', 'POST'])
def scraper_api():
    """method to handle the scraping of new posts entered from the browser or other sources"""
    url = request.args.get('url')
    return json.dumps(new_post_controller(url))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
