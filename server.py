from flask import Flask, render_template, request, redirect, url_for, flash
import peeweedbevolve
import os
from models import * 

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

# @app.cli.command()
# def copy(): 
#     warehouses = Warehouse.select()
#     for warehouse in warehouses:
#         warehouse.store = warehouse.store_backup
#         warehouse.save()
#         print(f"store: {warehouse.store.name}, store backup: {warehouse.store_backup.name}")
#     print("Copy done")

@app.route("/")
def index():
    stores = Store.select().order_by(Store.id.asc())
    warehouses = Warehouse.select().order_by(Warehouse.id.asc())
    products = Product.select().order_by(Product.id.asc())
    return render_template('index.html', stores=stores, warehouses=warehouses, products=products)

@app.route("/store", methods=["GET"])
def store():
    stores = Store.select().order_by(Store.id.asc())
    return render_template('store.html', stores=stores)

@app.route("/store/new", methods=["GET"])
def new_store():
    return render_template('new_store.html')

@app.route("/store", methods=["POST"])
def create_store():
    stores = Store.select()
    name = request.form.get('store_name')
    if Store.validate(name):
        store = Store(name=name)
        if store.save():
            flash('Create store successful', 'alert alert-primary')
            return redirect(url_for('store'))
        else:
            flash('Create store fail', 'alert alert-danger')
            return render_template('store.html', stores)
    else:
        flash('Store name is not appropriate', 'alert alert-danger')
        return render_template('new_store.html')

@app.route("/store/<store_id>/delete", methods=["POST"])
def delete_store(store_id):
    store = Store.get_or_none(Store.id == store_id)
    store.delete_instance()
    flash('Delete store successful', 'alert alert-primary')
    return redirect(url_for('store'))

@app.route('/store/<store_id>', methods=["GET"])
def edit_store(store_id):
    store = Store.get_or_none(Store.id == store_id)
    if store:
        warehouses = store.warehouses        
    else:
        warehouses = None
    return render_template('edit_store.html', store=store, warehouses=warehouses)

@app.route('/store/<store_id>/update', methods=["POST"])
def update_store(store_id):
    name = request.form.get('store_name')
    store = Store.get_or_none(Store.id == store_id)
    store.name = name
    warehouses = store.warehouses
    if store.save():
        flash('Edit store successful', 'alert alert-primary')
        return redirect(url_for('store'))
    else:
        flash('Edit store fail', 'alert alert-danger')
        return render_template('edit_store.html', store_id=store.id)

@app.route("/warehouse", methods=["GET", "POST"])
def warehouse():
    stores = Store.select().order_by(Store.id.asc())
    if request.method == "POST":
        location = request.form.get('warehouse_location')
        store_id = request.form.get('store_id')
        store = Store.get_by_id(store_id)
        if Warehouse.validate(store):
            warehouse = Warehouse(location=location, store=store)
            if warehouse.save():
                flash('Create warehouse successful', 'alert alert-primary')
                return redirect(url_for('index'))
            else:
                flash('Create warehouse fail', 'alert alert-danger')
                return render_template('warehouse.html', stores=stores, warehouse=warehouse)
        else:
            flash('Cannot select this store or location is not appropriate', 'alert alert-danger')
            return render_template('warehouse.html', stores=stores)
    return render_template('warehouse.html', stores=stores)

if __name__ == '__main__':
    app.run()

# todo
# 1. validate -> how to remain values? Why validate at save instead of creation?
# 2. delete on cascade -> how to add this feature halfway?
# 3. error -> how to show proper error?
