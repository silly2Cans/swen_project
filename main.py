from flask import Flask, current_app,request,render_template,url_for

app = Flask(__name__,
            static_url_path="/static",  
            static_folder="static",  
            template_folder="templates",  
            )

class Config(object):
    DEBUG = True
    ITCAST = "python"


app.config.from_object(Config)


@app.route("/index", methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.route("/bikeinfo", methods=["GET","POST"])
def bike():
    return render_template("bikeinfo.html")


@app.route("/googlemaps", methods=["GET","POST"])
def maps():
    return render_template("googlemaps.html")

if __name__ == '__main__':
    # app.run()
    app.run(host="127.0.0.1", port=5000, debug=True)