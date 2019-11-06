from flask import Flask, render_template, request
import peeweedbevolve
from models import db 

app = Flask(__name__)

@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate(): 
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/info")
def info():
    print("info")
    return render_template('info.html')

@app.route("/store", methods=["GET", "POST"])
def store():
    # name = request.args.get('store_name')
    if request.method == "POST":
        name = request.form.get('store_name')
        print(f"New store name: {name}")

    return render_template('store.html')



if __name__ == '__main__':
    app.run()