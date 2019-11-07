from flask import Flask, render_template, request, redirect, url_for, flash
import peeweedbevolve
import os
from models import * 

app = Flask(__name__)
app.secret_key = os.urandom(24)

def error_to_flash(errors):
    for error in errors:
        flash(error, 'alert alert-danger')

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
    store = Store(name=name)
    if store.save():
        flash('Create store successful', 'alert alert-primary')
        return redirect(url_for('store'))
    else:
        error_to_flash(store.errors)
        return render_template('new_store.html', store_name=name)

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
    return render_template('edit_store.html', store=store, warehouses=warehouses, store_name=store.name)

@app.route('/store/<store_id>/update', methods=["POST"])
def update_store(store_id):
    name = request.form.get('store_name')
    store = Store.get_or_none(Store.id == store_id)
    if store.name == name:
        flash('Edit store successful', 'alert alert-primary')
        return redirect(url_for('edit_store', store_id=store.id))

    backup_store_name = store.name
    store.name = name
    warehouses = store.warehouses
    if store.save():
        flash('Edit store successful', 'alert alert-primary')
        return redirect(url_for('edit_store', store_id=store.id))
    else:
        store.name = backup_store_name
        error_to_flash(store.errors)
        return render_template('edit_store.html', store=store, warehouses=warehouses, store_name=name)

@app.route("/warehouse", methods=["GET", "POST"])
def warehouse():
    stores = Store.select().order_by(Store.id.asc())
    if request.method == "POST":
        location = request.form.get('warehouse_location')
        store_id = request.form.get('store_id')
        store = Store.get_by_id(store_id)
        warehouse = Warehouse(location=location, store=store)
        if warehouse.save():
            flash('Create warehouse successful', 'alert alert-primary')
            return redirect(url_for('index'))
        else:
            error_to_flash(warehouse.errors)
            return render_template('warehouse.html', stores=stores, warehouse=warehouse)
    return render_template('warehouse.html', stores=stores)

if __name__ == '__main__':
    app.run()
