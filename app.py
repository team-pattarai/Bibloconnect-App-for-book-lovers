from flask import *

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("landing_page.html")
if __name__ == "__main__":
    app.run(debug=True)