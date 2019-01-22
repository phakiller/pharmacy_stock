import flask_restful

from flask import Blueprint
from .resource import pharmacy_user, login, provider, medicine, customer, sale


api_bp = Blueprint('backend', __name__)
api = flask_restful.Api(api_bp)

api.add_resource(pharmacy_user.PharmacyUserResource, '/user/<int:user_id>')
api.add_resource(pharmacy_user.CreatePharmacyUserResource, '/user')
api.add_resource(pharmacy_user.PharmacyUsersResource, '/users')

api.add_resource(login.Login, '/login')

api.add_resource(provider.ProviderResource, '/provider/<int:provider_id>')
api.add_resource(provider.CreateProviderResource, '/provider')
api.add_resource(provider.ProvidersResource, '/providers')

api.add_resource(medicine.MedicineResource, '/medicine/<int:medicine_id>')
api.add_resource(medicine.CreateMedicineResource, '/medicine')
api.add_resource(medicine.MedicinesResource, '/medicines')
api.add_resource(medicine.UploadMedicinesResource, '/medicines/upload')
api.add_resource(medicine.MedicineStockControl,
                '/medicine/<int:medicine_id>/<string:action>')

api.add_resource(customer.CustomerResource, '/customer/<int:customer_id>')
api.add_resource(customer.CreateCustomerResource, '/customer')
api.add_resource(customer.CustomersResource, '/customers')

api.add_resource(sale.DeleteSaleResource, '/sale/<int:sale_id>')
api.add_resource(sale.FinalizeSaleResource, '/sale/<int:sale_id>/finalize')
api.add_resource(sale.CreateSaleResource, '/sale')
api.add_resource(sale.CreateSaleItemResource, '/sale/<int:sale_id>/item')
api.add_resource(sale.SaleItemResource,
                 '/sale/<int:sale_id>/item/<int:item_id>')
api.add_resource(sale.SalesResource, '/sales')
