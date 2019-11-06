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
    stores = Store.select()
    warehouses = Warehouse.select()
    products = Product.select()
    return render_template('index.html', stores=stores, warehouses=warehouses, products=products)

@app.route("/store", methods=["GET", "POST"])
def store():
    stores = Store.select()
    if request.method == "POST":
        name = request.form.get('store_name')
        store = Store(name=name)
        if store.save():
            print(f"New store created: {store.id}, {store.name}")
            return redirect(url_for('store'))
        else:
            return render_template('store.html', stores=stores, store=store)
    return render_template('store.html', stores=stores)

@app.route('/store/<store_id>', methods=["GET", "POST"])
def store_id(store_id):

    # if request.method == "POST":
    #     name = request.form.get('store_name')
    #     print(f"debug store name: {name}")

    # store = Store.get_or_none(store_id)
    stores = Store.select().where(Store.id==store_id).limit(1)
    if len(stores):
        store = stores[0]
        warehouses = store.warehouses
        print(f"store id: {store_id}, store name: {store.name}")
        return render_template('store_id.html', store=store, warehouses=warehouses)
    else:
        store = None
        return render_template('store_id.html', store=store)

@app.route("/warehouse", methods=["GET", "POST"])
def warehouse():
    stores = Store.select()
    if request.method == "POST":
        location = request.form.get('warehouse_location')
        store_id = request.form.get('store_id')
        store = Store.get_by_id(store_id)
        warehouse = Warehouse(location=location, store=store)
        if warehouse.save():
            print(f"New warehouse created: {warehouse.id}, {warehouse.location}")
            return redirect(url_for('warehouse'))
        else:
            return render_template('warehouse.html', stores=stores, warehouse=warehouse)
    return render_template('warehouse.html', stores=stores)

if __name__ == '__main__':
    app.run()