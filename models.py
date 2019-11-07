import os
import peewee as pw
import datetime
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'))

class BaseModel(pw.Model):
   created_at = pw.DateTimeField(default=datetime.datetime.now)
   updated_at = pw.DateTimeField(default=datetime.datetime.now)

   def save(self, *args, **kwargs):
      self.errors = []
      self.validate()

      if len(self.errors) == 0:
         self.updated_at = datetime.datetime.now()
         return super(BaseModel, self).save(*args, **kwargs)
      else:
         return 0

   class Meta:
      database = db
      legacy_table_names = False

class Store(BaseModel):
   name = pw.CharField(unique=True)

   def validate(self):
      if len(self.name) > 0:
         store = Store.get_or_none(Store.name == self.name)
         if store:
            self.errors.append("Store name not unique")
      else:
         self.errors.append("Store name cannot be empty")

class Warehouse(BaseModel):
   store = pw.ForeignKeyField(Store, backref='warehouses', unique=True, on_delete="CASCADE")
   location = pw.TextField()
   # store_backup = pw.ForeignKeyField(Store, backref='warehouses', unique=True, on_delete="CASCADE", null=True)

   def validate(self):
      if len(self.location) > 0:
         stores = self.store.warehouses
         if len(stores):
            self.errors.append("This store has been selected")
      else:
         self.errors.append("Warehouse location cannot be empty")

class Product(BaseModel):
   name = pw.CharField(index=True)
   description = pw.TextField()
   warehouse = pw.ForeignKeyField(Warehouse, backref='products', on_delete="CASCADE")
   color = pw.CharField(null=True)