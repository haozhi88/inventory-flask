from flask import Flask, render_template, request, redirect, url_for
import peeweedbevolve
from models import * 

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
    stores = Store.select()
    warehouses = Warehouse.select()
    products = Product.select()
    return render_template('info.html', stores=stores, warehouses=warehouses, products=products)

@app.route("/store", methods=["GET", "POST"])
def store():
    if request.method == "POST":
        store_name = request.form.get('store_name')
        s = Store(name=store_name)
        if s.save():
            print(f"DB saved new store: {store_name}")
            return redirect(url_for('store'))
        else:
            return render_template('store.html', store_name=store_name)
    # else request.method == "GET":
    return render_template('store.html')

if __name__ == '__main__':
    app.run()