import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
   created_at = pw.DateTimeField(default=datetime.datetime.now)
   updated_at = pw.DateTimeField(default=datetime.datetime.now)

   def save(self, *args, **kwargs):
       self.updated_at = datetime.datetime.now()
       return super(BaseModel, self).save(*args, **kwargs)

   class Meta:
       database = db
       legacy_table_names = False

class Store(BaseModel):
   name = pw.CharField(unique=True)

   def validate(name):
      if len(name) > 0:
         store = Store.get_or_none(Store.name == name)
         if not store:
            return True      
      return False

class Warehouse(BaseModel):
   store = pw.ForeignKeyField(Store, backref='warehouses', unique=True, on_delete="CASCADE")
   location = pw.TextField()

   def validate(store, location):
      if len(location) > 0:
         store = Store.get_or_none(Store.id == store.id)
         if not store:
            return True
      return False

class Product(BaseModel):
   name = pw.CharField(index=True)
   description = pw.TextField()
   warehouse = pw.ForeignKeyField(Warehouse, backref='products', on_delete="CASCADE")
   color = pw.CharField(null=True)